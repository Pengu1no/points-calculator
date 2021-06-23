import json
from pathlib import Path

BASE_DIR = Path(__file__).parent
ICON_DIR = BASE_DIR / 'icons'


class Settings:
    __DEFAULTS = {
        'types_match': {
            2: ('o', '#000000', 'Грунт'),
            3: ('v', '#000000', 'Низкая растительность (трава)'),
            4: ('^', '#000000', 'Средняя растительность (кусты)'),
            5: ('s', '#000000', 'Высокая растительность (деревья)'),
            6: ('*', '#000000', 'Здания (крыши)'),
            7: ('d', '#000000', 'Ложно отражённые точки'),
            8: ('.', '#000000', 'Неизвестно'),
        },
        'background_color': '#ffffff',
    }

    __SETTINGS_FILE = BASE_DIR / 'proj.settings.json'

    __MARKERS = {
        '.': ICON_DIR / 'm00.png',
        ',': ICON_DIR / 'm01.png',
        'o': ICON_DIR / 'm02.png',
        'v': ICON_DIR / 'm03.png',
        '^': ICON_DIR / 'm04.png',
        '<': ICON_DIR / 'm05.png',
        '>': ICON_DIR / 'm06.png',
        '1': ICON_DIR / 'm07.png',
        '2': ICON_DIR / 'm08.png',
        '3': ICON_DIR / 'm09.png',
        '4': ICON_DIR / 'm10.png',
        '8': ICON_DIR / 'm11.png',
        's': ICON_DIR / 'm12.png',
        'p': ICON_DIR / 'm13.png',
        '*': ICON_DIR / 'm14.png',
        'h': ICON_DIR / 'm15.png',
        'H': ICON_DIR / 'm16.png',
        '+': ICON_DIR / 'm17.png',
        'x': ICON_DIR / 'm18.png',
        'D': ICON_DIR / 'm19.png',
        'd': ICON_DIR / 'm20.png',
        '|': ICON_DIR / 'm21.png',
        '_': ICON_DIR / 'm22.png',
        'P': ICON_DIR / 'm23.png',
        'X': ICON_DIR / 'm24.png',
    }

    __COLORS = {
        'b': 'Синий',
        'g': 'Зеленый',
        'r': 'Красный',
        'c': 'Голубой',
        'm': 'Пурпурный',
        'y': 'Оливковый',
        'k': 'Черный',
    }

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Settings, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        if not self.__SETTINGS_FILE.exists():
            self.save_settings()

        self.import_settings()

    def __getattr__(self, item):
        try:
            return self.__getattribute__(item)
        except AttributeError:
            return self.__DEFAULTS[item]

    @property
    def colors(self):
        return self.__COLORS

    @property
    def colors_rev(self):
        return {v: k for k, v in self.__COLORS.items()}

    @property
    def markers(self):
        return self.__MARKERS

    @property
    def markers_rev(self):
        return {v: k for k, v in self.__MARKERS.items()}

    def save_settings(self):
        with open(self.__SETTINGS_FILE, 'w') as _file:
            try:
                _match = self.__getattribute__('types_match')
            except AttributeError:
                _match = self.__DEFAULTS['types_match']

            try:
                _background_color = self.__getattribute__('background_color')
            except AttributeError:
                _background_color = self.__DEFAULTS['background_color']

            _file.write(json.dumps({
                'types_match': _match,
                'background_color': _background_color,
            }))

    def import_settings(self):
        with open(self.__SETTINGS_FILE, 'r') as _file:
            _settings = json.loads(_file.read())
            for k, v in _settings.items():
                self.__setattr__(k, v)

    def save_type_match(self, match):
        self.__setattr__('types_match', match)
        self.save_settings()
        self.import_settings()

    def save_background_color(self, color):
        self.__setattr__('background_color', color)
        self.save_settings()
        self.import_settings()
