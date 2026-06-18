from __future__ import annotations
from typing import Literal, Optional, TypedDict
from pydantic import BaseModel, ConfigDict, Field

class ContextChunk(BaseModel):
    title: str
    text: str

class QAExample(BaseModel):
    qid: str
    difficulty: Literal["easy", "medium", "hard"]
    question: str
    gold_answer: str
    context: list[ContextChunk]

class JudgeResult(BaseModel):
    model_config = ConfigDict(extra="ignore")
    score: int = Field(..., description="1 nếu đúng, 0 nếu sai")
    reason: str = Field(..., description="Lý do đánh giá")
    missing_evidence: Optional[list[str]] = Field(default=None, description="Bằng chứng còn thiếu")
    spurious_claims: Optional[list[str]] = Field(default=None, description="Các khẳng định sai")

class ReflectionEntry(BaseModel):
    model_config = ConfigDict(extra="ignore")
    attempt_id: int = Field(..., description="ID của lần thử thất bại")
    failure_reason: str = Field(..., description="Lý do tại sao câu trả lời sai")
    lesson: str = Field(..., description="Bài học rút ra từ lần thử này")
    next_strategy: str = Field(..., description="Chiến lược cho lần thử tiếp theo")

class AttemptTrace(BaseModel):
    attempt_id: int
    answer: str
    score: int
    reason: str
    reflection: Optional[ReflectionEntry] = None
    token_estimate: int = 0
    latency_ms: int = 0

class RunRecord(BaseModel):
    qid: str
    question: str
    gold_answer: str
    agent_type: Literal["react", "reflexion"]
    predicted_answer: str
    is_correct: bool
    attempts: int
    token_estimate: int
    latency_ms: int
    failure_mode: Literal["none", "entity_drift", "incomplete_multi_hop", "wrong_final_answer", "looping", "reflection_overfit"]
    reflections: list[ReflectionEntry] = Field(default_factory=list)
    traces: list[AttemptTrace] = Field(default_factory=list)

class ReportPayload(BaseModel):
    meta: dict
    summary: dict
    failure_modes: dict
    examples: list[dict]
    extensions: list[str]
    discussion: str

class ReflexionState(TypedDict):
    question: str
    context: list[str]
    trajectory: list[str]
    reflection_memory: list[str]
    attempt_count: int
    success: bool
    final_answer: str
