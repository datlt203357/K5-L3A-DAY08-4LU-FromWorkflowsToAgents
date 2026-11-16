# Team

## Thông tin nhóm

- Tên nhóm: 4LU
- Lớp: L3A
- Repo nhóm: `K5-L3A-DAY08-4LU-FromWorkflowsToAgents` (xem [SUBMISSION.md](SUBMISSION.md))
- URL repo: https://github.com/datlt203357/K5-L3A-DAY08-4LU-FromWorkflowsToAgents
- Nhánh làm việc: `tan_branch`; nhánh nộp và commit chốt: chưa xác định.

## Thành viên

| STT | Họ tên | MSSV | Email | GitHub | Vai trò |
| --: | ------ | ---- | ----- | ------ | ------- |
|   1 | Trần Minh Tân | 2A202603688 | minhtantran.contact@gmail.com | [minhtantran99](https://github.com/minhtantran99) | Durability (crash, ledger idempotency) và Benchmark/ADR |
|   2 |        |      |       |        |         |

Gợi ý chia vai:

- Nhóm 6 người: integration; workflow; single agent; orchestrator; ledger/policy/crash; eval/report.
- Nhóm 4 người: workflow + integration; single; orchestrator + handoff; ledger + evaluation.

## Bảng đóng góp

`python -m lab8.check_submission` đọc bảng này bằng máy: giữ nguyên tiêu đề `## Bảng đóng góp` và các cột. Mỗi người một dòng: commit có nội dung và ít nhất một test đã thêm hoặc sửa.

| Người | Vai | Commit | Test đã thêm hoặc sửa |
| --- | --- | --- | --- |
| Trần Minh Tân | Durability (crash, ledger idempotency) và Benchmark/ADR | 89d6275 | tests/test_refund_idempotency.py (thêm 3 test kiểm tra crash before/after checkpoint và replay idempotency) |

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
