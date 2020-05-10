import requests

from urllib.parse import unquote

from bs4 import BeautifulSoup

URL = 'https://www.facebook.com/HollandDrums/videos/174825810457310/'

def get_uri(facebook_url=None):
    if facebook_url is None:
        facebook_url = URL

    facebook_url = facebook_url.replace('www', 'm')
    page_content = requests.get(facebook_url).text

    bs_parse = BeautifulSoup(page_content, features='html.parser')
    wide_pic_div = bs_parse.find('div', {'class': 'widePic'})
    wide_div_href = wide_pic_div.a.attrs['href']
    video_source = wide_div_href[wide_div_href.index('=')+1:]

    return unquote(video_source)

