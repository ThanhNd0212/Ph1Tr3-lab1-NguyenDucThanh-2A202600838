import json

react = [json.loads(l) for l in open("outputs/golden_run/react_runs.jsonl")]
reflex = [json.loads(l) for l in open("outputs/golden_run/reflexion_runs.jsonl")]
reflex_map = {r["qid"]: r for r in reflex}

print("=== Ket qua tung cau - Golden Test Set ===")
print(f"{'#':>2}  {'ReAct':6}  {'Reflex':6}  {'Attempts':8}  {'Gold Answer':35}  Predicted (Reflexion)")
print("-" * 110)
for i, r in enumerate(react, 1):
    rf = reflex_map[r["qid"]]
    ra = "DUNG" if r["is_correct"] else "SAI "
    rfa = "DUNG" if rf["is_correct"] else "SAI "
    gold = r["gold_answer"][:33]
    pred = rf["predicted_answer"][:40].replace("\n", " ")
    print(f"{i:2d}  [{ra}]  [{rfa}]  {rf['attempts']:8d}  {gold:35}  {pred}")

print()
print("=== Tong ket ===")
react_em = sum(r["is_correct"] for r in react) / len(react)
reflex_em = sum(r["is_correct"] for r in reflex) / len(reflex)
print(f"ReAct    EM: {react_em*100:.1f}%  ({sum(r['is_correct'] for r in react)}/{len(react)})")
print(f"Reflexion EM: {reflex_em*100:.1f}%  ({sum(r['is_correct'] for r in reflex)}/{len(reflex)})")

wrong_react = {r["qid"] for r in react if not r["is_correct"]}
wrong_reflex = {r["qid"] for r in reflex if not r["is_correct"]}
recovered = wrong_react - wrong_reflex
still_wrong = wrong_react & wrong_reflex
new_wrong = wrong_reflex - wrong_react

print(f"\nReAct sai:         {len(wrong_react)} mau")
print(f"Reflexion phuc hoi: {len(recovered)} mau")
print(f"Van sai:            {len(still_wrong)} mau")
if new_wrong:
    print(f"Reflexion lam hong: {len(new_wrong)} mau (regression)")
