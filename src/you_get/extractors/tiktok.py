#!/usr/bin/env python

__all__ = ['tiktok_download']

from ..common import *

def tiktok_download(url, output_dir='.', merge=True, info_only=False, **kwargs):
    while True:
        m = re.match('https://([^/]+)(/.*)', url)
        host = m.group(1)
        if host == 'www.tiktok.com':  # canonical URL reached
            url = m.group(2).split('?')[0]
            vid = url.split('/')[3]  # should be a string of numbers
            break
        else:
            url = get_location(url)

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0',
        'Accept-Encoding': 'gzip, deflate',
        'Accept': '*/*',
        'Connection': 'keep-alive'  # important
    }

    html = getHttps(host, url, headers=headers)
    data = r1(r'window\[\'SIGI_STATE\'\]=(.*?);window\[\'SIGI_RETRY\'\]', html)
    info = json.loads(data)
    downloadAddr = info['ItemModule'][vid]['video']['downloadAddr']
    author = info['ItemModule'][vid]['author']  # same as uniqueId
    nickname = info['UserModule']['users'][author]['nickname']
    title = '%s [%s]' % (nickname or author, vid)

    mime, ext, size = url_info(downloadAddr, headers=headers)

    print_info(site_info, title, mime, size)
    if not info_only:
        download_urls([downloadAddr], title, ext, size, output_dir=output_dir, merge=merge, headers=headers)

site_info = "TikTok.com"
download = tiktok_download
download_playlist = playlist_not_supported('tiktok')