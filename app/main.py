from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.slider import Slider
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.graphics import Color, Ellipse, Rectangle
import socket
import math

# ---------------- CONFIG ----------------
ESP_IP = "192.168.4.1"
ESP_PORT = 4210
UDP_RATE = 0.02
# ---------------------------------------

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

Window.clearcolor = (1, 1, 1, 1)
Window.size = (900, 500)

# ---------------- JOYSTICK ----------------
class Joystick(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.x_val = 0
        self.y_val = 0
        self.radius = 0
        self.knob_radius = 35

        with self.canvas:
            Color(0.85, 0.85, 0.85, 1)
            self.base = Ellipse()

            Color(0.2, 0.6, 1, 1)
            self.knob = Ellipse(size=(70, 70))

    def on_size(self, *args):
        self.radius = min(self.width, self.height) / 2
        self.center_joystick()

    def center_joystick(self):
        cx, cy = self.center
        self.base.pos = (cx - self.radius, cy - self.radius)
        self.base.size = (self.radius * 2, self.radius * 2)
        self.knob.pos = (cx - self.knob_radius, cy - self.knob_radius)

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            self.update_knob(touch)
            return True

    def on_touch_move(self, touch):
        if self.collide_point(*touch.pos):
            self.update_knob(touch)
            return True

    def on_touch_up(self, touch):
        self.x_val = 0
        self.y_val = 0
        self.center_joystick()

    def update_knob(self, touch):
        cx, cy = self.center
        dx = touch.x - cx
        dy = touch.y - cy

        dist = math.hypot(dx, dy)
        if dist > self.radius:
            dx *= self.radius / dist
            dy *= self.radius / dist

        self.knob.pos = (
            cx + dx - self.knob_radius,
            cy + dy - self.knob_radius
        )

        self.x_val = int((dx / self.radius) * 100)
        self.y_val = int((dy / self.radius) * 100)


# ---------------- MAIN APP ----------------
class RoboController(App):
    def build(self):
        layout = FloatLayout()

        # LEFT JOYSTICK → FORWARD / BACKWARD
        self.left_joystick = Joystick(
            size_hint=(0.3, 0.55),
            pos_hint={'x': 0.03, 'y': 0.1}
        )
        layout.add_widget(self.left_joystick)

        # RIGHT JOYSTICK → LEFT / RIGHT
        self.right_joystick = Joystick(
            size_hint=(0.3, 0.55),
            pos_hint={'x': 0.67, 'y': 0.1}
        )
        layout.add_widget(self.right_joystick)

        # SPEED SLIDER (CENTER)
        self.slider = Slider(
            min=20, max=80, value=50,
            size_hint=(0.35, 0.08),
            pos_hint={'center_x': 0.5, 'y': 0.28},
            value_track=True,
            value_track_color=(1, 0, 0, 1)
        )
        layout.add_widget(self.slider)

        with self.slider.canvas.before:
            Color(1, 0.85, 0.85, 1)
            self.slider_bg = Rectangle()

        self.slider.bind(
            pos=lambda *_: self.update_slider_bg(),
            size=lambda *_: self.update_slider_bg()
        )
        self.update_slider_bg()

        # BOOST BUTTON
        self.boost = 0
        self.boost_btn = Button(
            text="BOOST",
            size_hint=(0.25, 0.18),
            pos_hint={'center_x': 0.5, 'y': 0.42},
            background_normal='',
            background_color=(0, 1, 0, 1),
            color=(0, 0, 0, 1),
            bold=True,
            font_size='22sp'
        )

        self.boost_btn.bind(on_press=self.boost_on,
                            on_release=self.boost_off)
        layout.add_widget(self.boost_btn)

        Clock.schedule_interval(self.send_udp, UDP_RATE)
        return layout

    def update_slider_bg(self):
        self.slider_bg.pos = self.slider.pos
        self.slider_bg.size = self.slider.size

    def boost_on(self, *args):
        self.boost = 1

    def boost_off(self, *args):
        self.boost = 0

    def send_udp(self, dt):
        forward = self.left_joystick.y_val      # ⬆⬇
        steering = self.right_joystick.x_val    # ⬅➡
        speed_limit = int(self.slider.value)

        if not self.boost:
            forward = int(forward * speed_limit / 100)

        msg = f"{forward},{steering},{speed_limit},{self.boost}"

        try:
            sock.sendto(msg.encode(), (ESP_IP, ESP_PORT))
        except:
            pass


if __name__ == "__main__":
    RoboController().run()
