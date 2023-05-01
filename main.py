#!bin/python3

import ytmusicapi

from json import load
from requests import get, post
from time import sleep


with open('keys.json') as keys:
    keys = load(keys)


ytmusic_headers = f'''User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:72.0) Gecko/20100101 Firefox/72.0
Accept: */*
Authorization: SAPISIDHASH 1682891956_5f0475dd184fad517bc107e7aafde36807568082
Accept-Language: en-US,en;q=0.5
Content-Type: application/json
X-Goog-AuthUser: 0
x-origin: https://music.youtube.com
Cookie: {keys['ytmusic_cookie']}'''


def get_spotify_artists(url: str = 'https://api.spotify.com/v1/me/following?type=artist', artists: set = set()):
    headers = {'Authorization': f'Bearer {keys["spotify"]}', 'limit': '50'}
    # avoid getting kicked
    sleep(0.1)
    res = get(
        url,
        headers=headers
    )
    if res.status_code != 200:
        raise Exception('f"[ERROR] {res.reason}"')
    else:
        data = res.json()['artists']
        results = data['items']
        for result in results:
            artists.add(result['name'])
        next = data['next']
        if next:
            return get_spotify_artists(next, artists)
        else:
            return artists


def get_channel_id(artist: str, browse_id: str):
    headers = {
        'Referer': 'https://music.youtube.com/search?q=supertramp',
        'Cookie': keys['ytmusic_cookie'],
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.4 Safari/605.1.15',
        'Host': 'music.youtube.com',
        'Origin': 'https://music.youtube.com',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Site': 'same-origin',
        'Connection': 'keep-alive',
        'Authorization': 'SAPISIDHASH 1682900089_766fe8ad43b8440910e5e7f7c812465756ad99aa',
        'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
        'Accept': '*/*',
        'Content-Type': 'application/json',
        'Sec-Fetch-Mode': 'same-origin',
        'X-Goog-Visitor-Id': 'Cgs0WEtGX0c2QmRKZyjwgbyiBg%3D%3D',
        'X-Goog-AuthUser': '0',
        'X-Youtube-Bootstrap-Logged-In': 'true',
        'X-Youtube-Client-Name': '67',
        'X-Origin': 'https://music.youtube.com',
        'X-Youtube-Client-Version': '1.20230424.01.00',
    }
    json_data = {
        'context': {
            'client': {
                'hl': 'es',
                'gl': 'AR',
                'remoteHost': '190.189.233.107',
                'deviceMake': 'Apple',
                'deviceModel': '',
                'visitorData': 'Cgs0WEtGX0c2QmRKZyjwgbyiBg%3D%3D',
                'userAgent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.4 Safari/605.1.15,gzip(gfe)',
                'clientName': 'WEB_REMIX',
                'clientVersion': '1.20230424.01.00',
                'osName': 'Macintosh',
                'osVersion': '10_15_7',
                'originalUrl': f'https://music.youtube.com/channel/{browse_id}',
                'platform': 'DESKTOP',
                'clientFormFactor': 'UNKNOWN_FORM_FACTOR',
                'configInfo': {
                    'appInstallData': 'CPCBvKIGEKC3_hIQzN-uBRCqsv4SENf_rgUQzK7-EhDWn68FELeRrwUQ25uvBRC4i64FEOSz_hIQ86ivBRCvn68FEIKdrwUQ_bj9EhC9tq4FEOf3rgUQpZmvBQ%3D%3D',
                },
                'userInterfaceTheme': 'USER_INTERFACE_THEME_DARK',
                'timeZone': 'America/Buenos_Aires',
                'browserName': 'Safari',
                'browserVersion': '16.4',
                'acceptHeader': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'deviceExperimentId': 'ChxOekl5TnprNU5qazFOemMzTVRJNE1qSTFOUT09EPCBvKIGGPCBvKIG',
                'screenWidthPoints': 2005,
                'screenHeightPoints': 582,
                'screenPixelDensity': 1,
                'screenDensityFloat': 1,
                'utcOffsetMinutes': -180,
                'musicAppInfo': {
                    'pwaInstallabilityStatus': 'PWA_INSTALLABILITY_STATUS_UNKNOWN',
                    'webDisplayMode': 'WEB_DISPLAY_MODE_BROWSER',
                    'storeDigitalGoodsApiSupportStatus': {
                        'playStoreDigitalGoodsApiSupportStatus': 'DIGITAL_GOODS_API_SUPPORT_STATUS_UNSUPPORTED',
                    },
                },
            },
            'request': {
                'useSsl': True
            }
        },
        'query': artist
    }
    sleep(0.1)
    response = post(
        'https://music.youtube.com/youtubei/v1/search',
        headers=headers,
        json=json_data,
    )

    if response.status_code == 200:
        contents = response.json().get('contents', {})
        search_result_renderer = contents.get('tabbedSearchResultsRenderer', {})
        tabs = search_result_renderer.get('tabs', [])
        if tabs:
            tab = tabs[0]
            tab_renderer = tab.get('tabRenderer', {})
            content = tab_renderer.get('content', {})
            section_list = content.get('sectionListRenderer', {})
            contents_sec = section_list.get('contents', [])
            if contents_sec:
                con_sec = contents_sec[0]
                music_card = con_sec.get('musicCardShelfRenderer', {})
                menu = music_card.get('menu', {})
                menu_renderer = menu.get('menuRenderer', {})
                menu_items = menu_renderer.get('items', [])
                if menu_items:
                    sub_button = menu_items[2]
                    toggle_menu_serv = sub_button.get('toggleMenuServiceItemRenderer', {})
                    service_ep = toggle_menu_serv.get('defaultServiceEndpoint', {})
                    channel_wrapper = service_ep.get('subscribeEndpoint', {})
                    channel_ids = channel_wrapper.get('channelIds', [])
                    if channel_ids:
                        return channel_ids[0]
                    return None
                return None
            return None
        return None
    return None


if __name__ == '__main__':
    artists = set()
    browse_ids = {}
    channel_ids = []
    auth = ytmusicapi.setup(headers_raw=str(ytmusic_headers))
    ytmusic = ytmusicapi.YTMusic(auth=auth)
    print('[INFO] attempting to retrieve spotify artists.')
    artists = get_spotify_artists(artists=artists)
    print(f'[INFO] Captured {len(artists)} artists from your spotify account.')
    print('[INFO] Capturing youtube music browse artist ids...')
    for artist in artists:
        res = ytmusic.search(query=artist, filter='artists')
        if res and res[0].get('browseId') is not None:
            browse_ids[artist.lower()] = res[0]['browseId']
    print('[INFO] Retrieving channel ids from artists')
    for browse in browse_ids:
        channel_id = get_channel_id(artist=browse, browse_id=browse_ids[browse])
        if channel_id is not None:
            channel_ids.append(channel_id)
    print(f'[INFO] We got {len(channel_ids)} channel ids.')
    print('[INFO] Starting subscription process..')
    for artist in channel_ids:
        sleep(0.1)
        res = ytmusic.subscribe_artists([artist])
    print('[INFO] Done subscribing you, enjoy!')



