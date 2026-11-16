# Báo cáo cá nhân — 203357_LeThanhDat

## 1. Thông tin thành viên

- Họ tên: Lê Thành Đạt
- MSSV: 203357
- Email: dat.ltforwork@gmail.com
- GitHub: https://github.com/datlt203357

## 2. Phần việc phụ trách

- **Kiến trúc đảm nhiệm:** Shape A (`workflow` — Deterministic Workflow) tại `src/lab8/shapes/workflow.py`.
- **Nghiệp vụ cốt lõi:** Hiện thực hóa quy trình xử lý claim cố định, thuần code Python; tính toán tiền bồi hoàn bằng `compute_compensation` dựa trên dữ liệu order thay vì tin vào văn bản ticket người dùng.
- **Tích hợp Host Gate:** Kết nối an toàn với cổng `durability.issue_refund`, truyền quote đầy đủ để host tự khấu trừ theo trần đơn hàng (per-order cap) và chuyển tiếp `crash_at`.

## 3. Đóng góp cụ thể

- Triển khai toàn bộ quy trình của Shape A trong `src/lab8/shapes/workflow.py`:
  + Đọc claim an toàn qua `get_claim_view`, trả về `needs_info` nếu thiếu `order_id`.
  + Tra cứu đơn hàng qua `lookup_order`, trả về `escalated` nếu đơn hàng không khả kiến với principal.
  + Tính toán mức bồi hoàn từ thông tin đơn hàng bằng `compute_compensation`.
  + Gọi host `durability.issue_refund(conn, claim_id, proposal, crash_at=crash_at)` với quote đầy đủ và không nuốt `InjectedCrash`.
  + Đảm bảo Trace contract v1 ghi nhận đúng mọi nhánh trả về (`resolved`, `denied`, `escalated`, `needs_info`, `failed`) và không rò rỉ secret/PII.

## 4. Bằng chứng

- File code: `src/lab8/shapes/workflow.py`.
- Commit kỹ thuật: `222c63d` ("update workflow") trên nhánh `LeThanhDat-branch`.
- Kết quả kiểm thử ma trận: Vượt qua 62/62 test student của workflow (`python -m pytest -q -m student -k workflow`).
- Kết quả benchmark: Pass rate = 1.000, Pass^5 = 1.000, Variance = 0.0, Cost/success = 28.79 VND (thấp nhất trong 4 shape).

## 5. Công cụ AI đã dùng

- Trợ lý AI hỗ trợ rà soát luồng điều kiện biên theo [docs/business_rules.md](../../docs/business_rules.md).
- Tự kiểm tra kết quả qua `python -m pytest -q -m student -k workflow`.

## 6. Tự đánh giá

- Hoàn thành 100% nhiệm vụ được giao cho Shape A.
