import json
import requests

from urllib.parse import unquote
from urllib.parse import urlparse

URL = 'https://www.youtube.com/watch?v=DnOFLhBWALE'
GET_VIDEO_URL = 'https://www.youtube.com/get_video_info?video_id={}&el=embedded&hl=en'

def get_page_content(url):
    return requests.get(url).content

def get_video_id(url):
    parsed_url = urlparse(url)
    params_list = parsed_url.query.split('&')
    params_dict = dict()
    for param in params_list:
        equal_index = param.rindex('=')
        params_dict[param[:equal_index]] = param[equal_index+1:]

    video_id = params_dict['v']
    return video_id

def get_video_urls_from_formats(formats):
    video_urls = list()
    for _format in formats:
        if 'url' in _format:
            video_urls.append(_format['url'])
            continue

        key_to_use = None

        if 'signatureCipher' in _format:
            key_to_use = 'signatureCipher'

        if 'cipher' in _format:
            key_to_use = 'cipher'

        cipher = _format[key_to_use]
        cipher_params = cipher.split('&')
        for param in cipher_params:
            key, value = param.split('=')
            if key == 'url':
                video_urls.append(unquote(value))

    return video_urls

def get_uris(youtube_url=None):
    if youtube_url is None:
        youtube_url = URL

    # Get the video id
    video_id = get_video_id(youtube_url)

    # get the content through youtube internal api
    youtube_get_url = GET_VIDEO_URL.format(video_id)
    page_content = requests.get(youtube_get_url).text

    # extract the player response
    params = page_content.split('&')
    params_dict = dict()
    for param in params:
        elems = param.split('=')
        params_dict[elems[0]] = elems[1]

    player_response = params_dict['player_response']
    player_response_unquote = unquote(player_response)

    player_response_dict = json.loads(player_response_unquote)

    # get the different formats and adaptive formats
    streaming_data = player_response_dict['streamingData']
    formats = streaming_data['formats']
    adaptive_formats = streaming_data['adaptiveFormats']

    # get urls from both the formats
    formats_video_urls = get_video_urls_from_formats(formats)
    # adaptive_formats_video_urls = get_video_urls_from_formats(adaptive_formats)
    
    # return formats_video_urls + adaptive_formats_video_urls
    return formats_video_urls

if __name__ == '__main__':
    print(get_uris()[0])

