import json
from collections import Counter

records = [json.loads(l) for l in open("outputs/final_run/reflexion_runs.jsonl")]
attempts_counter = Counter(r["attempts"] for r in records)

print("=== Phan bo so lan thu (Reflexion) ===")
for k in sorted(attempts_counter):
    total = attempts_counter[k]
    correct = sum(1 for r in records if r["attempts"] == k and r["is_correct"])
    print(f"  {k} lan thu: {total:3d} mau  (dung={correct}, sai={total - correct})")
print(f"  Tong:       {len(records):3d} mau")

retried = [r for r in records if r["attempts"] >= 2]
print(f"\n=== Chi tiet retry ({len(retried)} mau da thu lai) ===")
print(f"{'qid':20s}  {'attempts':8s}  {'correct':8s}  {'gold':30s}  predicted")
for r in retried:
    gold = r["gold_answer"][:28]
    pred = r["predicted_answer"][:28]
    print(f"  {r['qid'][:18]:18s}  {r['attempts']:8d}  {str(r['is_correct']):8s}  {gold:30s}  {pred}")

recovered = sum(1 for r in retried if r["is_correct"])
failed = sum(1 for r in retried if not r["is_correct"])
print(f"\nTong retry: {len(retried)} mau  |  Phuc hoi thanh cong: {recovered}  |  Van sai: {failed}")
print(f"Ti le phuc hoi: {recovered/len(retried)*100:.1f}%")
