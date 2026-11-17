# Team

## Thông tin nhóm

- Tên nhóm: 4LU
- Lớp: L3A
- Repo nhóm: `K5-L3A-DAY08-4LU-FromWorkflowsToAgents` (xem [SUBMISSION.md](SUBMISSION.md))
- URL repo: https://github.com/datlt203357/K5-L3A-DAY08-4LU-FromWorkflowsToAgents
- Nhánh nộp và commit chốt: `main`.

## Thành viên

| STT | Họ tên | MSSV | Email | GitHub | Vai trò |
| --: | ------ | ---- | ----- | ------ | ------- |
|   1 | Lê Thành Đạt | 2A202603579 | dat.ltforwork@gmail.com | [datlt203357](https://github.com/datlt203357) | Shape A (workflow) & Integration |
|   2 | Phạm Ngọc Trung Quân | 2A202603626 | trungquana123@gmail.com | [jadenphm29](https://github.com/jadenphm29) | Shape B (single ReAct agent) |
|   3 | Nguyễn Trọng Hưởng | 2A202603607 | nguyentronghuong05@gmail.com | [trongjhuongwr](https://github.com/trongjhuongwr) | Shape C (orchestrator & sanitizing handoff) |
|   4 | Trần Minh Tân | 2A202603688 | minhtantran.contact@gmail.com | [minhtantran99](https://github.com/minhtantran99) | Durability (crash, ledger idempotency) và Benchmark/ADR |

Gợi ý chia vai:

- Nhóm 6 người: integration; workflow; single agent; orchestrator; ledger/policy/crash; eval/report.
- Nhóm 4 người: workflow + integration; single; orchestrator + handoff; ledger + evaluation.

## Bảng đóng góp

`python -m lab8.check_submission` đọc bảng này bằng máy: giữ nguyên tiêu đề `## Bảng đóng góp` và các cột. Mỗi người một dòng: commit có nội dung.

| Người | Vai | Commit | Test đã thêm hoặc sửa |
| --- | --- | --- | --- |
| Lê Thành Đạt | Shape A (workflow) & Integration | 222c63d | tests/test_public_matrix.py (workflow suite) |
| Phạm Ngọc Trung Quân | Shape B (single ReAct agent) | 0cea4f4 | tests/test_single_agent.py |
| Nguyễn Trọng Hưởng | Shape C (orchestrator & sanitizing handoff) | b8ffa27 | tests/test_orchestrator_cases.py |
| Trần Minh Tân | Durability (crash, ledger idempotency) và Benchmark/ADR | 52f14ff | tests/test_refund_idempotency.py |

## Cá nhân

Mỗi thành viên đồng thời tạo một báo cáo riêng trong `report/` theo dạng:

```text
report/team/MSSV_HoTen.md
```

Ví dụ: `report/team/20241234_NguyenVanAn.md`.

Sao chép mục dưới đây cho từng thành viên.

## 2A202603688_TranMinhTan

### Phần việc phụ trách

- Durability: kiểm tra an toàn khi crash và tính idempotency của ledger.
- Benchmark và ADR: chạy benchmark, tổng hợp số liệu và ghi quyết định kiến trúc.

### Đóng góp cụ thể

- Sinh báo cáo crash test 20/20 (`src/reports/crash.json`).
- Bổ sung 3 test case kiểm tra tính bền vững (durability) và idempotency trong `tests/test_refund_idempotency.py`: kiểm tra crash trước effect, crash sau checkpoint và lặp lại replay nhiều lần.
- Chuẩn bị sẵn khung nghiên cứu mini Research Card (`report/team/research_card.md`) theo chủ đề R2 (Failure taxonomy - NeurIPS 2025).

### Bằng chứng

- `src/reports/crash.json` (crash safety 20/20).
- `src/tests/test_refund_idempotency.py` (các hàm test: `test_crash_before_effect_leaves_no_trace_and_resumes`, `test_crash_after_checkpoint_resumes_idempotently`, `test_repeated_sequential_replays_keep_single_row_and_single_audit`).

## 2A202603626_PhamNgocTrungQuan

### Phần việc phụ trách

- Shape B (single ReAct agent).

### Đóng góp cụ thể

- Triển khai Shape B (`src/lab8/shapes/single.py`) với vòng lặp ReAct `max_steps=8` và bảo đảm model chỉ gọi read tools (`worker=True`).
- Gắn kết an toàn với `durability.issue_refund`, truyền quote đầy đủ để host tự trừ trần theo đơn, và truyền `crash_at` không nuốt ngoại lệ `InjectedCrash`.
- Viết bộ test `src/tests/test_single_agent.py` bao gồm 6 nhóm kịch bản kiểm thử: 12 ca public claims, chống hallucination seed 55, chặn tool ghi, chặn step cap, bảo mật trace sạch PII/secret, và crash/idempotency.

### Bằng chứng

- Code: `src/lab8/shapes/single.py`.
- Test: `src/tests/test_single_agent.py` (17/17 passed).
- Test student ma trận: `pytest -q -m student -k single` (62/62 passed).
- Báo cáo chi tiết: `report/team/2A202603626_PhamNgocTrungQuan.md`.

## 202603607_NguyenTrongHuong

### Phần việc phụ trách

- Shape C (orchestrator + read-only investigators) tại `src/lab8/shapes/orchestrator.py`.

### Đóng góp cụ thể

- Hiện thực hóa kiến trúc điều phối Orchestrator tách biệt: điều phối viên cấp cao lập kế hoạch, đóng gói `make_handoff` an toàn (chỉ chứa các read tools: `lookup_order`, `lookup_policy`, `compute_compensation`).
- Đảm bảo cơ chế cách ly tuyệt đối: điều tra viên con không thể truy cập tool ghi tiền, trace không chứa secret/PII từ ticket.
- Gắn cổng an toàn với `durability.issue_refund` và chuyển tiếp `crash_at` không bắt nuốt ngoại lệ `InjectedCrash`.
- Viết bộ test tác giả `src/tests/test_orchestrator_cases.py` (3 test cases kiểm thử cô lập handoff, khấu trừ trần đơn hàng và chặn sai principal_id).

### Bằng chứng

- Code: `src/lab8/shapes/orchestrator.py`.
- Test tác giả: `src/tests/test_orchestrator_cases.py` (3/3 passed).
- Test student ma trận: `pytest -q -m student -k orchestrator` (62/62 passed).
- Báo cáo chi tiết: `report/team/202603607_NguyenTrongHuong.md`.

## 2A202603579_LeThanhDat

### Phần việc phụ trách

- Phụ trách shape `workflow` (Shape A), triển khai luồng xử lý claim cố định bằng Python trong `src/lab8/shapes/workflow.py`.

### Đóng góp cụ thể

- Thay stub `not_implemented` bằng luồng đọc claim qua `get_claim_view`, kiểm tra quyền xem order, tính quote bằng `compute_compensation`, và gọi host `issue_refund` khi quote dương.
- Xử lý các nhánh claim không tồn tại, thiếu order ID, order không hiển thị, quote bằng 0, host từ chối và refund thành công.
- Ghi trace cho các nhánh kết quả; không ghi ticket hay dữ liệu nhạy cảm vào trace.
- Chuyển tiếp `crash_at` tới `issue_refund` và để `InjectedCrash` truyền ra caller, hỗ trợ kiểm thử crash rồi resume.
- Commit chính: chưa ghi nhận.
- Test được thêm hoặc sửa: tests/test_public_matrix.py 

### Bằng chứng

- Test student cho workflow: `python -m pytest -q -m student -o addopts= -k workflow` — **62 passed**.
- Test retry/crash T11 và T12: `python -m pytest -q -m student -o addopts= -k "workflow and (t11 or t12)"` — **2 passed**.
- Cổng host: `python -m pytest -q` — **54 passed, 248 deselected**.
- Crash suite: `python -m lab8.crash_test --count 20 --out reports/crash.json` — **crash_safety 20/20**.
