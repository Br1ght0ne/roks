from bs4 import BeautifulSoup
import datetime
import re
import requests
from song import Song
from utils import log

API_URL = "https://radioroks.ua/playlist/{}.html"
_DATE_STR_REGEX = r'\d{2}-\d{2}-\d{4}'


def _fetch(_date_str: str):
    'Fetch HTML from server and return the page.'
    log(f'Fetching playlist for {_date_str}...')
    res = requests.get(API_URL.format(_date_str))
    res.encoding = 'utf-8'
    page = res.text
    log('Fetch success!')
    return page


def _get_song_list(date_str=None, count=None) -> [Song]:
    'Parse the page and return the list of songs.'
    if not date_str or date_str.lower() == '_today':
        date_str = _today_str()
    page = _fetch(date_str)
    soup = BeautifulSoup(page, 'html.parser')
    song_lists_html = soup.find_all(class_='song-list')

    songs = []
    for song_list_html in song_lists_html:
        time = song_list_html.find(class_='songTime').text
        song_html = song_list_html.find('div', class_='play-button-youtube')
        if song_html:
            singer = song_html['data-singer']
            title = song_html['data-song']
            video = song_html['data-video']
            singer_url = song_html['data-singer-url']
            song_url = song_html['data-song-url']
            song = Song(time, singer, title, video, singer_url, song_url)
            songs.append(song)
    if count and count >= 1:
        return songs[0:count]
    else:
        return songs


def _today_str():
    return datetime.datetime.today().strftime('%d-%m-%Y')


def playlist(command='', count=None):
    if command == 'today' or not command:
        print(_today(count=count))
    elif isinstance(command, int):
        print(_today(count=command))
    elif re.match(_DATE_STR_REGEX, command):
        print(_to_str(_get_song_list(command, count=count)))


def _to_str(song_list):
    return '\n'.join(map(str, song_list))


def _today(count=None):
    "Return playlist of today's songs, separated by newlines."
    return _to_str(_get_song_list(_today_str(), count=count))


def last():
    print(_last())


def _last(obj=False):
    'Return last played song.'
    song = _get_song_list(_today_str(), count=1)[0]
    if obj:
        return song
    else:
        return str(song)
