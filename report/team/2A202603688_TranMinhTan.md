# Báo cáo cá nhân — Trần Minh Tân

## 1. Thông tin thành viên

- Họ tên: Trần Minh Tân
- MSSV: 2A202603688
- Email: minhtantran.contact@gmail.com
- GitHub: https://github.com/minhtantran99

## 2. Phần việc phụ trách

- Durability: phụ trách kiểm tra các tình huống crash, retry/resume và tính idempotency của ledger.
- Benchmark/ADR: phụ trách chạy benchmark, tổng hợp kết quả và viết quyết định kiến trúc trong `report/team/decision_adr.md`.

## 3. Đóng góp cụ thể

- Sinh báo cáo crash suite đạt an toàn tuyệt đối 20/20 (`src/reports/crash.json`).
- Thêm 3 test case kiểm thử độ bền vững (durability) và idempotency trong file `src/tests/test_refund_idempotency.py`:
  + `test_crash_before_effect_leaves_no_trace_and_resumes`: Kiểm tra crash trước khi ghi ledger (`before_effect`), bảo đảm không để lại dữ liệu rác trong ledger hay checkpoint, và khi resume ghi nhận thành công 1 refund.
  + `test_crash_after_checkpoint_resumes_idempotently`: Kiểm tra crash sau khi ghi checkpoint (`after_checkpoint`), khi resume thì hệ thống nhận diện `idempotent_replay` và không tạo dòng refund trùng lặp.
  + `test_repeated_sequential_replays_keep_single_row_and_single_audit`: Kiểm tra gọi lặp lại liên tiếp nhiều lần với cùng claim và số tiền, bảo đảm bảng `refund_ledger` chỉ tồn tại duy nhất 1 dòng và bảng `audit_events` chỉ có duy nhất 1 sự kiện `refund_committed`.
- Hoàn thành nội dung nghiên cứu trên `report/team/research_card.md` theo đề tài R2 (Failure taxonomy - NeurIPS 2025) phân tích điểm yếu của Swarm khi thiếu kiểm chứng chéo và tin dữ liệu người dùng.

## 4. Bằng chứng

- File kết quả crash test: `src/reports/crash.json` (`crash_safety: "20/20"`).
- Test đã thêm: `src/tests/test_refund_idempotency.py` (vượt qua toàn bộ bộ test cổng host `python -m pytest -q` với 57 passed).
- Commit ghi nhận trên nhánh `tan_branch`: `89d6275` ("feat(durability): add crash test report 20/20, add idempotency tests and draft research card").

## 5. Công cụ AI đã dùng

- Antigravity AI hỗ trợ phân tích luồng Durability, đối soát các điều kiện crash safety, viết các test case edge case idempotency và lập khung báo cáo cá nhân / Research card.
- Tự kiểm tra bằng các lệnh chuẩn:
  + `python -m lab8.smoke` (pass)
  + `python -m lab8.crash_test --count 20 --out reports/crash.json` (20/20 pass)
  + `python -m pytest -q` (57 passed, 248 deselected).

## 6. Tự đánh giá

- Đã hoàn thành toàn bộ phần việc Durability độc lập ban đầu, đảm bảo tính sẵn sàng cho hệ thống và chuẩn bị sẵn các bài test bảo vệ trước khi tích hợp các Shape do các thành viên khác phụ trách.
