import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import subprocess
import threading
import re
import sys
import time
import socket
from pathlib import Path

class ScrcpyGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Scrcpy GUI Tool - Gaming & Movie Modes")
        self.root.geometry("800x600")
        self.root.resizable(True, True)

        # Variables
        self.current_device = ""
        self.scrcpy_process = None
        self.current_frame = None

        # Check dependencies at startup
        self.check_dependencies()

        # Initialize main menu
        self.show_main_menu()

    def check_dependencies(self):
        """Check if adb and scrcpy are available"""
        missing = []

        # Check ADB
        try:
            subprocess.run(['adb', 'version'], 
                         capture_output=True, check=True, timeout=5)
        except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
            missing.append("adb")

        # Check scrcpy
        try:
            result = subprocess.run(['scrcpy', '--version'], 
                                  capture_output=True, check=True, timeout=5, text=True)
            # Check version
            version_match = re.search(r'scrcpy\s+(\d+\.\d+)', result.stdout)
            if version_match:
                version = float(version_match.group(1))
                if version < 2.0:
                    messagebox.showwarning("Cảnh báo phiên bản", 
                                         f"Phát hiện scrcpy phiên bản {version}. Một số tính năng âm thanh yêu cầu từ v2.0 trở lên.")
        except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
            missing.append("scrcpy")

        if missing:
            msg = f"Thiếu phần phụ thuộc: {', '.join(missing)}\n\n"
            msg += "Vui lòng cài đặt:\n"
            msg += "• scrcpy: https://github.com/Genymobile/scrcpy\n"
            msg += "• adb (platform-tools): https://developer.android.com/studio/releases/platform-tools"
            messagebox.showerror("Thiếu phụ thuộc", msg)

    def clear_frame(self):
        """Clear current frame"""
        if self.current_frame:
            self.current_frame.destroy()

    def show_main_menu(self):
        """Show main menu"""
        self.clear_frame()
        self.current_frame = ttk.Frame(self.root)
        self.current_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Title
        title_label = ttk.Label(self.current_frame, text="Scrcpy GUI Tool by Pan", 
                               font=("Arial", 18, "bold"))
        title_label.pack(pady=20)

        subtitle = ttk.Label(self.current_frame, 
                           text="Gaming Mode: Độ trễ thấp | Movie Mode: Chất lượng cao",
                           font=("Arial", 10))
        subtitle.pack(pady=5)

        # Menu buttons
        button_frame = ttk.Frame(self.current_frame)
        button_frame.pack(pady=20)

        ttk.Button(button_frame, text="[1] Chế độ USB", 
                  command=self.show_usb_mode, width=20).pack(pady=5)
        ttk.Button(button_frame, text="[2] Chế độ ghép nối (Gỡ lỗi không dây)", 
                  command=self.show_pair_mode, width=20).pack(pady=5)
        ttk.Button(button_frame, text="[3] Chế độ IP trực tiếp", 
                  command=self.show_direct_ip_mode, width=20).pack(pady=5)
        ttk.Button(button_frame, text="[4] Hướng dẫn", 
                  command=self.show_guide, width=20).pack(pady=5)
        ttk.Button(button_frame, text="[0] Thoát", 
                  command=self.exit_app, width=20).pack(pady=5)

    def show_usb_mode(self):
        """USB Mode Frame"""
        self.clear_frame()
        self.current_frame = ttk.Frame(self.root)
        self.current_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        ttk.Label(self.current_frame, text="Chế độ USB", 
                 font=("Arial", 16, "bold")).pack(pady=10)

        # Status text
        self.status_text = tk.Text(self.current_frame, height=8, width=70)
        self.status_text.pack(pady=10)

        # Check devices
        ttk.Button(self.current_frame, text="Check USB Devices", 
                  command=self.check_usb_devices).pack(pady=5)

        # Back button
        ttk.Button(self.current_frame, text="Back to Menu", 
                  command=self.show_main_menu).pack(pady=10)

    def check_usb_devices(self):
        """Check connected USB devices"""
        self.status_text.delete(1.0, tk.END)
        self.status_text.insert(tk.END, "Checking USB devices...\n")

        try:
            result = subprocess.run(['adb', 'devices'], 
                                  capture_output=True, text=True, timeout=10)
            self.status_text.insert(tk.END, f"ADB Output:\n{result.stdout}\n")

            # Parse devices
            lines = result.stdout.strip().split('\n')[1:]  # Skip first line
            devices = [line.split('\t')[0] for line in lines if '\tdevice' in line]

            if devices:
                self.status_text.insert(tk.END, f"\nFound {len(devices)} device(s):\n")
                for device in devices:
                    self.status_text.insert(tk.END, f"• {device}\n")

                self.current_device = devices[0]  # Use first device
                self.status_text.insert(tk.END, f"\nUsing device: {self.current_device}\n")

                # Show mode selection
                ttk.Button(self.current_frame, text="Tiếp tục chọn chế độ", 
                       command=self.show_mode_selection).pack(pady=10)
            else:
                self.status_text.insert(tk.END, "\nKhông tìm thấy thiết bị nào. Vui lòng:\n")
                self.status_text.insert(tk.END, "1. Bật Gỡ lỗi USB trên thiết bị của bạn\n")
                self.status_text.insert(tk.END, "2. Kết nối bằng cáp USB\n")
                self.status_text.insert(tk.END, "3. Chấp nhận hộp thoại gỡ lỗi USB\n")

        except Exception as e:
            self.status_text.insert(tk.END, f"Error: {str(e)}\n")

    def show_pair_mode(self):
        """Pair Mode Frame for wireless debugging"""
        self.clear_frame()
        self.current_frame = ttk.Frame(self.root)
        self.current_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        ttk.Label(self.current_frame, text="Chế độ Ghép nối (Gỡ lỗi không dây - Android 11+)", 
                 font=("Arial", 16, "bold")).pack(pady=10)

        # Input fields
        input_frame = ttk.Frame(self.current_frame)
        input_frame.pack(pady=10)

        ttk.Label(input_frame, text="Device IP:").grid(row=0, column=0, sticky="w", padx=5)
        self.pair_ip = ttk.Entry(input_frame, width=20)
        self.pair_ip.grid(row=0, column=1, padx=5)

        ttk.Label(input_frame, text="Pair Port:").grid(row=1, column=0, sticky="w", padx=5)
        self.pair_port = ttk.Entry(input_frame, width=20)
        self.pair_port.grid(row=1, column=1, padx=5)

        ttk.Label(input_frame, text="Pair Code:").grid(row=2, column=0, sticky="w", padx=5)
        self.pair_code = ttk.Entry(input_frame, width=20)
        self.pair_code.grid(row=2, column=1, padx=5)

        ttk.Label(input_frame, text="Connection Port:").grid(row=3, column=0, sticky="w", padx=5)
        self.conn_port = ttk.Entry(input_frame, width=20)
        self.conn_port.grid(row=3, column=1, padx=5)
        self.conn_port.insert(0, "5555")  # Default

        # Status text
        self.status_text = tk.Text(self.current_frame, height=8, width=70)
        self.status_text.pack(pady=10)

        # Buttons
        button_frame = ttk.Frame(self.current_frame)
        button_frame.pack(pady=10)

        ttk.Button(button_frame, text="Bắt đầu quá trình ghép nối", 
                  command=self.start_pairing).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Quay lại Menu", 
                  command=self.show_main_menu).pack(side=tk.LEFT, padx=5)

    def start_pairing(self):
        """Start the pairing process"""
        ip = self.pair_ip.get()
        pair_port = self.pair_port.get()
        pair_code = self.pair_code.get()
        conn_port = self.conn_port.get()

        if not all([ip, pair_port, pair_code, conn_port]):
            messagebox.showerror("Error", "Please fill all fields")
            return

        self.status_text.delete(1.0, tk.END)

        # Step 1: Pair
        self.status_text.insert(tk.END, f"Pairing with {ip}:{pair_port}...\n")
        try:
            result = subprocess.run(['adb', 'pair', f"{ip}:{pair_port}", pair_code], 
                                  capture_output=True, text=True, timeout=30)
            self.status_text.insert(tk.END, f"Pair result: {result.stdout}\n")

            if result.returncode == 0:
                # Step 2: Connect
                self.status_text.insert(tk.END, f"\nConnecting to {ip}:{conn_port}...\n")
                result = subprocess.run(['adb', 'connect', f"{ip}:{conn_port}"], 
                                      capture_output=True, text=True, timeout=10)
                self.status_text.insert(tk.END, f"Connect result: {result.stdout}\n")

                if "connected" in result.stdout.lower():
                    self.current_device = f"{ip}:{conn_port}"
                    self.status_text.insert(tk.END, f"\nSuccess! Device: {self.current_device}\n")

                    # Show mode selection
                    ttk.Button(self.current_frame, text="Continue to Mode Selection", 
                              command=self.show_mode_selection).pack(pady=10)
                else:
                    self.status_text.insert(tk.END, "\nConnection failed. Check IP and port.\n")
            else:
                self.status_text.insert(tk.END, f"\nPairing failed: {result.stderr}\n")

        except Exception as e:
            self.status_text.insert(tk.END, f"Error: {str(e)}\n")

    def show_direct_ip_mode(self):
        """Direct IP Mode Frame"""
        self.clear_frame()
        self.current_frame = ttk.Frame(self.root)
        self.current_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        ttk.Label(self.current_frame, text="Direct IP Mode", 
                 font=("Arial", 16, "bold")).pack(pady=10)

        # Menu buttons
        button_frame = ttk.Frame(self.current_frame)
        button_frame.pack(pady=20)

        ttk.Button(button_frame, text="[1] USB → Bật TCP/IP", 
                   command=self.enable_tcpip, width=25).pack(pady=5)
        ttk.Button(button_frame, text="[2] Kết nối lại IP trước đó", 
                   command=self.reconnect_ip, width=25).pack(pady=5)
        ttk.Button(button_frame, text="[3] Nhập IP thủ công", 
                   command=self.manual_ip_entry, width=25).pack(pady=5)
        ttk.Button(button_frame, text="[4] Quét mạng nội bộ", 
                   command=self.scan_network, width=25).pack(pady=5)
        ttk.Button(button_frame, text="Quay lại Menu", 
                   command=self.show_main_menu, width=25).pack(pady=10)

        # Status text
        self.status_text = tk.Text(self.current_frame, height=10, width=70)
        self.status_text.pack(pady=10)

    def enable_tcpip(self):
        """Enable TCP/IP mode from USB"""
        self.status_text.delete(1.0, tk.END)
        self.status_text.insert(tk.END, "Enabling TCP/IP mode...\n")

        try:
            # Enable TCP/IP
            result = subprocess.run(['adb', 'tcpip', '5555'], 
                                  capture_output=True, text=True, timeout=10)
            self.status_text.insert(tk.END, f"TCP/IP result: {result.stdout}\n")

            if result.returncode == 0:
                # Get IP address
                time.sleep(2)  # Wait for TCP/IP to start
                result = subprocess.run(['adb', 'shell', 'ip', 'route'], 
                                      capture_output=True, text=True, timeout=10)

                # Extract IP
                ip_match = re.search(r'src (\d+\.\d+\.\d+\.\d+)', result.stdout)
                if ip_match:
                    device_ip = ip_match.group(1)
                    self.status_text.insert(tk.END, f"Device IP: {device_ip}\n")

                    # Connect
                    self.status_text.insert(tk.END, f"Connecting to {device_ip}:5555...\n")
                    result = subprocess.run(['adb', 'connect', f"{device_ip}:5555"], 
                                          capture_output=True, text=True, timeout=10)
                    self.status_text.insert(tk.END, f"Connect result: {result.stdout}\n")

                    if "connected" in result.stdout.lower():
                        self.current_device = f"{device_ip}:5555"
                        self.status_text.insert(tk.END, f"\nSuccess! Device: {self.current_device}\n")

                        # Show mode selection
                        ttk.Button(self.current_frame, text="Tiếp tục đến lựa chọn chế độ", 
                                  command=self.show_mode_selection).pack(pady=10)
                else:
                    self.status_text.insert(tk.END, "Không thể lấy địa chỉ IP của thiết bị. Vui lòng thử nhập thủ công.\n")
            else:
                self.status_text.insert(tk.END, f"Thất bại: {result.stderr}\n")

        except Exception as e:
            self.status_text.insert(tk.END, f"Lỗi: {str(e)}\n")

    def reconnect_ip(self):
        """Reconnect to previous IP"""
        # Simple dialog to enter IP
        import tkinter.simpledialog
        ip = tkinter.simpledialog.askstring("Kết nối lại", "Nhập IP:Port (e.g., 192.168.1.100:5555)")
        if ip:
            self.connect_to_ip(ip)

    def manual_ip_entry(self):
        """Manual IP entry dialog"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Nhập IP thủ công")
        dialog.geometry("300x150")

        ttk.Label(dialog, text="Địa chỉ IP:").pack(pady=5)
        ip_entry = ttk.Entry(dialog, width=20)
        ip_entry.pack(pady=5)

        ttk.Label(dialog, text="Cổng:").pack(pady=5)
        port_entry = ttk.Entry(dialog, width=20)
        port_entry.pack(pady=5)
        port_entry.insert(0, "5555")

        def connect():
            ip = ip_entry.get()
            port = port_entry.get()
            if ip and port:
                self.connect_to_ip(f"{ip}:{port}")
                dialog.destroy()

        ttk.Button(dialog, text="Connect", command=connect).pack(pady=10)

    def scan_network(self):
        """Scan local network for devices"""
        self.status_text.delete(1.0, tk.END)
        self.status_text.insert(tk.END, "Scanning local network...\n")

        # Get local IP range
        try:
            hostname = socket.gethostname()
            local_ip = socket.gethostbyname(hostname)
            base_ip = '.'.join(local_ip.split('.')[:-1])

            self.status_text.insert(tk.END, f"Scanning {base_ip}.1-254:5555...\n")

            def scan():
                found_devices = []
                for i in range(1, 255):
                    ip = f"{base_ip}.{i}"
                    try:
                        result = subprocess.run(['adb', 'connect', f"{ip}:5555"], 
                                              capture_output=True, text=True, timeout=2)
                        if "connected" in result.stdout.lower():
                            found_devices.append(f"{ip}:5555")
                            self.status_text.insert(tk.END, f"Found: {ip}:5555\n")
                            self.status_text.see(tk.END)
                            self.root.update()
                    except:
                        pass

                if found_devices:
                    self.current_device = found_devices[0]
                    self.status_text.insert(tk.END, f"\nUsing device: {self.current_device}\n")
                    # Show mode selection
                    ttk.Button(self.current_frame, text="Continue to Mode Selection", 
                              command=self.show_mode_selection).pack(pady=10)
                else:
                    self.status_text.insert(tk.END, "\nNo devices found on network.\n")

            threading.Thread(target=scan, daemon=True).start()

        except Exception as e:
            self.status_text.insert(tk.END, f"Scan error: {str(e)}\n")

    def connect_to_ip(self, ip_port):
        """Connect to IP:Port"""
        self.status_text.insert(tk.END, f"Connecting to {ip_port}...\n")

        try:
            result = subprocess.run(['adb', 'connect', ip_port], 
                                  capture_output=True, text=True, timeout=10)
            self.status_text.insert(tk.END, f"Result: {result.stdout}\n")

            if "connected" in result.stdout.lower():
                self.current_device = ip_port
                self.status_text.insert(tk.END, f"Success! Device: {self.current_device}\n")

                # Show mode selection
                ttk.Button(self.current_frame, text="Continue to Mode Selection", 
                          command=self.show_mode_selection).pack(pady=10)
            else:
                self.status_text.insert(tk.END, "Connection failed.\n")

        except Exception as e:
            self.status_text.insert(tk.END, f"Error: {str(e)}\n")

    def show_mode_selection(self):
        """Show mode selection frame"""
        self.clear_frame()
        self.current_frame = ttk.Frame(self.root)
        self.current_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        ttk.Label(self.current_frame, text="Chọn chế độ", 
                 font=("Arial", 16, "bold")).pack(pady=10)
        
        ttk.Label(self.current_frame, text=f"Thiết bị: {self.current_device}", 
                 font=("Arial", 10)).pack(pady=5)
        
        # Nút chọn chế độ
        button_frame = ttk.Frame(self.current_frame)
        button_frame.pack(pady=20)
        
        # Chế độ Chơi game
        gaming_frame = ttk.LabelFrame(button_frame, text="Chế độ Chơi game", padding=20)
        gaming_frame.pack(side=tk.LEFT, padx=20, fill=tk.BOTH, expand=True)
        
        ttk.Label(gaming_frame, text="• Ưu tiên độ trễ thấp", 
                 font=("Arial", 10)).pack(anchor="w")
        ttk.Label(gaming_frame, text="• Giảm bộ đệm", 
                 font=("Arial", 10)).pack(anchor="w")
        ttk.Label(gaming_frame, text="• Tùy chọn âm thanh", 
                 font=("Arial", 10)).pack(anchor="w")
        ttk.Label(gaming_frame, text="• Tối ưu hóa cho chơi game", 
                 font=("Arial", 10)).pack(anchor="w")
        
        ttk.Button(gaming_frame, text="Chế độ Chơi game", 
                  command=self.show_gaming_mode, width=15).pack(pady=10)
        
        # Chế độ Xem phim/Streaming
        movie_frame = ttk.LabelFrame(button_frame, text="Chế độ Xem phim/Streaming", padding=20)
        movie_frame.pack(side=tk.RIGHT, padx=20, fill=tk.BOTH, expand=True)
        
        ttk.Label(movie_frame, text="• Ưu tiên chất lượng cao", 
                 font=("Arial", 10)).pack(anchor="w")
        ttk.Label(movie_frame, text="• Bộ đệm lớn", 
                 font=("Arial", 10)).pack(anchor="w")
        ttk.Label(movie_frame, text="• Âm thanh đầy đủ", 
                 font=("Arial", 10)).pack(anchor="w")
        ttk.Label(movie_frame, text="• Trải nghiệm rạp phim", 
                 font=("Arial", 10)).pack(anchor="w")
        
        ttk.Button(movie_frame, text="Chế độ Xem phim", 
                  command=self.show_movie_mode, width=15).pack(pady=10)
        
        # Nút quay lại
        ttk.Button(self.current_frame, text="Quay lại Menu", 
                  command=self.show_main_menu).pack(pady=20)

    def show_gaming_mode(self):
        """Show Gaming Mode configuration"""
        self.clear_frame()
        self.current_frame = ttk.Frame(self.root)
        self.current_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Create notebook for tabs
        notebook = ttk.Notebook(self.current_frame)
        notebook.pack(fill=tk.BOTH, expand=True)

        # Quality tab
        quality_frame = ttk.Frame(notebook)
        notebook.add(quality_frame, text="Quality")

        ttk.Label(quality_frame, text="Gaming Mode - Quality Settings", 
                 font=("Arial", 14, "bold")).pack(pady=10)

        # Quality presets
        ttk.Label(quality_frame, text="Quality Presets:").pack(anchor="w", padx=10)
        self.gaming_quality = tk.StringVar(value="medium")

        quality_options = [
            ("Ultra Low (480p, 2M, 24fps)", "ultra_low"),
            ("Low (720p, 2M, 30fps)", "low"),
            ("Medium (1024p, 4M, 60fps)", "medium"),
            ("High (1080p, 8M, 90fps)", "high"),
            ("Ultra (1920p, 16M, 120fps)", "ultra"),
            ("Custom", "custom")
        ]

        for text, value in quality_options:
            ttk.Radiobutton(quality_frame, text=text, variable=self.gaming_quality, 
                           value=value).pack(anchor="w", padx=20)

        # Custom settings
        custom_frame = ttk.LabelFrame(quality_frame, text="Custom Settings", padding=10)
        custom_frame.pack(fill="x", padx=10, pady=10)

        custom_grid = ttk.Frame(custom_frame)
        custom_grid.pack(fill="x")

        ttk.Label(custom_grid, text="Resolution:").grid(row=0, column=0, sticky="w")
        self.custom_res = ttk.Entry(custom_grid, width=10)
        self.custom_res.grid(row=0, column=1, padx=5)
        self.custom_res.insert(0, "1080")

        ttk.Label(custom_grid, text="Bitrate:").grid(row=0, column=2, sticky="w", padx=(20,0))
        self.custom_bitrate = ttk.Entry(custom_grid, width=10)
        self.custom_bitrate.grid(row=0, column=3, padx=5)
        self.custom_bitrate.insert(0, "4M")

        ttk.Label(custom_grid, text="FPS:").grid(row=0, column=4, sticky="w", padx=(20,0))
        self.custom_fps = ttk.Entry(custom_grid, width=10)
        self.custom_fps.grid(row=0, column=5, padx=5)
        self.custom_fps.insert(0, "60")

        # Audio tab
        audio_frame = ttk.Frame(notebook)
        notebook.add(audio_frame, text="Audio & Latency")

        ttk.Label(audio_frame, text="Audio Options:", font=("Arial", 12, "bold")).pack(anchor="w", pady=10)

        self.gaming_audio = tk.BooleanVar(value=True)
        ttk.Checkbutton(audio_frame, text="Enable Audio", variable=self.gaming_audio).pack(anchor="w", padx=10)

        ttk.Label(audio_frame, text="Latency Profiles:", font=("Arial", 12, "bold")).pack(anchor="w", pady=(20,10))

        self.latency_profile = tk.StringVar(value="low")
        latency_options = [
            ("Ultra Low (buffer=0, audio=30, H.264)", "ultra_low"),
            ("Low (buffer=10, audio=40, H.264)", "low"),
            ("Normal (default)", "normal"),
            ("Custom", "custom_latency")
        ]

        for text, value in latency_options:
            ttk.Radiobutton(audio_frame, text=text, variable=self.latency_profile, 
                           value=value).pack(anchor="w", padx=10)

        # Custom latency
        latency_custom_frame = ttk.LabelFrame(audio_frame, text="Custom Latency", padding=10)
        latency_custom_frame.pack(fill="x", padx=10, pady=10)

        latency_grid = ttk.Frame(latency_custom_frame)
        latency_grid.pack(fill="x")

        ttk.Label(latency_grid, text="Video Buffer:").grid(row=0, column=0, sticky="w")
        self.custom_video_buffer = ttk.Entry(latency_grid, width=10)
        self.custom_video_buffer.grid(row=0, column=1, padx=5)
        self.custom_video_buffer.insert(0, "10")

        ttk.Label(latency_grid, text="Audio Buffer:").grid(row=0, column=2, sticky="w", padx=(20,0))
        self.custom_audio_buffer = ttk.Entry(latency_grid, width=10)
        self.custom_audio_buffer.grid(row=0, column=3, padx=5)
        self.custom_audio_buffer.insert(0, "40")

        ttk.Label(latency_grid, text="Codec:").grid(row=1, column=0, sticky="w", pady=(5,0))
        self.custom_codec = ttk.Combobox(latency_grid, values=["h264", "h265", "av1"], width=8)
        self.custom_codec.grid(row=1, column=1, padx=5, pady=(5,0))
        self.custom_codec.set("h264")

        # Additional tab
        additional_frame = ttk.Frame(notebook)
        notebook.add(additional_frame, text="Additional Options")

        ttk.Label(additional_frame, text="Additional Options:", font=("Arial", 12, "bold")).pack(anchor="w", pady=10)

        self.show_touches = tk.BooleanVar()
        self.record_session = tk.BooleanVar()
        self.turn_off_screen = tk.BooleanVar()
        self.stay_awake = tk.BooleanVar()
        self.fullscreen = tk.BooleanVar()
        self.always_on_top = tk.BooleanVar()

        ttk.Checkbutton(additional_frame, text="Hiển thị thao tác chạm", variable=self.show_touches).pack(anchor="w", padx=10)
        ttk.Checkbutton(additional_frame, text="Ghi màn hình", variable=self.record_session).pack(anchor="w", padx=10)
        ttk.Checkbutton(additional_frame, text="Tắt màn hình", variable=self.turn_off_screen).pack(anchor="w", padx=10)
        ttk.Checkbutton(additional_frame, text="Giữ màn hình luôn bật", variable=self.stay_awake).pack(anchor="w", padx=10)
        ttk.Checkbutton(additional_frame, text="Toàn màn hình", variable=self.fullscreen).pack(anchor="w", padx=10)
        ttk.Checkbutton(additional_frame, text="Luôn ở trên cùng", variable=self.always_on_top).pack(anchor="w", padx=10)

        # Record file selection
        record_frame = ttk.Frame(additional_frame)
        record_frame.pack(fill="x", padx=10, pady=10)

        ttk.Label(record_frame, text="Record File:").pack(side=tk.LEFT)
        self.record_file = ttk.Entry(record_frame, width=40)
        self.record_file.pack(side=tk.LEFT, padx=5)
        ttk.Button(record_frame, text="Browse", 
                  command=lambda: self.record_file.insert(0, filedialog.asksaveasfilename(
                      defaultextension=".mkv", filetypes=[("MKV files", "*.mkv")]))).pack(side=tk.LEFT)

        # Action buttons
        action_frame = ttk.Frame(self.current_frame)
        action_frame.pack(pady=10)

        ttk.Button(action_frame, text="Preview Command", 
                  command=lambda: self.preview_command("gaming")).pack(side=tk.LEFT, padx=5)
        ttk.Button(action_frame, text="Start Gaming Mode", 
                  command=lambda: self.start_scrcpy("gaming")).pack(side=tk.LEFT, padx=5)
        ttk.Button(action_frame, text="Back", 
                  command=self.show_mode_selection).pack(side=tk.LEFT, padx=5)

    def show_movie_mode(self):
        """Show Movie Mode configuration"""
        self.clear_frame()
        self.current_frame = ttk.Frame(self.root)
        self.current_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Create notebook for tabs
        notebook = ttk.Notebook(self.current_frame)
        notebook.pack(fill=tk.BOTH, expand=True)

        # Quality tab
        quality_frame = ttk.Frame(notebook)
        notebook.add(quality_frame, text="Quality")

        ttk.Label(quality_frame, text="Movie/Streaming Mode - Quality Settings", 
                 font=("Arial", 14, "bold")).pack(pady=10)

        # Quality presets
        ttk.Label(quality_frame, text="Quality Presets:").pack(anchor="w", padx=10)
        self.movie_quality = tk.StringVar(value="movie_1080p")

        quality_options = [
            ("Movie 1080p (1920p, 6M, 24fps)", "movie_1080p"),
            ("Cinema Ultra 4K (3840p, 16M, 60fps)", "cinema_4k"),
            ("Custom", "custom")
        ]

        for text, value in quality_options:
            ttk.Radiobutton(quality_frame, text=text, variable=self.movie_quality, 
                           value=value).pack(anchor="w", padx=20)

        # Custom settings
        custom_frame = ttk.LabelFrame(quality_frame, text="Custom Settings", padding=10)
        custom_frame.pack(fill="x", padx=10, pady=10)

        custom_grid = ttk.Frame(custom_frame)
        custom_grid.pack(fill="x")

        ttk.Label(custom_grid, text="Resolution:").grid(row=0, column=0, sticky="w")
        self.movie_custom_res = ttk.Entry(custom_grid, width=10)
        self.movie_custom_res.grid(row=0, column=1, padx=5)
        self.movie_custom_res.insert(0, "1920")

        ttk.Label(custom_grid, text="Bitrate:").grid(row=0, column=2, sticky="w", padx=(20,0))
        self.movie_custom_bitrate = ttk.Entry(custom_grid, width=10)
        self.movie_custom_bitrate.grid(row=0, column=3, padx=5)
        self.movie_custom_bitrate.insert(0, "6M")

        ttk.Label(custom_grid, text="FPS:").grid(row=0, column=4, sticky="w", padx=(20,0))
        self.movie_custom_fps = ttk.Entry(custom_grid, width=10)
        self.movie_custom_fps.grid(row=0, column=5, padx=5)
        self.movie_custom_fps.insert(0, "24")

        # Audio tab
        audio_frame = ttk.Frame(notebook)
        notebook.add(audio_frame, text="Audio & Quality")

        ttk.Label(audio_frame, text="Audio Options (Required):", font=("Arial", 12, "bold")).pack(anchor="w", pady=10)

        # Audio codec
        ttk.Label(audio_frame, text="Audio Codec:").pack(anchor="w", padx=10, pady=(10,0))
        self.movie_audio_codec = ttk.Combobox(audio_frame, values=["aac", "opus", "flac", "raw"], width=15)
        self.movie_audio_codec.pack(anchor="w", padx=10, pady=5)
        self.movie_audio_codec.set("aac")

        # Audio bitrate
        ttk.Label(audio_frame, text="Audio Bitrate:").pack(anchor="w", padx=10, pady=(10,0))
        self.movie_audio_bitrate = ttk.Entry(audio_frame, width=15)
        self.movie_audio_bitrate.pack(anchor="w", padx=10, pady=5)
        self.movie_audio_bitrate.insert(0, "128k")

        # Audio dup (Android 13+)
        self.movie_audio_dup = tk.BooleanVar()
        ttk.Checkbutton(audio_frame, text="Audio Dup (Android 13+)", variable=self.movie_audio_dup).pack(anchor="w", padx=10)

        ttk.Label(audio_frame, text="Quality Profiles:", font=("Arial", 12, "bold")).pack(anchor="w", pady=(20,10))

        self.movie_latency_profile = tk.StringVar(value="balanced")
        latency_options = [
            ("Smooth Quality (buffer=50/100, H.265)", "smooth"),
            ("Balanced (buffer=30/60)", "balanced"),
            ("Cinema Ultra (buffer=200/200, H.265/AV1)", "cinema_ultra"),
            ("Custom", "custom_latency")
        ]

        for text, value in latency_options:
            ttk.Radiobutton(audio_frame, text=text, variable=self.movie_latency_profile, 
                           value=value).pack(anchor="w", padx=10)

        # Custom latency
        latency_custom_frame = ttk.LabelFrame(audio_frame, text="Custom Quality", padding=10)
        latency_custom_frame.pack(fill="x", padx=10, pady=10)

        latency_grid = ttk.Frame(latency_custom_frame)
        latency_grid.pack(fill="x")

        ttk.Label(latency_grid, text="Video Buffer:").grid(row=0, column=0, sticky="w")
        self.movie_video_buffer = ttk.Entry(latency_grid, width=10)
        self.movie_video_buffer.grid(row=0, column=1, padx=5)
        self.movie_video_buffer.insert(0, "50")

        ttk.Label(latency_grid, text="Audio Buffer:").grid(row=0, column=2, sticky="w", padx=(20,0))
        self.movie_audio_buffer = ttk.Entry(latency_grid, width=10)
        self.movie_audio_buffer.grid(row=0, column=3, padx=5)
        self.movie_audio_buffer.insert(0, "100")

        ttk.Label(latency_grid, text="Video Codec:").grid(row=1, column=0, sticky="w", pady=(5,0))
        self.movie_video_codec = ttk.Combobox(latency_grid, values=["h264", "h265", "av1"], width=8)
        self.movie_video_codec.grid(row=1, column=1, padx=5, pady=(5,0))
        self.movie_video_codec.set("h265")

        # Additional tab
        additional_frame = ttk.Frame(notebook)
        notebook.add(additional_frame, text="Tùy chọn bổ sung")

        ttk.Label(additional_frame, text="Tùy chọn bổ sung:", font=("Arial", 12, "bold")).pack(anchor="w", pady=10)

        self.movie_fullscreen = tk.BooleanVar(value=True)  # Default on for movies
        self.movie_record_session = tk.BooleanVar()
        self.movie_always_on_top = tk.BooleanVar()

        ttk.Checkbutton(additional_frame, text="Toàn màn hình (Mặc định)", variable=self.movie_fullscreen).pack(anchor="w", padx=10)
        ttk.Checkbutton(additional_frame, text="Ghi màn hình", variable=self.movie_record_session).pack(anchor="w", padx=10)
        ttk.Checkbutton(additional_frame, text="Luôn trên cùng (Bổ sung)", variable=self.movie_always_on_top).pack(anchor="w", padx=10)

        # Record file selection
        record_frame = ttk.Frame(additional_frame)
        record_frame.pack(fill="x", padx=10, pady=10)

        ttk.Label(record_frame, text="Record File:").pack(side=tk.LEFT)
        self.movie_record_file = ttk.Entry(record_frame, width=40)
        self.movie_record_file.pack(side=tk.LEFT, padx=5)
        ttk.Button(record_frame, text="Browse", 
                  command=lambda: self.movie_record_file.insert(0, filedialog.asksaveasfilename(
                      defaultextension=".mkv", filetypes=[("MKV files", "*.mkv")]))).pack(side=tk.LEFT)

        # Action buttons
        action_frame = ttk.Frame(self.current_frame)
        action_frame.pack(pady=10)

        ttk.Button(action_frame, text="Xem trước lệnh", 
                  command=lambda: self.preview_command("movie")).pack(side=tk.LEFT, padx=5)
        ttk.Button(action_frame, text="Bắt đầu chế độ xem phim", 
                  command=lambda: self.start_scrcpy("movie")).pack(side=tk.LEFT, padx=5)
        ttk.Button(action_frame, text="Trở lại", 
                  command=self.show_mode_selection).pack(side=tk.LEFT, padx=5)

    def build_scrcpy_command(self, mode):
        """Build scrcpy command based on mode and settings"""
        cmd = ['scrcpy']

        if self.current_device:
            cmd.extend(['-s', self.current_device])

        if mode == "gaming":
            # Quality settings
            quality = self.gaming_quality.get()

            quality_presets = {
                "ultra_low": ["--max-size", "480", "-b", "2M", "--max-fps", "24"],
                "low": ["--max-size", "720", "-b", "2M", "--max-fps", "30"],
                "medium": ["--max-size", "1024", "-b", "4M", "--max-fps", "60"],
                "high": ["--max-size", "1080", "-b", "8M", "--max-fps", "90"],
                "ultra": ["--max-size", "1920", "-b", "16M", "--max-fps", "120"]
            }

            if quality in quality_presets:
                cmd.extend(quality_presets[quality])
            elif quality == "custom":
                cmd.extend(["--max-size", self.custom_res.get()])
                cmd.extend(["-b", self.custom_bitrate.get()])
                cmd.extend(["--max-fps", self.custom_fps.get()])

            # Audio
            if not self.gaming_audio.get():
                cmd.append("--no-audio")

            # Latency profiles
            latency = self.latency_profile.get()
            latency_presets = {
                "ultra_low": ["--video-buffer=0", "--audio-buffer=30", "--video-codec=h264"],
                "low": ["--video-buffer=10", "--audio-buffer=40", "--video-codec=h264"]
            }

            if latency in latency_presets:
                cmd.extend(latency_presets[latency])
            elif latency == "custom_latency":
                cmd.append(f"--video-buffer={self.custom_video_buffer.get()}")
                cmd.append(f"--audio-buffer={self.custom_audio_buffer.get()}")
                cmd.append(f"--video-codec={self.custom_codec.get()}")

            # Additional options
            if self.show_touches.get():
                cmd.append("--show-touches")
            if self.turn_off_screen.get():
                cmd.append("-S")
            if self.stay_awake.get():
                cmd.append("--stay-awake")
            if self.fullscreen.get():
                cmd.append("--fullscreen")
            if self.always_on_top.get():
                cmd.append("--always-on-top")
            if self.record_session.get() and self.record_file.get():
                cmd.extend(["--record", self.record_file.get()])

        elif mode == "movie":
            # Quality settings
            quality = self.movie_quality.get()

            quality_presets = {
                "movie_1080p": ["--max-size", "1920", "-b", "6M", "--max-fps", "24"],
                "cinema_4k": ["--max-size", "3840", "-b", "16M", "--max-fps", "60"]
            }

            if quality in quality_presets:
                cmd.extend(quality_presets[quality])
            elif quality == "custom":
                cmd.extend(["--max-size", self.movie_custom_res.get()])
                cmd.extend(["-b", self.movie_custom_bitrate.get()])
                cmd.extend(["--max-fps", self.movie_custom_fps.get()])

            # Audio (always enabled for movies)
            cmd.extend(["--audio-codec", self.movie_audio_codec.get()])
            cmd.extend(["--audio-bit-rate", self.movie_audio_bitrate.get()])

            if self.movie_audio_dup.get():
                cmd.append("--audio-dup")

            # Quality profiles
            latency = self.movie_latency_profile.get()
            latency_presets = {
                "smooth": ["--video-buffer=50", "--audio-buffer=100", "--video-codec=h265"],
                "balanced": ["--video-buffer=30", "--audio-buffer=60"],
                "cinema_ultra": ["--video-buffer=200", "--audio-buffer=200", "--video-codec=h265"]
            }

            if latency in latency_presets:
                cmd.extend(latency_presets[latency])
            elif latency == "custom_latency":
                cmd.append(f"--video-buffer={self.movie_video_buffer.get()}")
                cmd.append(f"--audio-buffer={self.movie_audio_buffer.get()}")
                cmd.append(f"--video-codec={self.movie_video_codec.get()}")

            # Additional options (fullscreen default for movies)
            if self.movie_fullscreen.get():
                cmd.append("--fullscreen")
            if self.movie_always_on_top.get():
                cmd.append("--always-on-top")
            if self.movie_record_session.get() and self.movie_record_file.get():
                cmd.extend(["--record", self.movie_record_file.get()])

        return cmd

    def preview_command(self, mode):
        """Preview the scrcpy command"""
        cmd = self.build_scrcpy_command(mode)
        command_str = ' '.join(cmd)

        # Show preview dialog
        dialog = tk.Toplevel(self.root)
        dialog.title("Xem trước lệnh")
        dialog.geometry("600x300")

        ttk.Label(dialog, text="Lệnh đã tạo:", font=("Arial", 12, "bold")).pack(pady=10)

        text_widget = tk.Text(dialog, height=8, width=70, wrap=tk.WORD)
        text_widget.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)
        text_widget.insert(1.0, command_str)
        text_widget.config(state=tk.DISABLED)

        button_frame = ttk.Frame(dialog)
        button_frame.pack(pady=10)

        ttk.Button(button_frame, text="Chạy lệnh", 
                  command=lambda: [dialog.destroy(), self.start_scrcpy(mode)]).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Đóng", command=dialog.destroy).pack(side=tk.LEFT, padx=5)

    def start_scrcpy(self, mode):
        """Start scrcpy with built command"""
        cmd = self.build_scrcpy_command(mode)

        try:
            self.scrcpy_process = subprocess.Popen(cmd, 
                                                  stdout=subprocess.PIPE, 
                                                  stderr=subprocess.PIPE,
                                                  text=True)

            messagebox.showinfo("Scrcpy đã khởi động", 
                                f"Scrcpy ở chế độ {mode} đã khởi động thành công!\n\n"
                                f"Lệnh: {' '.join(cmd)}")

            # Show return menu
            self.show_return_menu()

            # Monitor process in background
            def monitor():
                self.scrcpy_process.wait()
                if self.scrcpy_process.returncode != 0:
                    stderr = self.scrcpy_process.stderr.read()
                    messagebox.showerror("Scrcpy Error", f"Scrcpy exited with error:\n{stderr}")

            threading.Thread(target=monitor, daemon=True).start()

        except Exception as e:
            messagebox.showerror("Error", f"Failed to start scrcpy:\n{str(e)}")

    def show_return_menu(self):
        """Show return menu after starting scrcpy"""
        self.clear_frame()
        self.current_frame = ttk.Frame(self.root)
        self.current_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        ttk.Label(self.current_frame, text="Scrcpy is Running", 
                 font=("Arial", 16, "bold")).pack(pady=20)

        ttk.Label(self.current_frame, text=f"Device: {self.current_device}", 
                 font=("Arial", 10)).pack(pady=5)

        # Menu buttons
        button_frame = ttk.Frame(self.current_frame)
        button_frame.pack(pady=20)

        ttk.Button(button_frame, text="Quay lại Menu chính", 
                   command=self.show_main_menu, width=25).pack(pady=5)
        ttk.Button(button_frame, text="Kết nối lại thiết bị hiện tại", 
                   command=self.show_mode_selection, width=25).pack(pady=5)
        ttk.Button(button_frame, text="Thay đổi Chất lượng/Chế độ", 
                   command=self.show_mode_selection, width=25).pack(pady=5)
        ttk.Button(button_frame, text="Dừng Scrcpy & Thoát", 
                   command=self.stop_and_exit, width=25).pack(pady=5)

    def stop_and_exit(self):
        """Stop scrcpy and exit"""
        if self.scrcpy_process:
            self.scrcpy_process.terminate()
        self.exit_app()

    def show_guide(self):
        """Show guide frame"""
        self.clear_frame()
        self.current_frame = ttk.Frame(self.root)
        self.current_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Create notebook for guide sections
        notebook = ttk.Notebook(self.current_frame)
        notebook.pack(fill=tk.BOTH, expand=True)

        # Connection Guide
        conn_frame = ttk.Frame(notebook)
        notebook.add(conn_frame, text="Connection Guide")

        conn_text = tk.Text(conn_frame, height=20, width=80, wrap=tk.WORD)
        conn_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        guide_content = """Hướng dẫn Chế độ USB:

1. Bật Gỡ lỗi USB trong Tùy chọn nhà phát triển
2. Kết nối thiết bị bằng cáp USB
3. Chấp nhận hộp thoại gỡ lỗi USB trên thiết bị
4. Nhấn “Kiểm tra thiết bị USB” trong Chế độ USB

Hướng dẫn Chế độ Ghép nối (Android 11+):
1. Vào Cài đặt > Tùy chọn nhà phát triển
2. Bật “Gỡ lỗi không dây”
3. Chọn “Ghép nối thiết bị bằng mã ghép nối”
4. Nhập IP, cổng và mã ghép nối vào ứng dụng này
5. Kết nối sẽ được thiết lập tự động

Hướng dẫn Chế độ IP trực tiếp:
1. USB → TCP/IP: Kết nối qua USB trước, sau đó bật TCP/IP
2. Nhập IP thủ công: Tự nhập địa chỉ IP của thiết bị
3. Quét mạng: Tự động quét mạng nội bộ để tìm thiết bị

Mẹo:
• Dùng Wi-Fi 5GHz để có hiệu năng không dây tốt hơn
• Giữ thiết bị và máy tính trong cùng một mạng khi dùng chế độ không dây
• Kết nối USB luôn mang lại trải nghiệm ổn định nhất
"""

        conn_text.insert(1.0, guide_content)
        conn_text.config(state=tk.DISABLED)

        # Gaming Tips
        gaming_frame = ttk.Frame(notebook)
        notebook.add(gaming_frame, text="Gaming Tips")

        gaming_text = tk.Text(gaming_frame, height=20, width=80, wrap=tk.WORD)
        gaming_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        gaming_content = """Tối ưu hóa Chế độ Chơi game:

Cài đặt tốt nhất cho chơi game:
• Chất lượng: Trung bình hoặc Cao (tránh Siêu cao để giảm độ trễ)
• Độ trễ: Hồ sơ Siêu thấp hoặc Thấp
• Âm thanh: Tắt để có độ trễ thấp nhất
• Codec: H.264 (mã hóa nhanh nhất)
• Bộ đệm: 0–10ms cho video

Khuyến nghị mạng:
• Dùng kết nối USB khi có thể
• Wi-Fi 5GHz cho chế độ không dây
• Đóng các ứng dụng tiêu tốn băng thông
• Dùng kết nối mạng dây trên PC

Mẹo bổ sung:
• Bật “Hiển thị thao tác chạm” khi stream
• Dùng “Tắt màn hình” để tiết kiệm pin
• “Giữ màn hình luôn bật” tránh thiết bị ngủ
• Độ phân giải thấp = độ trễ thấp hơn
• Tắt hiệu ứng hoạt họa trên thiết bị
"""

        gaming_text.insert(1.0, gaming_content)
        gaming_text.config(state=tk.DISABLED)

        # Movie Tips
        movie_frame = ttk.Frame(notebook)
        notebook.add(movie_frame, text="Movie Tips")

        movie_text = tk.Text(movie_frame, height=20, width=80, wrap=tk.WORD)
        movie_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        movie_content = """Tối ưu hóa Chế độ Xem phim/Streaming:

Cài đặt tốt nhất cho phim:
Chất lượng: 1080p Movie hoặc Cinema Ultra 4K
• Độ trễ: Chất lượng mượt hoặc Cinema Ultra
• Âm thanh: Bộ mã hóa AAC với bitrate từ 128k trở lên
• Codec: H.265 cho chất lượng tốt nhất (nếu được hỗ trợ)
• Bộ đệm: 50–200ms để phát lại mượt mà

Nâng cao chất lượng:
• Sử dụng độ phân giải cao nhất mà mạng của bạn chịu được
• Codec H.265/HEVC cho khả năng nén tốt hơn
• Codec AV1 cho thiết bị mới (thử nghiệm)
• Bộ đệm lớn để streaming mượt hơn
• Bật “Audio Dup” cho Android 13+

Yêu cầu mạng:
• Kết nối Wi-Fi ổn định
• Bitrate 6M+ cần tín hiệu mạnh
• Streaming 4K yêu cầu kết nối cực tốt
• Dùng “Toàn màn hình” để có trải nghiệm rạp phim
• “Luôn ở trên cùng” khi muốn đa nhiệm

Ghi hình:
• Khuyến nghị dùng định dạng MKV
• Bitrate cao hơn cho chất lượng ghi tốt hơn
• Cần đủ dung lượng lưu trữ
"""

        movie_text.insert(1.0, movie_content)
        movie_text.config(state=tk.DISABLED)

        # Links
        links_frame = ttk.Frame(notebook)
        notebook.add(links_frame, text="Resources")

        links_text = tk.Text(links_frame, height=20, width=80, wrap=tk.WORD)
        links_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        links_content = """Tài nguyên chính thức:

• Kho lưu trữ Scrcpy chính thức:
https://github.com/Genymobile/scrcpy
• Android Platform Tools (ADB):
https://developer.android.com/studio/releases/platform-tools

Tài liệu:
• Tài liệu Scrcpy: Có trong kho GitHub
• Hướng dẫn Tùy chọn nhà phát triển Android
• Hướng dẫn bật gỡ lỗi USB

Xử lý sự cố:
• Kiểm tra mục issues trên GitHub Scrcpy cho các vấn đề thường gặp
• Xác minh kết nối ADB và thiết bị
• Cập nhật lên phiên bản Scrcpy mới nhất
• Kiểm tra tính tương thích của phiên bản Android

Yêu cầu hệ thống:
• Android 5.0+ (API 21 trở lên)
• Gỡ lỗi ADB được bật
• Đã cài đặt driver USB (cho chế độ USB)
• Có kết nối mạng (cho chế độ không dây)

Mẹo hiệu năng:
• Đóng ứng dụng không cần thiết trên thiết bị
• Bật chế độ hiệu năng cao trên thiết bị
• Đảm bảo kết nối mạng ổn định
• Giữ thiết bị và PC cùng trong một mạng khi dùng chế độ không dây
"""

        links_text.insert(1.0, links_content)
        links_text.config(state=tk.DISABLED)

        # Back button
        ttk.Button(self.current_frame, text="Back to Menu", 
                  command=self.show_main_menu).pack(pady=10)

    def exit_app(self):
        """Exit application with thank you message"""
        # Stop any running scrcpy process
        if self.scrcpy_process:
            try:
                self.scrcpy_process.terminate()
            except:
                pass

        # Show thank you message
        message = """Cảm ơn bạn đã sử dụng Scrcpy GUI Tool!

    Developed by: Pan
○ Mục đích: Tối ưu hóa Chơi game & Xem phim cho scrcpy
○ Hy vọng ứng dụng này giúp ích cho việc sử dụng scrcpy của bạn.
    Chúc bạn có trải nghiệm tuyệt vời!"""

        messagebox.showinfo("Cảm ơn - Thank You", message)
        self.root.quit()
        self.root.destroy()
        sys.exit()

    def run(self):
        """Run the application"""
        # Handle window close event
        self.root.protocol("WM_DELETE_WINDOW", self.exit_app)
        self.root.mainloop()

if __name__ == "__main__":
    app = ScrcpyGUI()
    app.run()
