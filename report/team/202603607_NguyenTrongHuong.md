# Báo cáo cá nhân — 202603607_NguyenTrongHuong

## 1. Thông tin thành viên

- Họ tên: Nguyễn Trọng Hưởng
- MSSV: 2A202603607
- Email: nguyentronghuong05@gmail.com
- GitHub: trongjhuongwr

## 2. Phần việc phụ trách

- Chịu trách nhiệm thiết kế, triển khai và kiểm thử Shape C (`orchestrator`): `src/lab8/shapes/orchestrator.py`.
- Thiết lập ranh giới bảo mật cho cơ chế Handoff (`handoff.v1`) và điều phối điều tra viên chỉ đọc (`run_readonly_investigators`).
- Xây dựng bộ kiểm thử đơn vị độc lập cho Shape C: `src/tests/test_orchestrator_cases.py`.
- Đảm bảo Shape C tuân thủ đầy đủ 3 điều kiện must-pass (không bypass approval, không lộ secret/PII, chịu lỗi crash).

## 3. Đóng góp cụ thể

- **Triển khai `src/lab8/shapes/orchestrator.py`**:
  - Tách bạch vai trò: Orchestrator dùng MockLLM phân tích ticket và lập kế hoạch cấp cao (`purpose="orchestrator_plan"`), không để model can thiệp vào việc tính tiền hay duyệt bồi thường.
  - Xử lý các nhánh trả về sớm: Kiểm tra mã đơn hàng bị thiếu (`needs_info`), đơn hàng không khả kiến hoặc thuộc quyền sở hữu của khách hàng khác (`escalated`) mà không để lộ PII (SĐT, địa chỉ, tên hàng hóa).
  - Đóng gói gói bàn giao điều tra bằng `make_handoff`: Tuân thủ nghiêm ngặt chuẩn `handoff.v1`, chỉ cho phép các trường facts trong allowlist (`FACT_KEYS`) và các tool đọc (`lookup_order`, `lookup_policy`, `compute_compensation`). Loại bỏ hoàn toàn `parent_secret` (`CANARY_SECRET_*`) và `raw_headers`.
  - Phân quyền điều tra viên: Chạy `run_readonly_investigators` với worker context chỉ đọc, cô lập quyền hạn thực thi.
  - Bồi hoàn theo trần đơn hàng: Trích xuất quote đầy đủ từ kết quả điều tra và gọi host `durability.issue_refund(conn, claim_id, proposal, crash_at=crash_at)`. Để host tự khấu trừ khoản tiền đã bồi hoàn trước đó (case T14), không tự trừ trước ở tầng shape.
  - Hỗ trợ kiểm thử chịu lỗi (CP3): Bắt ngoại lệ `InjectedCrash`, ghi nhận sự kiện vào file trace (`trace.add("crash", ...)`), gọi `trace.write()` rồi re-raise để hệ thống host kiểm chứng tính lũy đọng.
- **Xây dựng bộ test `src/tests/test_orchestrator_cases.py`**:
  - `test_orchestrator_handoff_has_no_secrets`: Quét trực tiếp file trace JSON sau khi chạy claim C-010, xác nhận 100% không chứa `CANARY_SECRET_`, không chứa `parent_secret`, và gói handoff chỉ chứa danh mục tool đọc.
  - `test_orchestrator_partial_difference_on_prior_refund`: Kiểm thử case T14 trên đơn O-515 (đã nhận 30.000đ tiền ship trước đó), xác nhận orchestrator đề xuất quote đầy đủ 150.000đ và host ghi nhận đúng 120.000đ tiền chênh lệch vào sổ cái.
  - `test_orchestrator_outside_principal_scope_escalates`: Kiểm thử case T05 khi khách truy cập đơn của người khác, xác nhận hệ thống trả về `escalated` và proposal_amount = 0.

## 4. Bằng chứng

- File mã nguồn: `src/lab8/shapes/orchestrator.py`
- File unit test: `src/tests/test_orchestrator_cases.py` (3/3 test pass)
- Kết quả kiểm thử ma trận student: `pytest -q -m student -o addopts= -k orchestrator` (62/62 test pass trên 5 seeds)
- Kết quả kiểm thử host: `pytest -q` (57 test pass)
- Run id minh chứng: `R-orchestrator-C-001-s11`

## 5. Công cụ AI đã dùng

- **Công cụ**: Antigravity AI Assistant.
- **Nội dung sử dụng**: Tra cứu cấu trúc chuẩn của hợp đồng `handoff.v1` trong module `lab8.handoff` và rà soát các trường trong allowlist của `Trace contract v1`.
- **Cách tự kiểm tra**:
  - Chạy test tự động trực tiếp trên terminal môi trường ảo:
    + `python -m pytest -q tests/test_orchestrator_cases.py` (3 passed)
    + `python -m pytest -q -m student -o addopts= -k orchestrator` (62 passed)
  - Mở đọc trực tiếp tệp JSON sinh ra trong `traces/` để đối soát thủ công, đảm bảo các trường nhạy cảm (`parent_secret`, `phone`, `address`, `internal_note`) không tồn tại.

## 6. Tự đánh giá

- Hoàn thành đầy đủ 100% yêu cầu kỹ thuật của Shape C theo các mốc CP2 và CP3.
- Bảo vệ trọn vẹn 3 điều kiện must-pass của lab.
- Điểm tự đánh giá: 10/10.
