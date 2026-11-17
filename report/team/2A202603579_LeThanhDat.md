# Báo cáo cá nhân — Lê Thành Đạt - 2A202603579

## 1. Thông tin thành viên

- Họ tên: Lê Thành Đạt
- MSSV: 2A202603579
- Email: 26ai.datlt7@vinuni.edu.vn
- GitHub: https://github.com/datlt203357

## 2. Phần việc phụ trách

- Phụ trách shape `workflow` (Shape A), triển khai luồng xử lý claim cố định bằng Python trong `src/lab8/shapes/workflow.py`.

## 3. Đóng góp cụ thể

- Thay stub `not_implemented` bằng luồng đọc claim qua `get_claim_view`, kiểm tra quyền xem order, tính quote bằng `compute_compensation`, và gọi host `issue_refund` khi quote dương.
- Xử lý các nhánh claim không tồn tại, thiếu order ID, order không hiển thị, quote bằng 0, host từ chối và refund thành công.
- Ghi trace cho các nhánh kết quả; không ghi ticket hay dữ liệu nhạy cảm vào trace.
- Chuyển tiếp `crash_at` tới `issue_refund` và để `InjectedCrash` truyền ra caller, hỗ trợ kiểm thử crash rồi resume.
- Commit chính: chưa ghi nhận.
- Test được thêm hoặc sửa: tests/test_public_matrix.py 

## 4. Bằng chứng

- Test student cho workflow: `python -m pytest -q -m student -o addopts= -k workflow` — **62 passed**.
- Test retry/crash T11 và T12: `python -m pytest -q -m student -o addopts= -k "workflow and (t11 or t12)"` — **2 passed**.
- Cổng host: `python -m pytest -q` — **54 passed, 248 deselected**.
- Crash suite: `python -m lab8.crash_test --count 20 --out reports/crash.json` — **crash_safety 20/20**.

## 5. Công cụ AI đã dùng

- Dùng trợ lý AI để giải thích yêu cầu CP2/CP3, hỗ trợ triển khai shape `workflow` và diễn giải các lệnh kiểm tra.
- Tự kiểm tra bằng cách chạy bộ test student của workflow, riêng T11/T12, cổng host và crash suite; các kết quả được ghi ở mục 4.

## 6. Tự đánh giá

Đã hoàn thành và kiểm tra CP2/CP3 cho shape `workflow`. Phần tiếp theo là phối hợp tích hợp với các shape còn lại và ghi nhận commit kỹ thuật theo yêu cầu nộp bài.
