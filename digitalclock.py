
import time
import datetime

from kivy.app import App
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.properties import StringProperty
from kivy.properties import NumericProperty
from kivy.uix.widget import Widget
from kivy.uix.floatlayout import FloatLayout


kv = '''
<SecondsIndicator>:
    canvas:
        Color: 
            rgba: 1, 0, 0, 1

        Ellipse:
            size: self.size
            pos: self.pos
            angle_end: root.seconds_angle
            segments: 60

        Color: 
            rgba: 0, 0, 0, 1

        Ellipse:
            size: (self.width * 0.9, self.height * 0.9)
            pos: (self.x + self.width * 0.05, self.y + self.height * 0.05)
            segments: 60


<DigitalClock>:
    SecondsIndicator:
        id: seconds
        pos_hint: {'center_x': 0.5, 'center_y': 0.5}

    Label:
        id: label
        pos_hint: {'center_x': 0.5, 'center_y': 0.5}
        text: self.parent.display_time
        font_size: sp(min( self.height * 0.3, self.width * 0.2 ))
'''

Builder.load_string(kv)

class SecondsIndicator(Widget):
    seconds_angle = NumericProperty(90)

    def __init__(self, **kwargs):
        super(SecondsIndicator, self).__init__(**kwargs)
        self.update()


    def update(self, dt=0):
        current_time = time.localtime()
        seconds = current_time[5]

        self.seconds_angle = (360 / 60) * seconds
        self.schedule_update();


    def schedule_update(self):
        current_time = datetime.datetime.now()
        secs_to_next_sec = (1000.0 - current_time.microsecond) / 1000.0

        Clock.schedule_once(self.update, secs_to_next_sec)


class DigitalClock(FloatLayout):
    display_time = StringProperty("00 : 00")

    def __init__(self, **kwargs):
        super(DigitalClock, self).__init__(**kwargs)


    def update(self, dt=0):
        self.display_time = time.strftime("%H : %M")
        self.schedule_update()


    def schedule_update(self):
        current_time = time.localtime()
        seconds = current_time[5]

        # Handle leap seconds?
        secs_to_next_minute = 60 - seconds

        Clock.schedule_once(self.update, secs_to_next_minute)


class DigitalClockApp(App):
    def build(self):
        dc = DigitalClock()
        dc.update()

        return dc


if __name__ == '__main__':
    DigitalClockApp().run()
