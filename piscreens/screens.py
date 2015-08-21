from itertools import cycle
import string
import urwid
import systeminfo


class Screen(object):
    def __init__(self):
        self.loop = None
        self.cached_widget = None

    def get_title(self):
        return 'Screen title'

    def get_widget(self, loop):
        if self.cached_widget is None:
            self.loop = loop
            self.cached_widget = self.create_widget()

        return self.cached_widget

    def create_widget(self):
        class_name = self.__class__.__name__
        raise NotImplementedError(
            "Class %s doesn't implement create_widget" % class_name
        )

    def activate(self):
        pass

    def deactivate(self):
        pass


class TimeScreen(Screen):
    def __init__(self):
        super().__init__()
        font = urwid.font.HalfBlock7x7Font()
        self.text = urwid.BigText(systeminfo.get_time(), font)

    def get_title(self):
        return 'Time'

    def create_widget(self):
        padded = urwid.Padding(self.text, 'center', 'clip')
        return urwid.Filler(padded)

    def activate(self):
        self.loop.set_alarm_in(0, self.refresh_time)

    def deactivate(self):
        self.loop.remove_alarm(self.alarm_handle)

    def refresh_time(self, loop, user_data):
        self.text.set_text(systeminfo.get_time())
        self.alarm_handle = loop.set_alarm_in(0.1, self.refresh_time)


class WeatherScreen(Screen):
    def __init__(self, service):
        super().__init__()
        self.service = service

        self.loc_text = urwid.Text('')
        font = urwid.font.HalfBlock7x7Font()
        self.temp_text = urwid.BigText('', font)
        self.desc_text = urwid.Text('')
        self.wind_text = urwid.Text('')
        self.hum_text = urwid.Text('')
        self.upd_text = urwid.Text('')

    def get_title(self):
        return 'Weather'

    def create_widget(self):
        overview_pile = urwid.Pile([
            self.loc_text,
            urwid.Padding(self.temp_text, 'left', 'clip')
        ])
        detail_pile = urwid.Pile([
            self.desc_text,
            self.wind_text,
            self.hum_text,
            self.upd_text
        ])
        columns = urwid.Columns([overview_pile, detail_pile], 2)
        padded = urwid.Padding(columns, ('relative', 50), 45)

        self.loop.set_alarm_in(0, self.refresh_weather)
        return urwid.Filler(padded)

    def refresh_weather(self, loop, user_data):
        weather = self.service.get_current_weather()
        self.loc_text.set_text('%s\n' % weather.location)
        self.temp_text.set_text('%sc' % round(weather.temp))
        self.desc_text.set_text('%s\n' % string.capwords(weather.description))
        self.wind_text.set_text('W: %s km/h' % weather.wind_speed)
        self.hum_text.set_text('H: %s%%\n' % weather.humidity)
        self.upd_text.set_text('Updated: %s' % systeminfo.get_time())

        self.loop.set_alarm_in(60*15, self.refresh_weather)


class NewsScreen(Screen):
    def __init__(self, service):
        super().__init__()
        self.service = service
        self.headlines = None

        self.title_text_1 = urwid.Text('', align='center')
        self.summary_text_1 = urwid.Text('')
        self.title_text_2 = urwid.Text('', align='center')
        self.summary_text_2 = urwid.Text('')

    def get_title(self):
        return 'News'

    def create_widget(self):
        wrapped_title_1 = urwid.AttrWrap(self.title_text_1, 'title_text')
        wrapped_title_2 = urwid.AttrWrap(self.title_text_2, 'title_text')
        pile = urwid.Pile([
            wrapped_title_1, self.summary_text_1,
            urwid.Divider('-', 1, 1),
            wrapped_title_2, self.summary_text_2
        ])

        self.loop.set_alarm_in(0, self.refresh_news)
        return urwid.Filler(pile, valign='top')

    def activate(self):
        if self.headlines is None:
            return

        headline = next(self.headlines)
        self.title_text_1.set_text(headline.title)
        self.summary_text_1.set_text(headline.summary)

        headline = next(self.headlines)
        self.title_text_2.set_text(headline.title)
        self.summary_text_2.set_text(headline.summary)

    def refresh_news(self, loop, user_data):
        headlines = self.service.get_current_headlines()
        self.headlines = cycle(headlines)
        self.activate()

        self.loop.set_alarm_in(60*15, self.refresh_news)


class ScreenPager(object):
    def __init__(self, screens):
        self.screens = cycle(screens)
        self.current_screen = None

    def create_widget(self):
        blank = urwid.SolidFill()
        self.container = urwid.WidgetPlaceholder(blank)
        self.outer_box = urwid.LineBox(self.container)

        return urwid.AttrWrap(self.outer_box, 'outer_box')

    def start(self, loop):
        loop.set_alarm_in(0, self.move_next)

    def move_next(self, loop, user_data):
        if self.current_screen is not None:
            self.current_screen.deactivate()

        self.current_screen = next(self.screens)
        self.outer_box.set_title(self.current_screen.get_title())
        self.container.original_widget = self.current_screen.get_widget(loop)
        self.current_screen.activate()

        loop.set_alarm_in(15, self.move_next)
