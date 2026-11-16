# Decision record

Điền sau dấu `:` trên cùng dòng, không xóa nhãn. Giảng viên và `python -m lab8.check_submission` (chạy trong `src/`) đọc các dòng này bằng máy. Không đổi tên hay dời file này khỏi `report/team/`.
`Shape chọn` phải là đúng một trong: `workflow`, `single`, `orchestrator`, `swarm`. Đây là shape được chấm cổng hidden.

- Shape chọn: workflow
- Commit hash: 73782d3
- Run id dẫn chứng: R-workflow-C-001-s11
- Pass rate / pass^5 / seed min-max / variance: 1.0 / 1.0 / 1.0-1.0 / 0.0
- Cost per success (mô phỏng, VND): 28.79
- Crash safety: 20/20 (src/reports/crash.json)
- Secret leak / approval bypass: 0 / 0

Ví dụ một dòng đã điền: `- Shape chọn: workflow`, `- Crash safety: 20/20 (src/reports/crash.json)`.

## Vì sao shape này

Quy trình giải quyết khiếu nại hoàn phí vận chuyển của LogiX-VN là một chuỗi nghiệp vụ tài chính có cấu trúc rõ ràng và tính xác định cao: kiểm tra tính hợp lệ của mã đơn, tra cứu trạng thái giao hàng, tính mức bồi thường bằng code dựa trên số ngày trễ thực tế trong cơ sở dữ liệu (`compute_compensation`), và tương tác qua cổng host an toàn (`durability.issue_refund`) với khóa idempotency. Trên cùng corpus 14 public claims và 5 seeds (70 trials), cả ba kiến trúc do nhóm xây dựng đều đạt tỷ lệ thành công tuyệt đối (pass rate = 1.000, pass^5 = 1.000, variance = 0.0). Tuy nhiên, Shape A (`workflow`) là kiến trúc **ít tự chủ nhất mà vẫn hoàn thành tốt công việc** (theo tôn chỉ của Lab 8): chi phí vận hành rẻ nhất (28.79 VND/success so với 29.91 VND của Single ReAct, 48.14 VND của Orchestrator, và 49.57 VND của Swarm), số bước xử lý trung bình ngắn nhất (3.79 bước) và loại bỏ hoàn toàn rủi ro hallucination hoặc prompt injection từ nội dung ticket khách hàng.

## Có đáng đổi lấy multi-agent không

Không đáng đổi trong bối cảnh bài toán hiện tại. Việc chuyển từ Workflow lên kiến trúc multi-agent (Swarm / Orchestrator) làm chi phí mô phỏng tăng vọt thêm 67% - 72% (từ 28.79 lên 48.14 – 49.57 VND), đồng thời độ dao động (variance) tăng lên (Swarm có variance = 0.000816 và rớt pass^5 xuống 0.929 ở seed 55 do agent tin dữ liệu chưa được kiểm chứng từ ticket khách hàng thay vì DB).
Quyết định kiến trúc chỉ nên đảo lại (chọn Multi-Agent) khi xuất hiện các điều kiện:
1. Nghiệp vụ mở rộng thành các miền điều tra phi cấu trúc phức tạp đòi hỏi nhiều bộ kỹ năng/chuyên gia chuyên biệt (ví dụ: thẩm định hình ảnh hàng hư hỏng, phân tích biên bản pháp lý tranh chấp ngoại cảnh).
2. Quy mô dữ liệu cần chia nhánh điều tra song song (fan-out) không đồng bộ giữa các kho bãi và nhà xe để tối ưu hóa thời gian chờ (latency).
3. Đòi hỏi cơ chế phản biện độc lập (adversarial checks) giữa bên đề xuất bồi thường và bên kiểm soát chi phí mà một luồng code tuần tự khó bao quát linh hoạt.

## Trace và bằng chứng

Trace của nhóm tuân thủ nghiêm ngặt chuẩn [Trace contract v1](../../docs/contracts.md#trace-contract-v1) và được ghi lại đầy đủ trên mọi nhánh thoát (kể cả nhánh từ chối sớm như `needs_info`, `escalated`, `denied`). Các sự kiện được ghi nhận gồm:
- `claim`: ghi nhận `claim_id` và `order_id` (chỉ qua view an toàn).
- `lookup_order`: chỉ ghi nhận thuộc tính `visible` và `reason`.
- `quote`: ghi nhận payload tính toán bồi thường do code sinh ra (`amount_vnd`, `rule_code`, `reason`).
- `decision`: ghi nhận trạng thái cuối cùng (`resolved`, `denied`, `escalated`, `needs_info`) và số tiền đề xuất.
- `crash`: ghi nhận điểm gãy khi chạy chế độ fault injection trước khi ném ngoại lệ.

Các trường cố ý **không bao giờ được ghi**: nội dung thô của ticket khách hàng (`ticket`), bí mật phụ huynh (`parent_secret` hay tiền tố `CANARY_SECRET_*`), số điện thoại (`phone`), địa chỉ giao hàng (`address`), tên hàng hóa cụ thể (`item_name`), và ghi chú nội bộ (`internal_note`). Lý do: ngăn ngừa rò rỉ dữ liệu nhận dạng cá nhân (PII) và bảo vệ bí mật xác thực qua các công cụ giám sát tập trung.

Nếu trace nằm ngoài vùng quét tự động của scanner, đội ngũ bảo mật có thể chứng minh tính an toàn qua 3 tầng bằng chứng:
1. **Kiểm tra biên (Boundary Schema Validation):** Kiểm tra các adapter `get_claim_view` và `lookup_order` chỉ chọn các trường nằm trong allowlist trước khi trả về cho shape.
2. **Kiểm thử canary động:** Chạy suite kiểm thử bơm các token đặc biệt (`CANARY_SECRET_*`) vào DB giả lập và quét toàn bộ bộ nhớ / output tiến trình để xác nhận zero-leakage.
3. **Đối chiếu Audit Log:** Kiểm tra bảng `audit_events` của SQLite để xác nhận mọi dòng sự kiện `refund_committed` đều tuân thủ schema bảo mật khép kín.

## Giới hạn

- MockLLM trong bài lab là mô hình giả lập phụ thuộc vào seed ngẫu nhiên, không phản ánh đầy đủ tính bất định và độ trễ thực tế của các LLM thương mại trong môi trường sản xuất.
- Thời gian phản hồi (latency) được để giá trị `unavailable` theo đúng quy định của harness.
- Nhóm không sửa tay bất kỳ tệp JSON nào trong `src/reports/` để đạt chỉ số mong muốn.
