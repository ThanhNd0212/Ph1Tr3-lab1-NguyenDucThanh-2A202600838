# Kế hoạch Lab 16 — Reflexion Agent

## Tổng quan mục tiêu

Xây dựng Reflexion Agent hoạt động thật (thay mock bằng LLM), chạy benchmark so sánh với ReAct baseline, và nộp report đạt đủ tiêu chí chấm điểm tự động.

---

## Rubric điểm — Cách đạt tối đa 100đ

| Phần | Điểm | Điều kiện cụ thể |
|---|---:|---|
| Schema completeness | 30 | `report.json` có đủ 6 key: `meta`, `summary`, `failure_modes`, `examples`, `extensions`, `discussion` |
| Experiment completeness | 30 | Có **cả ReAct + Reflexion**, ≥ **100 records**, ≥ **20 examples** chi tiết |
| Analysis depth | 20 | ≥ **3 failure modes** được phân tích; `discussion` ≥ **250 ký tự** |
| **Bonus** | **20** | Triển khai ≥ 1 extension (10đ/extension, tối đa 20đ) |

**Tổng tối đa: 100đ** (80đ core + 20đ bonus)

---

## Lộ trình thực hiện (120 phút)

### Bước 1 — Hiểu flow, chạy mock (30 phút)

- [ ] Đọc `src/reflexion_lab/agents.py` — vòng lặp ReAct + Reflexion
- [ ] Đọc `src/reflexion_lab/mock_runtime.py` — 3 hàm cần thay: `actor_answer()`, `evaluator()`, `reflector()`
- [ ] Đọc `src/reflexion_lab/schemas.py` — xem các TODO cần điền
- [ ] Đọc `src/reflexion_lab/prompts.py` — xem các TODO cần viết prompt
- [ ] Chạy thử mock để hiểu output format:
  ```bash
  python run_benchmark.py --dataset data/hotpot_mini.json --out-dir outputs/sample_run
  python autograde.py --report-path outputs/sample_run/report.json
  ```

---

### Bước 2 — Hoàn thiện TODO trong scaffold (35 phút)

**2a. `schemas.py` — Định nghĩa dataclass/fields:**
- [ ] `JudgeResult`: thêm trường `score` (float 0–1) và `reason` (str)
- [ ] `ReflectionEntry`: thêm trường `attempt_id`, `failure_reason`, `lesson`, `strategy_next`

**2b. `prompts.py` — Viết 3 system prompts:**
- [ ] `ACTOR_SYSTEM`: hướng dẫn agent trả lời câu hỏi multi-hop dựa trên context
- [ ] `EVALUATOR_SYSTEM`: hướng dẫn LLM-as-Judge cho điểm 0–1 + lý do
- [ ] `REFLECTOR_SYSTEM`: hướng dẫn phân tích lỗi và đề xuất chiến lược mới

**2c. `agents.py` (dòng 31–35) — Triển khai Reflexion loop:**
- [ ] Gọi `reflector()` khi evaluator trả về `score < 1`
- [ ] Cập nhật `reflection_memory` với entry mới
- [ ] Truyền `reflection_memory` vào lần gọi `actor_answer()` tiếp theo

---

### Bước 3 — Thay mock bằng LLM thật (trong `mock_runtime.py`)

| Hàm mock | Thay bằng |
|---|---|
| `actor_answer()` | `ACTOR_SYSTEM` + question + context → LLM → parse câu trả lời |
| `evaluator()` | `EVALUATOR_SYSTEM` + question + gold + predicted → LLM → parse `JudgeResult` |
| `reflector()` | `REFLECTOR_SYSTEM` + question + wrong answer + reason → LLM → parse `ReflectionEntry` |

- [ ] Chọn provider: Ollama / OpenAI API / Gemini API / vLLM
- [ ] Thay `token_estimate` và `latency_ms` hardcoded bằng giá trị thật từ LLM response

---

### Bước 4 — Tạo dataset và chạy Benchmark (30 phút)

- [ ] Tải HotpotQA dataset (link trong README hoặc Google Drive)
- [ ] Convert sang format `QAExample` và lưu vào `data/my_test_set.json`
- [ ] **Yêu cầu tối thiểu: ≥ 100 mẫu** (autograde kiểm tra `num_records >= 100`)
- [ ] Chạy benchmark cả ReAct và Reflexion:
  ```bash
  python run_benchmark.py --dataset data/my_test_set.json --out-dir outputs/final_run
  ```
- [ ] Kiểm tra output có đủ: `report.json`, `report.md`, `react_runs.jsonl`, `reflexion_runs.jsonl`
- [ ] Chạy autograde để kiểm tra điểm:
  ```bash
  python autograde.py --report-path outputs/final_run/report.json
  ```

---

### Bước 5 — Viết report đạt đủ tiêu chí (song song với benchmark)

**`report.json` phải có đủ 6 key:**
```json
{
  "meta": { ... },
  "summary": { "react_em": ..., "reflexion_em": ..., ... },
  "failure_modes": [ { "mode": "...", "count": ..., "analysis": "..." }, ... ],
  "examples": [ { ... }, ... ],
  "extensions": [ "..." ],
  "discussion": "Phân tích trade-off... (≥250 ký tự)"
}
```

**`report.md` phải có:**
- [ ] Bảng so sánh EM giữa ReAct và Reflexion
- [ ] Phân tích ≥ 3 failure modes
- [ ] Phân tích chi phí token
- [ ] Discussion ≥ 250 ký tự về trade-off

---

## Bonus — Lấy thêm 20đ (ưu tiên dễ → khó)

| Extension | Điểm | Độ khó |
|---|---:|---|
| `structured_evaluator` — Evaluator parse Pydantic thay vì regex | 10 | Dễ |
| `reflection_memory` — Lưu và truyền memory qua các lần thử | 10 | Dễ |
| `mock_mode_for_autograding` — Flag để chạy mock khi autograding | 10 | Dễ |
| `benchmark_report_json` — Xuất report JSON đầy đủ | 10 | Trung bình |
| `adaptive_max_attempts` — Tự điều chỉnh số lần thử theo độ khó | 10 | Trung bình |
| `memory_compression` — Tóm tắt reflection memory khi quá dài | 10 | Khó |
| `mini_lats_branching` — Sinh 2 candidates/step, chọn tốt nhất | 10 | Khó |
| `plan_then_execute` — Lên kế hoạch trước khi reflect | 10 | Khó |

**Gợi ý:** Làm `structured_evaluator` + `reflection_memory` để dễ lấy 20đ bonus.

---

## Deliverables cần nộp lên GitHub

```
outputs/final_run/
├── report.json          ← bắt buộc (6 key đầy đủ)
├── report.md            ← bắt buộc (narrative analysis)
├── react_runs.jsonl     ← bắt buộc (trace từng câu)
└── reflexion_runs.jsonl ← bắt buộc (trace từng câu)
```

---

## Lưu ý — Golden Test Set (15 phút cuối)

- Giảng viên sẽ phát bộ test **chưa từng thấy** trong 15 phút cuối
- Cần đảm bảo agent hoạt động tốt trên **câu hỏi đa dạng**, không chỉ `hotpot_mini.json`
- Kết quả Golden Test Set dùng để **xếp hạng và tính điểm bonus nhóm**
- Chuẩn bị: tự tạo dataset đa dạng, test trước trên nhiều loại câu hỏi multi-hop

---

## Checklist cuối — Kiểm tra trước khi nộp

- [ ] `schemas.py`: `JudgeResult` và `ReflectionEntry` không còn `pass`
- [ ] `prompts.py`: 3 prompts đã viết đầy đủ
- [ ] `agents.py`: Reflexion loop hoạt động (gọi reflector + cập nhật memory)
- [ ] Mock đã được thay bằng LLM thật
- [ ] `token_estimate` và `latency_ms` là giá trị thật
- [ ] Dataset ≥ 100 mẫu đã chạy xong
- [ ] `report.json` có đủ 6 key
- [ ] `report.md` có ≥ 3 failure modes + discussion ≥ 250 ký tự
- [ ] `autograde.py` chạy pass không lỗi
- [ ] Bonus extension đã gắn tên vào key `extensions` trong report
