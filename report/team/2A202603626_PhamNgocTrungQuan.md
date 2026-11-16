# Báo cáo cá nhân — 2A202603626_PhamNgocTrungQuan

## 1. Thông tin thành viên

- Họ tên: Phạm Ngọc Trung Quân
- MSSV: 2A202603626
- Email: trungquana123@gmail.com
- GitHub: https://github.com/jadenphm29

## 2. Phần việc phụ trách

- **Kiến trúc đảm nhiệm:** Shape B (`single` — Single ReAct Agent) tại `src/lab8/shapes/single.py`.
- **Ranh giới an toàn ReAct:** Hiện thực hóa vòng lặp suy luận ReAct có chặn chặn chặn (`max_steps=8`), đảm bảo Agent chỉ được gọi các công cụ đọc (`READONLY_TOOLS`), tuyệt đối không cấp quyền ghi vào sổ cái hay cấp quyền gọi `issue_refund` cho model.
- **Tích hợp Durability & Policy:** Kết nối Shape B với cổng host `durability.issue_refund`, truyền đầy đủ `crash_at` mà không nuốt ngoại lệ `InjectedCrash`, bảo đảm trần bồi thường theo đơn và chống trùng lặp (idempotency key `refund:{claim_id}`).
- **Kiểm thử & Bằng chứng:** Viết và kiểm thử các kịch bản test ma trận cho Shape B, đảm bảo Trace contract v1 sạch secret/PII và pass toàn bộ các case public/hidden.

## 3. Đóng góp cụ thể

- **Thiết kế vòng lặp ReAct an toàn (Shape B):**
  - Xây dựng hàm `decide` tương tác qua `MockLLM` với budget kiểm soát chặt chẽ; điều hướng agent tuần tự qua các bước: đọc claim (`get_claim_view`), tra cứu đơn hàng (`lookup_order`), đối chiếu chính sách (`lookup_policy`), và tính mức bồi hoàn (`compute_compensation`).
  - Đảm bảo agent không bị đánh lừa bởi dữ liệu khách hàng nhập trong ticket (bỏ qua số ngày trễ khai khống hay câu lệnh prompt injection kiểu *"ignore policy"*), lấy sự thật duy nhất từ DB.
  - Sau khi agent ReAct kết thúc, code của Shape B trực tiếp tiếp quản: kiểm tra proposal > 0 thì gọi `durability.issue_refund(conn, claim_id, proposal, crash_at=crash_at)` với **quote đầy đủ** để host tự trừ khoản đã hoàn trước đó (per-order cap).
- **Tuân thủ Trace contract v1:**
  - Khởi tạo trace hợp lệ gắn liền với `run_id = make_run_id("single", claim_id, seed)`.
  - Tuyệt đối không log toàn bộ `claim_row` hay `order_row` thô vào trace; loại bỏ hoàn toàn `parent_secret`, số điện thoại, địa chỉ nhận hàng và ghi chú nội bộ.
  - Đảm bảo mọi đường thoát (exit paths) kể cả `needs_info`, `escalated`, `denied` đều ghi trace và gọi `lab8.shapes.common.finish()`.
- **Kiểm thử & Fix bug:**
  - Viết bộ test chuyên biệt `src/tests/test_single_agent.py` gồm 17 test case: kiểm tra 12 ca public claims, chống ảo giác số ngày trễ ở seed 55, chặn model gọi tool ghi (`ToolRejected`), chặn vòng lặp vượt 8 bước (`step_cap`), kiểm tra trace contract sạch không rò rỉ PII/secret, và kiểm tra cơ chế ghi đè retry/crash durability.

## 4. Bằng chứng

- **Code Shape B:** `src/lab8/shapes/single.py` (thay thế stub `not_implemented`).
- **File test tác giả:** `src/tests/test_single_agent.py` (17/17 passed).
- **Lệnh kiểm thử đã chạy pass:**
  - `python -m pytest -q tests/test_single_agent.py` (17 passed).
  - `python -m pytest -q` (Cổng host: 71 passed).
  - `python -m pytest -q -m student -k single` (Toàn bộ test student của Shape B đạt 100% pass).
  - `python -m lab8.smoke` (Smoke test pass, trace clean).
- **Run ID / Commit:**
  - Commit kỹ thuật của nhánh cá nhân `quan-branch`.
  - Trace logs lưu tại `src/traces/` không chứa `CANARY_SECRET_*` hay chuỗi cấm PII.

## 5. Công cụ AI đã dùng

- **Công cụ hỗ trợ:** Trợ lý AI (Antigravity / Claude).
- **Mục đích sử dụng:**
  - Hỗ trợ phân tích kiến trúc ReAct loop trong `src/lab8/runtime.py` và cách thức cấu trúc `decide(observation)` cho phù hợp với `max_steps=8`.
  - Tra cứu quy tắc xử lý biên của host đối với `proposal_amount` (quote đầy đủ vs số thực nhận sau khi trừ per-order cap).
  - Soạn thảo checklist tự kiểm tra rò rỉ PII/Secret trong trace file.
- **Cách tự kiểm tra lại kết quả:**
  - Tự chạy và đối chiếu trực tiếp qua `pytest` và script audit `check_trace`.
  - Kiểm tra thủ công nội dung file trace `.json` sinh ra từ các lần chạy thử xem có field nhạy cảm nào bị sót hay không.
  - Đối chiếu logic tiền hoàn với [docs/business_rules.md](../../docs/business_rules.md) để khẳng định code chứ không phải AI quyết định số tiền.

## 6. Tự đánh giá

- **Mức độ hoàn thành:** 100% yêu cầu đặt ra cho cá nhân đối với Shape B (CP1 -> CP5).
- **Bài học kinh nghiệm:**
  - Hiểu rõ ranh giới sống còn giữa Code và Agent trong các hệ thống tài chính/giao dịch: LLM chỉ nên đóng vai trò là "mắt đọc" và "soạn thảo", tuyệt đối không giao quyền quyết định số tiền hay quyền ghi DB trực tiếp.
  - Nắm vững cơ chế Idempotency và Atomic Transaction kết hợp giữa `refund_ledger` và `audit_events` để đảm bảo hệ thống an toàn ngay cả khi gặp sự cố crash đột ngột.
