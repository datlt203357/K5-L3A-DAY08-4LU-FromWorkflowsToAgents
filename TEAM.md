# Team

## Thông tin nhóm

- Tên nhóm: 4LU
- Lớp: L3A
- Repo nhóm: `K5-L3A-DAY08-4LU-FromWorkflowsToAgents` (xem [SUBMISSION.md](SUBMISSION.md))
- URL repo: https://github.com/datlt203357/K5-L3A-DAY08-4LU-FromWorkflowsToAgents
- Nhánh làm việc: `main`; nhánh nộp và commit chốt: `main`.

## Thành viên

| STT | Họ tên | MSSV | Email | GitHub | Vai trò |
| --: | ------ | ---- | ----- | ------ | ------- |
|   1 | Lê Thành Đạt | 203357 | dat.ltforwork@gmail.com | [datlt203357](https://github.com/datlt203357) | Shape A (workflow) & Integration |
|   2 | Phạm Ngọc Trung Quân | 2A202603626 | trungquana123@gmail.com | [jadenphm29](https://github.com/jadenphm29) | Shape B (single ReAct agent) |
|   3 | Nguyễn Trọng Hưởng | 2A202603607 | nguyentronghuong05@gmail.com | [trongjhuongwr](https://github.com/trongjhuongwr) | Shape C (orchestrator & sanitizing handoff) |
|   4 | Trần Minh Tân | 2A202603688 | minhtantran.contact@gmail.com | [minhtantran99](https://github.com/minhtantran99) | Durability (crash, ledger idempotency) và Benchmark/ADR |

Gợi ý chia vai:

- Nhóm 6 người: integration; workflow; single agent; orchestrator; ledger/policy/crash; eval/report.
- Nhóm 4 người: workflow + integration; single; orchestrator + handoff; ledger + evaluation.

## Bảng đóng góp

`python -m lab8.check_submission` đọc bảng này bằng máy: giữ nguyên tiêu đề `## Bảng đóng góp` và các cột. Mỗi người một dòng: commit có nội dung và ít nhất một test đã thêm hoặc sửa.

| Người | Vai | Commit | Test đã thêm hoặc sửa |
| --- | --- | --- | --- |
| Lê Thành Đạt | Shape A (workflow) & Integration | 222c63d | tests/test_public_matrix.py (workflow suite) |
| Phạm Ngọc Trung Quân | Shape B (single ReAct agent) | 0cea4f4 | tests/test_single_agent.py |
| Nguyễn Trọng Hưởng | Shape C (orchestrator & sanitizing handoff) | b8ffa27 | tests/test_orchestrator_cases.py |
| Trần Minh Tân | Durability (crash, ledger idempotency) và Benchmark/ADR | 52f14ff | tests/test_refund_idempotency.py (thêm 3 test kiểm tra crash before/after checkpoint và replay idempotency) |

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

## 2A202603607_NguyenTrongHuong

### Phần việc phụ trách

- Shape C (orchestrator & sanitizing handoff).

### Đóng góp cụ thể

- Triển khai Shape C (`src/lab8/shapes/orchestrator.py`) với vai trò điều phối, tách rời hoàn toàn quyền hạn giữa orchestrator và investigators.
- Đóng gói gói bàn giao điều tra qua `make_handoff` tuân thủ nghiêm ngặt allowlist facts và read-only tools, khử 100% secret/PII.
- Viết bộ test kiểm thử `src/tests/test_orchestrator_cases.py` cho handoff isolation, phân quyền đơn hàng và khấu trừ hoàn tiền từng phần.

### Bằng chứng

- Code: `src/lab8/shapes/orchestrator.py`.
- Test: `src/tests/test_orchestrator_cases.py` (3/3 passed).
- Báo cáo chi tiết: `report/team/202603607_NguyenTrongHuong.md`.

## LeThanhDat

### Phần việc phụ trách

- Shape A (workflow) & Integration.

### Đóng góp cụ thể

- Triển khai Shape A (`src/lab8/shapes/workflow.py`) giải quyết tuần tự các bước xử lý claim cố định.
- Tích hợp cổng host `durability.issue_refund` với quote đầy đủ và chuyển tiếp `crash_at`.

### Bằng chứng

- Code: `src/lab8/shapes/workflow.py`.
