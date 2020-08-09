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

if __name__ == '__main__':

    # Obj = Requestlink()
    #
    # print(Obj.requst_s())   # token:63ab19d0a064894aa1316fb30ef8170f5883e5994bfe8d8b86976348f132fca387f3690c1a4710850defe

    mas = []

    print(bool(mas))