@echo off
setlocal ENABLEEXTENSIONS ENABLEDELAYEDEXPANSION
title scrcpy WiFi (Gaming & Low Latency Mode)

:: ================== CẤU HÌNH MẶC ĐỊNH ==================
set PORT=5555
set SCREENOFF=0
:: =======================================================

:: Kiểm tra adb/scrcpy trong PATH
where adb >nul 2>nul || (echo [ERR] Chua co ADB trong PATH. Cai "platform-tools" va them vao PATH. & goto :END)
where scrcpy >nul 2>nul || (echo [ERR] Chua co scrcpy trong PATH. Cai scrcpy va them vao PATH. & goto :END)

:MENU
cls
echo.
echo ================================================
echo  SCRCPY WI-FI MIRRORING (GAMING OPTIMIZED)
echo ================================================
echo  [1] USB Debug (Android ^<=10) - Bat WiFi qua USB
echo  [2] Wireless Debugging (Android 11+ Pair code)
echo  [3] Ket noi truc tiep bang IP:PORT da biet
echo  [4] Huong dan su dung
echo  [0] Thoat
echo ================================================
set /p CHOICE=Chon che do (1/2/3/4/0): 

if "%CHOICE%"=="1" goto :USB_MODE
if "%CHOICE%"=="2" goto :PAIR_MODE
if "%CHOICE%"=="3" goto :DIRECT_MODE
if "%CHOICE%"=="4" goto :GUIDE
if "%CHOICE%"=="0" goto :END
echo [!!!] Lua chon khong hop le. Nhan phim bat ky de chon lai...
pause >nul
goto :MENU

:USB_MODE
cls
echo [*] Che do USB Debug (bat WiFi TCP/IP)...
for /f "tokens=1" %%i in ('adb get-state 2^>nul') do set STATE=%%i
if /I not "%STATE%"=="device" (
  echo [ERR] Khong thay thiet bi USB. Hay cam USB va bat "USB debugging".
  pause
  goto :MENU
)
echo [*] adb tcpip %PORT%
adb tcpip %PORT% >nul

:: Lay IP tu wlan0
set "IP="
for /f "tokens=3" %%a in ('adb shell ip -o -f inet addr show wlan0 ^| findstr /i "inet " 2^>nul') do set IPMASK=%%a
if defined IPMASK for /f "tokens=1 delims=/" %%b in ("%IPMASK%") do set IP=%%b

if not defined IP (
  echo [WARN] Khong lay duoc IP tu wlan0. Nhap tay (vi du 192.168.1.23):
  set /p IP=Nhap IP: 
)
set "HOSTPORT=%IP%:%PORT%"
goto :ADVANCED_OPTIONS

:PAIR_MODE
cls
echo [*] Che do Wireless Debugging (Android 11+)
echo [TIP] Tren dien thoai: Developer options ^> Wireless debugging ^> "Pair device with pairing code"
set /p PAIR_HOST=Nhap host:pair_port (vd 192.168.1.23:37099): 
set /p PAIR_CODE=Nhap Pairing code (6 chu so): 
adb pair %PAIR_HOST% %PAIR_CODE%
if errorlevel 1 (
  echo [ERR] Pair khong thanh cong. Thu lai.
  pause
  goto :MENU
)
set /p HOSTPORT=Nhap IP:port de ket noi (vd 192.168.1.23:5555): 
goto :ADVANCED_OPTIONS

:DIRECT_MODE
cls
set /p HOSTPORT=Nhap IP:port cua dien thoai (vd 192.168.1.23:5555): 
goto :ADVANCED_OPTIONS

:ADVANCED_OPTIONS
cls
set "ENCODER_OPT="
set "AUDIO_OPT=--no-audio"   :: Mac dinh TAT am thanh de giam do tre; co the bat lai o buoc sau
echo.
echo ============ TUY CHON NANG CAO (GAMING) ============
echo  [1] Mac dinh (scrcpy tu chon encoder)
echo  [2] Chi dinh encoder phan cung (nhap ten)
echo  [L] Liet ke encoder ho tro (yeu cau thiet bi da ket noi qua USB/WiFi)
echo =====================================================
set /p ADV_CHOICE=Chon (1/2/L): 

if /i "%ADV_CHOICE%"=="2" (
    set /p ENCODER_NAME=Nhap ten Encoder (vd: OMX.qcom.video.encoder.avc hoac c2.android.avc.encoder): 
    if not "%ENCODER_NAME%"=="" set ENCODER_OPT=--video-encoder="%ENCODER_NAME%"
) else if /i "%ADV_CHOICE%"=="L" (
    cls
    echo [*] Liet ke encoder... (neu chua ket noi, ket qua co the trong)
    scrcpy --list-encoders
    echo.
    pause
)
goto :SELECT_QUALITY

:SELECT_QUALITY
cls
echo.
echo ========== CHON CHE DO CHAT LUONG ==========
echo  [1] Thap       (Low)    - 720p,   2M, 30 FPS
echo  [2] Trung      (Medium) - 1024p,  4M, 60 FPS
echo  [3] Cao        (High)   - 1080p,  8M, 90 FPS
echo  [4] Sieu Cao   (Ultra)  - 1920p, 16M, 120 FPS
echo ===============================================
set /p Q=Chon chat luong (1/2/3/4): 

if "%Q%"=="1" (set RES=720  & set BITRATE=2M  & set FPS=30 & goto :AUDIO_PROMPT)
if "%Q%"=="2" (set RES=1024 & set BITRATE=4M  & set FPS=60 & goto :AUDIO_PROMPT)
if "%Q%"=="3" (set RES=1080 & set BITRATE=8M  & set FPS=90 & goto :AUDIO_PROMPT)
if "%Q%"=="4" (set RES=1920 & set BITRATE=16M & set FPS=120 & goto :AUDIO_PROMPT)

echo [!!!] Lua chon khong hop le.
pause >nul
goto :SELECT_QUALITY

:AUDIO_PROMPT
cls
echo ============ TUY CHON AM THANH ============
echo  Mac dinh: TAT am thanh (--no-audio) de giam do tre.
echo  Bat am thanh chi khi thuc su can (co the tang delay).
echo ==============================================
set /p AUDIO_CHOICE=Bat am thanh? (y/N): 
if /i "%AUDIO_CHOICE%"=="y" set "AUDIO_OPT="

goto :RUN_SCRCPY

:RUN_SCRCPY
cls
echo [*] Ket noi ADB den %HOSTPORT% ...
adb connect %HOSTPORT% >nul
if errorlevel 1 (
  echo [ERR] Ket noi that bai. Kiem tra IP/Port va WiFi cung mang.
  pause
  goto :MENU
)

echo.
adb devices

:: Hop nhat OPTIONS cho scrcpy
set "OPTS=%ENCODER_OPT% %AUDIO_OPT%"
if defined RES set OPTS=!OPTS! -m %RES%
if defined BITRATE set OPTS=!OPTS! -b %BITRATE%
if defined FPS set OPTS=!OPTS! --max-fps %FPS%
if "%SCREENOFF%"=="1" set OPTS=!OPTS! --turn-screen-off
set OPTS=!OPTS! --stay-awake -s %HOSTPORT%

echo.
echo [*] Tham so chay:
echo     scrcpy !OPTS!
echo.
echo [i] Dong cua so scrcpy de quay lai menu...
scrcpy !OPTS!

goto :MENU

:GUIDE
cls
echo.
echo ================= HUONG DAN SU DUNG =================
echo [1] USB Debug (Android ^<=10):
echo     - Cam dien thoai vao PC, bat "USB debugging"
echo     - Script se bat TCP/IP va tim IP; sau do ket noi qua WiFi
echo     - Lan sau chi can dung che do [3] (nhap IP:PORT)
echo.
echo [2] Wireless Debugging (Android 11+):
echo     - Developer options ^> Wireless debugging ^> Pair device with pairing code
echo     - Nhap host:pair_port va Pair code vao script
echo     - Nhap IP:5555 de ket noi
echo.
echo [3] Ket noi truc tiep:
echo     - Nhap IP:PORT (vd 192.168.1.23:5555) de ket noi nhanh
echo.
echo [Chat luong]:
echo     - Low   : Do tre thap nhat, hinh vua du
echo     - Medium: Can bang do tre / chat luong
echo     - High  : Hinh dep, can WiFi 5GHz on dinh
echo     - Ultra : Net cao, de lag neu WiFi yeu
echo.
echo [Meo giam do tre]:
echo     - Dung WiFi 5GHz, de PC va dien thoai gan router
echo     - Chon chat luong phan giai thap = Low
echo     - TAT am thanh (--no-audio) neu choi game
echo     - Neu co the, dung cap USB luon la thap nhat
echo ======================================================
echo [Developer & Error Report]:
echo     - Facebook: facebook.com/S.A.C.L.B9F
echo     - Telegram: @SACLB9F
echo ======================================================
pause
goto :MENU

:END
echo.
endlocal
exit /b