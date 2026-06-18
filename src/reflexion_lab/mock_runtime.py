from __future__ import annotations
import json
import os
import time
from dotenv import load_dotenv
from google import genai
from google.genai import errors as genai_errors
from google.genai import types
from .schemas import QAExample, JudgeResult, ReflectionEntry
from .prompts import ACTOR_SYSTEM, EVALUATOR_SYSTEM, REFLECTOR_SYSTEM

load_dotenv()

_client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
_MODEL = os.getenv("LLM_MODEL", "gemini-2.5-flash-lite")

# Kept for compatibility with agents.py; real failure modes are determined post-hoc
FAILURE_MODE_BY_QID: dict[str, str] = {}


def _call_with_retry(model: str, contents: str, config, max_retries: int = 6):
    for attempt in range(max_retries):
        try:
            return _client.models.generate_content(model=model, contents=contents, config=config)
        except genai_errors.ServerError:
            if attempt == max_retries - 1:
                raise
            time.sleep(min(2 ** attempt + 2, 30))


def _format_context(example: QAExample) -> str:
    return "\n\n".join(f"[{c.title}]\n{c.text}" for c in example.context)


def _token_count(response) -> int:
    usage = response.usage_metadata
    if usage and usage.total_token_count:
        return usage.total_token_count
    return 0


def actor_answer(example: QAExample, _attempt_id: int, _agent_type: str, reflection_memory: list[str]) -> tuple[str, int, int]:
    context_str = _format_context(example)
    user_msg = f"Context:\n{context_str}\n\nQuestion: {example.question}"
    if reflection_memory:
        notes = "\n".join(f"- {r}" for r in reflection_memory)
        user_msg += f"\n\nReflection notes from previous attempts:\n{notes}"

    t0 = time.perf_counter()
    response = _call_with_retry(
        model=_MODEL,
        contents=user_msg,
        config=types.GenerateContentConfig(system_instruction=ACTOR_SYSTEM),
    )
    latency_ms = int((time.perf_counter() - t0) * 1000)
    return response.text.strip(), _token_count(response), latency_ms


def evaluator(example: QAExample, answer: str) -> tuple[JudgeResult, int, int]:
    user_msg = (
        f"Question: {example.question}\n"
        f"Gold answer: {example.gold_answer}\n"
        f"Predicted answer: {answer}"
    )
    t0 = time.perf_counter()
    response = _call_with_retry(
        model=_MODEL,
        contents=user_msg,
        config=types.GenerateContentConfig(
            system_instruction=EVALUATOR_SYSTEM,
            response_mime_type="application/json",
        ),
    )
    latency_ms = int((time.perf_counter() - t0) * 1000)
    data = json.loads(response.text)
    return JudgeResult(**data), _token_count(response), latency_ms


def reflector(example: QAExample, attempt_id: int, judge: JudgeResult, wrong_answer: str = "") -> tuple[ReflectionEntry, int, int]:
    user_msg = (
        f"Question: {example.question}\n"
        f"Wrong answer given: {wrong_answer}\n"
        f"Judge's reason: {judge.reason}"
    )
    if judge.missing_evidence:
        user_msg += f"\nMissing evidence needed: {'; '.join(judge.missing_evidence)}"

    t0 = time.perf_counter()
    response = _call_with_retry(
        model=_MODEL,
        contents=user_msg,
        config=types.GenerateContentConfig(
            system_instruction=REFLECTOR_SYSTEM,
            response_mime_type="application/json",
        ),
    )
    latency_ms = int((time.perf_counter() - t0) * 1000)
    data = json.loads(response.text)
    return ReflectionEntry(attempt_id=attempt_id, **data), _token_count(response), latency_ms
