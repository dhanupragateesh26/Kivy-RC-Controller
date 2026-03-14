# Kivy RC Controller (Android APK)

A custom **Android remote control application** built with **Python + Kivy** to control robots, RC vehicles, or IoT devices using **WiFi UDP communication**.

The app features dual joysticks, speed control, and a boost button for real-time control.

---

## Features

* Dual virtual joysticks
* Adjustable speed limiter
* Boost mode
* Real-time UDP communication
* Touch optimized UI
* Lightweight APK
* Works with ESP32 / WiFi robots

---

## UI Overview

Controls included:

| Control        | Function              |
| -------------- | --------------------- |
| Left Joystick  | Forward / Reverse     |
| Right Joystick | Steering              |
| Speed Slider   | Maximum speed limiter |
| Boost Button   | Full power override   |

---

## Communication Protocol

The app sends UDP packets in the format:

```
forward,steering,speed_limit,boost
```

Example:

```
45,-20,50,0
```

| Value       | Description |
| ----------- | ----------- |
| forward     | -100 to 100 |
| steering    | -100 to 100 |
| speed_limit | 20–80       |
| boost       | 0 or 1      |

---

## Network Configuration

Default settings:

```
ESP32 IP: 192.168.4.1
UDP Port: 4210
```

These can be modified in:

```
app/main.py
```

---

## System Architecture

```
Android App
   │
   │ UDP Packets
   ▼
ESP32 WiFi Access Point
   │
Robot / RC Controller
```

---

## Screenshots

Place screenshots in:

```
docs/images/ui_preview.png
```

---

# Building the APK

The app is compiled using **Buildozer**.

### Requirements

Linux is recommended (Ubuntu).

Install dependencies:

```
sudo apt update
sudo apt install python3-pip git zip unzip openjdk-17-jdk
pip install --user buildozer
pip install --user cython
```

---

### Initialize Buildozer

Navigate to the project root:

```
buildozer init
```

Replace the generated spec file with the one in:

```
build/buildozer.spec
```

---

### Build the APK

Run:

```
buildozer -v android debug
```

The APK will appear in:

```
bin/
```

Example:

```
bin/kivyrccontroller-0.1-debug.apk
```

---

### Install on Phone

Enable **Developer Mode** and install:

```
adb install bin/kivyrccontroller-0.1-debug.apk
```

Or copy the APK to your phone and install manually.

---

# Running Without APK (Desktop)

You can test the app directly with Python.

Install dependencies:

```
pip install kivy
```

Run:

```
python app/main.py
```

---

# Future Improvements

* Telemetry display
* Battery indicator
* Camera streaming
* Custom joystick sensitivity
* Gamepad support
* Dark mode UI

---

# License

MIT License

