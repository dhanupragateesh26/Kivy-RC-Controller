# Setup Guide

## Step 1 — Clone Repository

```
git clone https://github.com/yourname/kivy-rc-controller.git
cd kivy-rc-controller
```

---

## Step 2 — Install Dependencies

```
sudo apt update
sudo apt install python3-pip git zip unzip openjdk-17-jdk
pip install buildozer cython
```

---

## Step 3 — Build APK

```
cd build
buildozer -v android debug
```

---

## Step 4 — Install APK

```
adb install bin/*.apk
```

---

## Step 5 — Connect to Robot WiFi

Connect phone to:

```
ESP32_RC
```

Default IP:

```
192.168.4.1
```

Launch the app and start controlling.
