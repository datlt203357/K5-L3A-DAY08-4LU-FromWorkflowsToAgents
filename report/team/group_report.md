# Báo cáo nhóm — Lab 8 LogiX-VN

Tối đa 5 trang ngoài phụ lục. Số liệu lấy từ file trong `src/reports/`, không chép tay từ terminal.

## 1. Thông tin nhóm

- Tên nhóm: 4LU
- Lớp: L3A
- Repo: `https://github.com/datlt203357/K5-L3A-DAY08-4LU-FromWorkflowsToAgents`
- Nhánh làm việc và nộp: `main`
- Commit chốt (trùng `report/team/decision_adr.md`): `73782d3`
- Thành viên: xem [TEAM.md](../../TEAM.md)

## 2. Mục tiêu và cách tiếp cận

Bài toán yêu cầu xây dựng và đối chiếu hệ thống xử lý khiếu nại (claim) hoàn phí vận chuyển cho công ty giả lập LogiX-VN trên bốn kiến trúc khác nhau:
1. **Shape A — Workflow**: Quy trình code tuần tự, logic nghiệp vụ xác định bằng Python.
2. **Shape B — Single ReAct Agent**: Vòng lặp suy luận ReAct (`max_steps=8`), model chỉ đóng vai trò mắt đọc (`worker=True`).
3. **Shape C — Orchestrator**: Kiến trúc điều phối phân tầng, cô lập gói chuyển giao (sanitized handoff) và các điều tra viên chỉ đọc.
4. **Shape D — Swarm (tham chiếu)**: Mô hình swarm phân tán có sẵn để đối chứng độ lệch và chi phí.

Nguyên tắc bất biến của hệ thống: **Code quyết định tiền và phê duyệt (Host Gate); Model chỉ đọc dữ liệu và soạn thảo phản hồi**. Mọi thao tác ghi sổ cái đều phải đảm bảo tính lũy đọng (idempotency key `refund:{claim_id}`) và chống mất an toàn khi tiến trình bị sập đột ngột (crash-resilient durability).

Nhóm tiếp cận theo phương pháp phát triển song song kết hợp TDD:
- Thành viên 4 thiết lập bộ kiểm thử Durability, Idempotency và sinh báo cáo crash safety 20/20.
- Thành viên 1, 2, 3 độc lập xây dựng Shape A, B, C trên các nhánh riêng (`LeThanhDat-branch`, `quan-branch`, `feat/shape-orchestrator`).
- Sau khi từng shape hoàn thiện và vượt qua bộ test ma trận riêng, toàn bộ nhánh được tích hợp về `main` để tiến hành benchmark đồng bộ trên 14 claims và 5 seeds.

## 3. Giải pháp

### Ranh giới Code / Model & An toàn Giao dịch
- **Shape A (Workflow)**: Đọc claim qua view an toàn `get_claim_view`, tra cứu đơn hàng bằng `lookup_order`. Mức bồi thường được tính trực tiếp bằng hàm thuần túy `compute_compensation`. Host là đơn vị duy nhất ghi sổ qua `durability.issue_refund`.
- **Shape B (Single Agent)**: Hiện thực hóa vòng ReAct với bộ công cụ chỉ đọc `READONLY_TOOLS`. Model tương tác qua `MockLLM` để tìm dữ kiện, nhưng không được cấp quyền gọi lệnh ghi hay tự quyết định số tiền. Sau khi ReAct kết thúc, code shape tiếp quản và chuyển quote đầy đủ sang host.
- **Shape C (Orchestrator)**: Orchestrator lập kế hoạch cấp cao, sử dụng `make_handoff` để đóng gói dữ kiện. Handoff chỉ chứa các trường trong allowlist (`FACT_KEYS`) và read-only tools, loại bỏ hoàn toàn `parent_secret` (`CANARY_SECRET_*`) hay thông tin nhạy cảm. Dispatching qua `run_readonly_investigators`.
- **Durability & Crash Resilience**: Tất cả các shape khi gọi `durability.issue_refund(conn, claim_id, proposal, crash_at=crash_at)` đều chuyển tiếp tham số `crash_at` và không nuốt ngoại lệ `InjectedCrash`. Khi crash xảy ra trước hoặc sau checkpoint, cơ chế giao dịch nguyên tử (atomic transaction) kết hợp giữa `refund_ledger` và `audit_events` bảo đảm khi resume lại hệ thống nhận diện `idempotent_replay`, không bao giờ sinh ra dòng hoàn tiền thứ hai.

## 4. Kết quả

### Bảng đối chiếu Benchmark (trích xuất từ `src/reports/benchmark.json`)

Tập dữ liệu: 14 claims public × 5 seeds (11, 22, 33, 44, 55) = 70 trials mỗi kiến trúc.

| Shape | Pass rate | Pass^5 | Seed Variance | Min | Max | Cost / Success (VND) | Mean Steps |
|---|---:|---:|---:|---:|---:|---:|---:|
| **Workflow (Shape A)** | **1.000** | **1.000** | **0.000000** | **1.000** | **1.000** | **28.79** | **3.79** |
| **Single (Shape B)** | **1.000** | **1.000** | **0.000000** | **1.000** | **1.000** | **29.91** | **6.57** |
| **Orchestrator (Shape C)** | **1.000** | **1.000** | **0.000000** | **1.000** | **1.000** | **48.14** | **2.79** |
| **Swarm (Shape D - ref)** | 0.986 | 0.929 | 0.000816 | 0.929 | 1.000 | 49.57 | 2.80 |

### Đánh giá An toàn Bền vững (Crash & Security)
- **Crash Safety**: Đạt tuyệt đối **20/20** kịch bản tại các mốc `before_effect`, `after_effect_before_checkpoint`, và `after_checkpoint` (minh chứng: [src/reports/crash.json](../../src/reports/crash.json)).
- **Secret & PII Leak**: **0** rò rỉ secret (`secret_leak_count = 0`), **0** bypass phê duyệt (`approval_bypass_count = 0`).
- **Phủ kiểm thử tự động**: 100% test suites vượt qua với **322 passed** (bao gồm 74 test host gates và 248 test ma trận student).

Quyết định kiến trúc chi tiết: xem [report/team/decision_adr.md](decision_adr.md).  
Nghiên cứu suy thoái Multi-Agent (R2 - MAST Taxonomy): xem [report/team/research_card.md](research_card.md).

## 5. Khó khăn và cách xử lý

1. **Lỗi phân quyền thư mục Temp trên Windows (PermissionError [WinError 5])**:
   - *Triệu chứng*: Khi chạy `pytest`, Windows chặn quyền truy cập vào `C:\Users\Admin\AppData\Local\Temp\pytest-of-Admin`.
   - *Xử lý*: Điều hướng biến môi trường tạm sang thư mục dự án `$env:TEMP="E:\LAB8\tmp"; $env:TMP="E:\LAB8\tmp"` trong PowerShell, giúp pytest chạy mượt mà mà không phụ thuộc quyền Admin.
2. **Xung đột tích hợp khi merge đa nhánh (Git Merge Conflict)**:
   - *Triệu chứng*: Cả ba thành viên ban đầu đều có điều chỉnh trong `workflow.py`, `orchestrator.py` và `TEAM.md`.
   - *Xử lý*: Phân định rõ trách nhiệm theo đúng vai trò được giao trong `TEAM.md`, giữ bản chuẩn của từng tác giả tương ứng cho Shape A, B, C; sau đó gộp chung bảng đóng góp trong `TEAM.md` và chạy kiểm thử toàn diện `pytest -q -o addopts=` để xác thực không phát sinh lỗi hồi quy.

## 6. Tổng hợp đóng góp

| Thành viên | MSSV | Vai trò chính | Đóng góp cốt lõi |
|---|---|---|---|
| Lê Thành Đạt | 203357 | Shape A & Integration | Triển khai Shape A Workflow tuần tự; cấu hình cổng gọi host bồi hoàn. |
| Phạm Ngọc Trung Quân | 2A202603626 | Shape B (Single Agent) | Triển khai Shape B ReAct (`max_steps=8`); viết bộ test `test_single_agent.py`. |
| Nguyễn Trọng Hưởng | 2A202603607 | Shape C (Orchestrator) | Triển khai Shape C Orchestrator & Handoff sanitization; viết bộ test `test_orchestrator_cases.py`. |
| Trần Minh Tân | 2A202603688 | Durability & Benchmark/ADR | Xây dựng test case Idempotency/Crash; chạy crash suite 20/20, Benchmark 4 shape và hoàn thiện ADR/Research Card. |

Chi tiết tại [TEAM.md](../../TEAM.md) và các file báo cáo cá nhân tương ứng trong thư mục `report/team/`.

## 7. Hạn chế và hướng cải thiện

- **Mô phỏng MockLLM**: MockLLM trong bài thực hành là mô hình giả lập phụ thuộc vào hạt giống ngẫu nhiên (seed), chưa mô phỏng được tính đa nghĩa phức tạp và độ trễ ngẫu nhiên của các mô hình LLM lớn thương mại (GPT-4o, Gemini 1.5 Pro).
- **Phạm vi mở rộng**: Trong tương lai, khi quy trình bồi hoàn mở rộng thêm việc phân loại hình ảnh hóa đơn hoặc thẩm định hợp đồng đa ngôn ngữ, hệ thống có thể kết hợp kiến trúc lai (Hybrid Workflow-Agent): giữ Workflow làm xương sống kiểm soát dòng tiền, chỉ nhúng Agent tại các trạm trích xuất thông tin phi cấu trúc.

## 8. Tài liệu tham khảo

1. *Towards a Science of Scaling Agent Systems*, Google Research, 2026.
2. *Why Do Multi-Agent LLM Systems Fail?*, MAST, NeurIPS 2025 (arXiv:2501.06830).
3. *Trace contract v1 & Business rules*, Tài liệu hướng dẫn môn học Lab 8 LogiX-VN, 2026.
