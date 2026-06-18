"""Convert hotpot_dev_distractor_v1.json to QAExample format and sample N records."""
import argparse
import json
import random
from pathlib import Path


def convert(src: str, out: str, n: int, seed: int) -> None:
    with open(src, encoding="utf-8") as f:
        raw = json.load(f)

    random.seed(seed)
    sample = random.sample(raw, min(n, len(raw)))

    records = []
    for item in sample:
        context = [
            {"title": title, "text": " ".join(sentences)}
            for title, sentences in item["context"]
        ]
        records.append({
            "qid": item["_id"],
            "difficulty": item.get("level", "medium"),
            "question": item["question"],
            "gold_answer": item["answer"],
            "context": context,
        })

    Path(out).parent.mkdir(parents=True, exist_ok=True)
    with open(out, "w", encoding="utf-8") as f:
        json.dump(records, f, ensure_ascii=False, indent=2)

    print(f"Saved {len(records)} records to {out}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--src", default="data/hotpot_dev_distractor_v1.json")
    parser.add_argument("--out", default="data/hotpot_100.json")
    parser.add_argument("--n", type=int, default=120)
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()
    convert(args.src, args.out, args.n, args.seed)
