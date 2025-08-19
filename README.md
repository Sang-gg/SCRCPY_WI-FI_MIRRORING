# Scrcpy GUI Tool - Gaming & Movie Modes

Một ứng dụng Python GUI hỗ trợ chạy scrcpy với 2 chế độ tối ưu hóa: **Gaming Mode** (độ trễ thấp) & **Movie/Streaming Mode** (chất lượng cao).

## 🎯 Mục tiêu

- **Gaming Mode**: Ưu tiên độ trễ thấp, giảm buffer, tùy chọn tắt âm thanh
- **Movie/Streaming Mode**: Ưu tiên chất lượng hình ảnh, độ mượt, âm thanh đầy đủ với buffer cao

## 🛠️ Yêu cầu hệ thống

### Phần mềm cần thiết
- **Python 3**
- **Scrcpy** - [Tải tại đây](https://github.com/Genymobile/scrcpy)
- **ADB (Android Debug Bridge)** - [Platform Tools](https://developer.android.com/studio/releases/platform-tools)

### ❗ QUAN TRỌNG: Cách thêm vào biến môi trường (PATH)

Để script có thể gọi `adb.exe` và `scrcpy.exe` từ bất kỳ đâu, bạn cần thêm đường dẫn của chúng vào biến môi trường `PATH` của hệ thống.

1.  Mở **System Properties** (Tìm kiếm "Edit the system environment variables" trong Start Menu).
2.  Chọn **Environment Variables...**.
3.  Trong mục **System variables**, tìm và chọn biến `Path`, sau đó nhấn **Edit...**.
4.  Nhấn **New** và thêm đường dẫn đến thư mục bạn đã giải nén `platform-tools` (ví dụ: `C:\platform-tools`).
5.  Nhấn **New** một lần nữa và thêm đường dẫn đến thư mục `scrcpy` (ví dụ: `C:\scrcpy`).
6.  Nhấn **OK** để lưu lại tất cả các cửa sổ.
7.  Mở một Command Prompt mới và gõ `adb --version` và `scrcpy --version` để kiểm tra. Nếu lệnh chạy mà không báo lỗi là bạn đã thành công.

### Thiết bị Android
- Android 5.0+ (API 21+)
- USB Debugging đã bật
- Wireless Debugging (Android 11+ cho chế độ không dây)

## 🚀 Cách cài đặt và chạy

1. **Tải code**:
   ```bash
   # Lưu file stream.py vào máy
   ```

2. **Cài đặt dependencies**:
   - Cài đặt Python 3
   - Tải và cài scrcpy
   - Tải Android Platform Tools (chứa ADB)
   - Thêm scrcpy và adb vào PATH

3. **Chạy ứng dụng**:
   ```bash
   python stream.py
   ```

## 📱 Các chế độ kết nối

### 1. USB Mode
- Kết nối qua cáp USB
- Ổn định nhất, độ trễ thấp nhất
- Yêu cầu: USB Debugging đã bật

### 2. Pair Mode (Android 11+)
- Kết nối không dây qua Wireless Debugging
- Cần nhập IP, Pair Port, Pair Code
- Tự động thiết lập connection

### 3. Direct IP Mode
- **USB → TCP/IP**: Chuyển từ USB sang không dây
- **Manual IP**: Nhập IP thủ công
- **Network Scan**: Tự động quét mạng LAN

## 🎮 Gaming Mode - Tối ưu cho game

### Quality Presets
- **Ultra Low**: 480p, 2Mbps, 24fps
- **Low**: 720p, 2Mbps, 30fps
- **Medium**: 1024p, 4Mbps, 60fps
- **High**: 1080p, 8Mbps, 90fps
- **Ultra**: 1920p, 16Mbps, 120fps
- **Custom**: Tùy chỉnh theo ý muốn

### Audio Options
- ✅ Có âm thanh (mặc định)
- ❌ Không âm thanh (độ trễ thấp nhất)

### Latency Profiles
- **Ultra Low**: buffer=0ms, H.264
- **Low**: buffer=10ms, H.264
- **Normal**: Cài đặt mặc định
- **Custom**: Tùy chỉnh codec và buffer

### Additional Options
- Show Touches (hiện điểm chạm)
- Record Session (quay màn hình)
- Turn Off Screen (tắt màn hình điện thoại)
- Stay Awake (giữ thức)
- Fullscreen (toàn màn hình)
- Always on Top (luôn ở trên cùng)

## 🎬 Movie Mode - Tối ưu cho phim

### Quality Presets
- **Movie 1080p**: 1920p, 6Mbps, 24fps
- **Cinema Ultra 4K**: 3840p, 16Mbps, 60fps
- **Custom**: Tùy chỉnh chi tiết

### Audio Options (Luôn bật)
- **Codec**: AAC, Opus, FLAC, Raw
- **Bitrate**: 128k (mặc định)
- **Audio Dup**: Cho Android 13+ 

### Quality Profiles
- **Smooth Quality**: buffer=50/100ms, H.265
- **Balanced**: buffer=30/60ms
- **Cinema Ultra**: buffer=200/200ms, H.265/AV1
- **Custom**: Tùy chỉnh hoàn toàn

### Additional Options
- Fullscreen (mặc định bật)
- Record Session (quay phim)
- Always on Top (tùy chọn)

## 📚 Hướng dẫn tích hợp trong ứng dụng

Ứng dụng có **Guide** tích hợp với 4 tab:
1. **Connection Guide**: Hướng dẫn kết nối từng loại
2. **Gaming Tips**: Tối ưu cho gaming
3. **Movie Tips**: Tối ưu cho xem phim
4. **Resources**: Link chính thức và troubleshooting

## 💡 Tips sử dụng

### Cho Gaming
- Dùng USB khi có thể (độ trễ thấp nhất)
- Tắt âm thanh nếu không cần
- Chọn chất lượng Medium/High (tránh Ultra)
- Dùng Wi-Fi 5GHz cho không dây
- Chọn H.264 codec (nhanh nhất)

### Cho Movie/Streaming
- Buffer cao để mượt mà
- H.265 cho chất lượng tốt (nếu hỗ trợ)
- Fullscreen cho trải nghiệm cinema
- Kết nối ổn định cho 4K
- Bitrate cao cho recording

## 🔧 Xử lý lỗi

Ứng dụng tự động:
- Kiểm tra ADB và scrcpy khi khởi động
- Hiển thị lỗi chi tiết và gợi ý fix
- Cảnh báo nếu scrcpy version < 2.0
- Hiện link tải chính thức

## 📁 Cấu trúc code

```
stream.py
├── ScrcpyGUI class
├── Connection methods (USB/Pair/Direct IP)
├── Gaming Mode configuration
├── Movie Mode configuration
├── Command builder & executor
├── Guide system
└── Error handling
```

## 🎨 Giao diện

- **Modern GUI** với tkinter + ttk
- **Multi-frame navigation**
- **Tabbed interface** cho cài đặt chi tiết
- **Real-time status** display
- **Command preview** trước khi chạy

## 🌟 Tính năng đặc biệt

- **Auto device detection**
- **Network scanning**
- **Command preview**
- **Background monitoring**
- **Vietnamese/English support**
- **Thank you message** khi thoát

## 🚨 Lưu ý quan trọng

1. **Phải cài đặt scrcpy và adb trước**
2. **USB Debugging** phải được bật
3. **Cùng mạng** cho kết nối không dây
4. **Firewall** có thể chặn kết nối
5. **Permissions** cần được cấp trên Android

## 📞 Troubleshooting

### Không tìm thấy thiết bị
- Kiểm tra USB Debugging
- Thử cable khác
- Restart ADB: `adb kill-server && adb start-server`

### Kết nối không dây thất bại
- Kiểm tra cùng mạng WiFi
- Thử restart Wireless Debugging
- Kiểm tra firewall

### Scrcpy không chạy
- Cập nhật scrcpy version mới nhất
- Kiểm tra PATH environment
- Thử chạy scrcpy trực tiếp trong terminal

---

**Developed by**: Pan

**Purpose**: Gaming & Movie optimization for scrcpy  
**MIT License**

Chúc bạn có trải nghiệm tuyệt vời với scrcpy! 🎉
