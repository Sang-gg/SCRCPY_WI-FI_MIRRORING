# Script Hỗ Trợ Scrcpy qua WiFi (Tối ưu Độ trễ Thấp)

Đây là một script Windows Batch (`.bat`) giúp đơn giản hóa việc kết nối và trình chiếu màn hình điện thoại Android lên máy tính bằng [Scrcpy](https://github.com/Genymobile/scrcpy) thông qua kết nối WiFi. Script cung cấp một giao diện menu dòng lệnh trực quan để lựa chọn các chế độ kết nối, thiết lập chất lượng và các tùy chọn nâng cao để giảm độ trễ khi chơi game.

## ✨ Tính năng nổi bật

* **Giao diện Menu trực quan**: Không cần nhớ các lệnh phức tạp, chỉ cần chọn từ menu.
* **Nhiều chế độ kết nối**:
    * [span_0](start_span)[span_1](start_span)Tự động kích hoạt WiFi qua USB (cho Android 10 trở xuống)[span_0](end_span)[span_1](end_span).
    * [span_2](start_span)Hỗ trợ ghép cặp qua mã QR cho "Wireless Debugging" (Android 11 trở lên)[span_2](end_span).
    * [span_3](start_span)Kết nối trực tiếp nếu đã biết IP[span_3](end_span).
* **[span_4](start_span)Cài đặt sẵn chất lượng**: Dễ dàng chọn giữa các mức chất lượng từ Thấp đến Siêu cao[span_4](end_span).
* **Tối ưu cho Gaming**: Tùy chọn nâng cao để chọn encoder phần cứng và tắt âm thanh nhằm giảm độ trễ tối đa.
* **[span_5](start_span)Hướng dẫn tích hợp**: Có sẵn mục hướng dẫn chi tiết ngay trong script[span_5](end_span).

## ⚙️ Yêu cầu cài đặt

Trước khi sử dụng script, bạn **BẮT BUỘC** phải cài đặt và cấu hình hai công cụ sau:

1.  **ADB (Android Debug Bridge)**
    * **Tải về**: Tải gói **SDK Platform-Tools for Windows** từ trang chủ của Android: [https://developer.android.com/studio/releases/platform-tools](https://developer.android.com/studio/releases/platform-tools)
    * **Cài đặt**: Giải nén file zip vừa tải về (ví dụ: vào `C:\platform-tools`).

2.  **Scrcpy**
    * **Tải về**: Tải phiên bản mới nhất cho Windows từ trang GitHub của Scrcpy: [https://github.com/Genymobile/scrcpy/releases](https://github.com/Genymobile/scrcpy/releases)
    * **Cài đặt**: Giải nén file zip vừa tải về (ví dụ: vào `C:\scrcpy`).

### ❗ QUAN TRỌNG: Thêm vào biến môi trường (PATH)

Để script có thể gọi `adb.exe` và `scrcpy.exe` từ bất kỳ đâu, bạn cần thêm đường dẫn của chúng vào biến môi trường `PATH` của hệ thống.

1.  Mở **System Properties** (Tìm kiếm "Edit the system environment variables" trong Start Menu).
2.  Chọn **Environment Variables...**.
3.  Trong mục **System variables**, tìm và chọn biến `Path`, sau đó nhấn **Edit...**.
4.  Nhấn **New** và thêm đường dẫn đến thư mục bạn đã giải nén `platform-tools` (ví dụ: `C:\platform-tools`).
5.  Nhấn **New** một lần nữa và thêm đường dẫn đến thư mục `scrcpy` (ví dụ: `C:\scrcpy`).
6.  Nhấn **OK** để lưu lại tất cả các cửa sổ.
7.  Mở một Command Prompt mới và gõ `adb --version` và `scrcpy --version` để kiểm tra. Nếu lệnh chạy mà không báo lỗi là bạn đã thành công.

## 🚀 Hướng dẫn sử dụng

1.  **Tải script**: Tải file `stream.bat` này về máy tính của bạn.
2.  **Chạy script**: Nháy đúp chuột vào file `stream.bat` để khởi chạy menu.
3.  **Bật Gỡ lỗi USB trên điện thoại**:
    * Vào `Settings` > `About phone` > Gõ 7 lần vào `Build number` để bật `Developer options`.
    * Vào `Developer options`, bật `USB debugging`.
    * Đối với Android 11+, bật thêm `Wireless debugging`.

### Các chế độ kết nối

* **[span_6](start_span)[1] USB Debug (Android <=10)**[span_6](end_span)
    * Cắm điện thoại vào PC qua cáp USB.
    * Chọn chế độ này, script sẽ tự động kích hoạt ADB qua TCP/IP và tìm IP của điện thoại.
    * Sau khi kết nối thành công, bạn có thể rút cáp USB.

* **[span_7](start_span)[2] Wireless Debugging (Android 11+)**[span_7](end_span)
    * Trên điện thoại, vào `Developer options` > `Wireless debugging`.
    * Chọn `Pair device with pairing code`.
    * Nhập `Host:Port` và `Pairing code` hiển thị trên điện thoại vào script.
    * Sau đó, nhập `IP:Port` chính (thường là port 5555) để kết nối.

* **[span_8](start_span)[3] Kết nối trực tiếp**[span_8](end_span)
    * Sử dụng khi bạn đã biết chính xác địa chỉ IP và cổng của điện thoại.
    * Chỉ cần nhập `IP:PORT` và kết nối.

### 🎮 Tối ưu cho Gaming (Độ trễ thấp)

Để có trải nghiệm stream game FPS mượt mà nhất, script cung cấp các tùy chọn nâng cao:

1.  **Chọn Encoder Phần cứng**:
    * Sau khi chọn chế độ kết nối, script sẽ hỏi bạn về `Tùy chọn Nâng cao`.
    * Bạn có thể chọn **[L] Liet ke cac encoder** để xem danh sách các bộ mã hóa video mà điện thoại hỗ trợ.
    * Hãy ưu tiên chọn các encoder có tên của nhà sản xuất chip (`qcom`, `exynos`, `mediatek`) thay vì `google` hay `android` để có hiệu năng cao nhất.
    * Chọn **[2] Hieu nang cao** và nhập tên encoder bạn muốn sử dụng.

2.  **Tắt âm thanh**:
    * Trước khi chạy scrcpy, script sẽ hỏi bạn có muốn truyền âm thanh không.
    * Chọn **'n' (không)** sẽ giúp giảm thêm một chút độ trễ, vì máy không phải xử lý luồng âm thanh.

## 👨‍💻 Báo lỗi

* **[span_9](start_span)GitHub**: github.com/Sang-gg/SCRCPY_WI-FI_MIRRORING[span_9](end_span)
* **[span_10](start_span)Telegram**: @SACLB9F[span_10](end_span)

Chúc bạn có trải nghiệm tốt nhất!
