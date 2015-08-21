import urwid
import systeminfo
from tornado.ioloop import IOLoop
from screens import TimeScreen, WeatherScreen, NewsScreen, ScreenPager
from services import WeatherService, NewsService


class Player(object):
    def __init__(self, screens):
        self.screens = screens
        self.pager = ScreenPager(screens)
        self.date_text = None

        self.palette = [
            ('outer_box', 'yellow', 'black'),
            ('footer', 'white', 'dark red'),
            ('title_text', 'black', 'light gray')
        ]

    def start(self):
        loop = urwid.MainLoop(
            self.create_widget(),
            self.palette,
            event_loop=urwid.TornadoEventLoop(IOLoop()),
            unhandled_input=self.exit_on_q
        )
        self.pager.start(loop)

        loop.set_alarm_in(0, self.refresh_footer)
        loop.run()

    def create_widget(self):
        ip_text = urwid.Text('[%s]' % systeminfo.get_ip(), align='left')
        self.date_text = urwid.Text(systeminfo.get_datetime(), align='right')

        footer = urwid.Columns([ip_text, self.date_text])
        footer = urwid.AttrWrap(footer, 'footer')

        return urwid.Frame(body=self.pager.create_widget(), footer=footer)

    def refresh_footer(self, loop, user_data):
        self.date_text.set_text(systeminfo.get_datetime())
        loop.set_alarm_in(5, self.refresh_footer)

    def exit_on_q(self, key):
        if key in ('q', 'Q'):
            raise urwid.ExitMainLoop()


if __name__ == '__main__':
    api_key = '0643505f637afa8641c4c6a4f626a93f'
    weather_service = WeatherService(api_key, lat=38.84, lon=0.11)
    news_service = NewsService()

    Player([
        TimeScreen(),
        WeatherScreen(weather_service),
        NewsScreen(news_service)
    ]).start()
