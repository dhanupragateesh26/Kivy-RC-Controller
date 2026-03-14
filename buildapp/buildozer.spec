[app]

title = Kivy RC Controller
package.name = kivyrccontroller
package.domain = org.yourname

source.dir = ../app
source.include_exts = py,png,jpg,kv

version = 0.1

requirements = python3,kivy

orientation = landscape

fullscreen = 0

android.permissions = INTERNET

android.api = 31
android.minapi = 21

android.archs = arm64-v8a, armeabi-v7a

android.entrypoint = org.kivy.android.PythonActivity

[buildozer]

log_level = 2
warn_on_root = 1
