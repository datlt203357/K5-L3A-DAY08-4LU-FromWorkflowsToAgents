# Team

## Thông tin nhóm

- Tên nhóm:
- Lớp: L3A
- Repo nhóm: `K5-L3A-DAY08-TenNhom-FromWorkflowsToAgents` (xem [SUBMISSION.md](SUBMISSION.md))
- URL repo, nhánh nộp, commit chốt:

## Thành viên

| STT | Họ tên | MSSV | Email | GitHub | Vai trò |
| --: | ------ | ---- | ----- | ------ | ------- |
|   1 | Phạm Ngọc Trung Quân       | 2A202603626     | trungquana123@gmail.com      | https://github.com/jadenphm29       | Shape B (single ReAct agent) |
|   2 | Nguyễn Trọng Hưởng         | 202603607       | nguyentronghuong05@gmail.com | https://github.com/trongjhuongwr    | Shape C (orchestrator) |

Gợi ý chia vai:

- Nhóm 6 người: integration; workflow; single agent; orchestrator; ledger/policy/crash; eval/report.
- Nhóm 4 người: workflow + integration; single; orchestrator + handoff; ledger + evaluation.

## Bảng đóng góp

`python -m lab8.check_submission` đọc bảng này bằng máy: giữ nguyên tiêu đề `## Bảng đóng góp` và các cột. Mỗi người một dòng: commit có nội dung và ít nhất một test đã thêm hoặc sửa.

| Người | Vai | Commit | Test đã thêm hoặc sửa |
| --- | --- | --- | --- |
| Phạm Ngọc Trung Quân | Shape B (single ReAct agent) | quan-branch | tests/test_single_agent.py |
| Nguyễn Trọng Hưởng | Shape C (orchestrator) | feat/shape-orchestrator | tests/test_orchestrator_cases.py |

## Cá nhân

Mỗi thành viên đồng thời tạo một báo cáo riêng trong `report/` theo dạng:

```text
report/team/MSSV_HoTen.md
```

Ví dụ: `report/team/20241234_NguyenVanAn.md`.

Sao chép mục dưới đây cho từng thành viên.

## 202603607_Nguyễn Trọng Hưởng

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

## 2A202603626_Phạm Ngọc Trung Quân

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
