from urllib.parse import urlencode


class Requestlink:

    def requst_s(self):
        quath = 'https://oauth.vk.com/authorize'
        params = {
            'client_id': 7507933,
            'display_page': 'page',
            'scope': 'friends,users,database,photos',
            'response_type': 'token',
            'v' : 5.89
        }
        url = ('?'.join((quath, urlencode(params))))
        return url