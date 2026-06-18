1. Thông tin chung về Bài Lab
Tên bài lab: Lab 16 — Implement Reflexion agent từ scratch với LangGraph.

Mục tiêu: Xây dựng Reflexion agent repo + benchmark report (so sánh EM, phân tích chi phí cost, phân loại các failure modes).

Thời lượng: 2 giờ (120 phút).

2. Hướng dẫn & Các bước thực hiện (Roadmap)
Quá trình làm bài được chia làm 4 bước chính với lộ trình thời gian gợi ý như sau:

Bước 1: Chạy ReAct baseline và hiểu trace (30 phút)

Xây dựng state machine với các nodes: [act, evaluate, reflect, terminate] cùng các edges có định tuyến điều kiện (conditional routing).

Mẹo từ giảng viên: Học viên nên chạy ở chế độ giả lập (mock mode) trước để hiểu định dạng đầu ra (format output) trước khi thay đổi provider thật.

Bước 2: Thêm Evaluator dạng structured output (35 phút)

Xây dựng Evaluator theo dạng LLM-as-Judge.

Prompt yêu cầu trả về điểm số từ 0-1 kèm theo lý do (reason), parse kết quả đầu ra bằng Pydantic.

Bước 3: Thêm Reflector + reflection memory (25 phút)

Cấu trúc mỗi entry bộ nhớ bao gồm: (attempt_id, failure_reason, lesson, strategy_next).

Bước 4: Benchmark, viết report, sinh artifact để auto-grade (30 phút)

Chạy thử nghiệm so sánh giữa Reflexion và ReAct trên 20 câu hỏi HotpotQA.

Đo lường các chỉ số: Exact Match (EM), số lần thử (attempts), và token cost.

3. Yêu cầu sản phẩm nộp (Deliverables)
Để phục vụ chấm điểm tự động nhanh chóng và khách quan từ Trợ giảng (TA), sản phẩm nộp lên GitHub repo phải tuân thủ đúng cấu trúc (schema) ổn định sau:

report.json: Bảng số liệu/metric tổng hợp.

report.md: Bài phân tích chuyên sâu (narrative analysis), so sánh bảng EM, phân tích chi phí và phân loại các failure modes.

react_runs.jsonl và reflexion_runs.jsonl: Dữ liệu trace chi tiết theo từng câu hỏi.

4. Tiêu chí chấm điểm (Grading Criteria)
Chấm điểm Objective (Tự động/Nhanh): Dựa trên việc giữ vững cấu trúc dữ liệu nộp (Deliverable schema) để TA quét nhanh các chỉ số định lượng.

Chấm điểm nâng cao & phân hóa học viên:

Không chỉ chấm theo tiêu chí "có làm được hay không" mà sẽ đánh giá thêm thông qua thí nghiệm, phân tích trade-off (sự đánh đổi) và cách giải thích của học viên trong báo cáo.

Các task Bonus để lấy điểm tối đa (Phân hóa học viên): Học viên có thể triển khai thêm các tính năng cao cấp sau:

adaptive max attempts

memory compression

evidence-grounded evaluator

mini-LATS branching (2 candidates / step)

plan-then-execute trước khi thực hiện reflect