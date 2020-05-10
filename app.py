import json
import soco

from flask import Flask, render_template, url_for, request

from get_fb_video_uri import get_uri
from get_yt_video_uri import get_uris

app = Flask(__name__)

sonos = list(soco.discover())[0]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/play_url', methods=['POST'])
def play_url():
    data = json.loads(request.data)
    video_uri = get_uri(data['url'] or None)
    sonos.stop()
    sonos.play_uri(video_uri)
    return 'OK'

@app.route('/play')
def play():
    sonos.play()
    return 'OK'

@app.route('/pause')
def pause():
    sonos.pause()
    return 'OK'

@app.route('/increase')
def increase():
    sonos.volume += 5
    return 'OK'

@app.route('/decrease')
def decrease():
    sonos.volume -= 5
    return 'OK'


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
