#!/usr/bin/env python3
import datetime
from flask import Flask, jsonify, request

import playlist as roks_playlist

API_NAME = 'roks'
API_VERSION = '1'
API_ROOT = f'/{API_NAME}/api/v{API_VERSION}'
app = Flask(__name__)


@app.route(API_ROOT)
def index():
    return "Hello, World!"


@app.route(API_ROOT + '/last')
def last():
    res = roks_playlist._last(obj=True)._asdict()
    c = -2 if not res else 0
    return jsonify({'c': c, 'res': res})


@app.route(API_ROOT + '/playlist')
@app.route(API_ROOT + '/playlist/today')
def playlist_today():
    return playlist(datetime.datetime.today().strftime('%d-%m-%Y'))


@app.route(API_ROOT + '/playlist/<date_str>')
def playlist(date_str):
    count = request.args.get('count')
    if not count:
        count = 0
    else:
        count = int(count)
    res = [
        song._asdict()
        for song in roks_playlist._get_song_list(date_str, count=count)
    ]
    c = -2 if not res else 0

    return jsonify({'c': c, 'res': res})


if __name__ == '__main__':
    app.run()
