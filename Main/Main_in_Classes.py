import vk
from pprint import pprint
import time
import json
import pymongo
from Main.Get_token import Requestlink

def get_photos(vkapi, id):
    time.sleep(0.34)
    photos = vkapi.photos.getAll(owner_id=id, extended=1, skip_hidden=0, count=200, v=5.122, photo_sizes=0, no_service_albums=0)
    return photos


def to_status():
    list_of_values = [('1 — неженат(незамужем)',
                       '2 — встречается',
                       '3 — помолвлен(-а)',
                       '4 — женат(замужем)',
                       '5 — всёсложно',
                       '6 — вактивномпоиске',
                       '7 — влюблен(-а)',
                       '8 — вгражданскомбраке')]
    pprint(list_of_values)
    x = int(input('введите id из предложенного списка:'))
    return x


class VKinder:

    def __init__(self, token):
        session = vk.Session(access_token=token)
        self.vk_api = vk.API(session)
        self.client = pymongo.MongoClient()
        self.searches = self.client['searches']
        self.already_watched_ids = []
        for i in self.searches.Already_watched.find():
            self.already_watched_ids.append(i['user_id'])

    def search(self, to_city, to_age, to_sex, to_stat):
        id_list = []  # сюда добавляются id пользователей

        search = self.vk_api.users.search(sort=0, count=1000, city=to_city, age_from=to_age, age_to=to_age + 1, sex=to_sex, status=to_stat, fields='id', v=5.89)

        print('Людей найдено:', search['count'])

        for i in search['items']:
            id_list.append(i['id'])

        self.id_list = id_list

    def search_city_id(self, city):  # ищет похожие города и регионы, в конце нужно выбрать номер из предложенного поиска
        search = self.vk_api.database.getCities(country_id=1, q=city, need_all=1, count=1000, v=5.122)

        for items in search['items']:
            print(items['title'], ',', items.get('area'), ',', items.get('region'), '-', items['id'])
        to_city = input('введите идентификатор города, из нужного вам региона:')

        return int(to_city)

    def get_user_and_photos_info(self):  # получает id пользователя и список всех его фотографий и добавляет их в список из 10(список может иметь меньшую длинну если пользователей, которых нашла функция search меньше чем 10),
        self.list_of_photos = []         # если пользователь установил приватные настройки, то он не добавляется в список из 10,
        persons_counter = 0              # кроме того пользователи не установившие приватные настройки и установившие отправляются в новый список , а затем отправляются в базу данных для того чтобы при следующем запуске программы по этим пользователям не было итерации
        id_collection = []

        for id in self.id_list:
            if id in self.already_watched_ids:
                continue
            else:
                id_us = {}
                if persons_counter != 10:
                    try:
                        id_photos = get_photos(self.vk_api, id)
                    except Exception as e:
                        print(f'пользователь с id={id} установил приватные настройки', e)
                        id_us['user_id'] = id
                    else:
                        persons_counter += 1
                        user_info = {}
                        user_info['owner_id'] = id
                        user_info['count_of_photos'] = id_photos['count']
                        user_info['items'] = []
                        for items in id_photos['items']:
                            photos_info = {}
                            photos_info['id'] = items['id']
                            photos_info['likes'] = items['likes']['count']
                            photos_info['reposts'] = items['reposts']['count']
                            photos_info['photo_url'] = items['sizes'][-1]['url']
                            user_info['items'].append(photos_info)
                        self.list_of_photos.append(user_info)
                        id_us['user_id'] = id
                else:
                    break
            id_collection.append(id_us)

        self.searches.Already_watched.insert_many(id_collection)

    def sort_top_3_photos(self):  # сортирова 3 популярных фото
        self.dict_photos_and_people = {}
        for items in self.list_of_photos:

            user_id = items['owner_id']

            self.dict_photos_and_people[user_id] = []
            photo_ids = []
            for i in items['items']:
                photo_ids.append((i['id'], i['likes'] + i['reposts']))

            photo_ids = sorted(photo_ids, key=lambda x: x[1], reverse=True)
            if len(photo_ids) > 3:
                photo_ids = photo_ids[:3]

            for items in photo_ids:
                self.dict_photos_and_people[user_id].append(items[0])

    def list_of_objects_to_file(self):  # добавление в финальный список адреса странички пользователя и ссылок на 3 популярные фотографии с его профиля
        self.list_of_objects = []
        for ids in self.dict_photos_and_people.keys():
            object_dict = {}
            object_dict['account_link'] = 'https://vk.com/id' + str(ids)
            object_dict['photo_urls'] = []
            for i in self.dict_photos_and_people[ids]:
                for items in self.list_of_photos:
                    if ids == items['owner_id']:                        # пытался упростить насколько мог
                        for photos_info in items['items']:
                            if i == photos_info['id']:
                                object_dict['photo_urls'].append(photos_info['photo_url'])
            self.list_of_objects.append(object_dict)

    def write_to_file(self):
        with open('search_objects.json', 'w', encoding='utf-8') as file:
            json.dump(self.list_of_objects, file, ensure_ascii=False, indent=2)


#begin


# Obj=Requestlink()
#
# print(Obj.requst_s())   # token:aa7e14e1506de13ea39e0250760441a78e8f8217a073a4f7770b2a13ebd827bdcedbdb92ec3fa369c2d08

Object = VKinder(input('введите токен из url:'))

to_city = Object.search_city_id((input('вввелите город:')))

to_age = int(input('ввелите возраст:'))

to_sex = int(input('введите пол(1-женский, 2-мужской):'))

to_stat = to_status()

Object.search(to_city, to_age, to_sex, to_stat)

Object.get_user_and_photos_info()

Object.sort_top_3_photos()

Object.list_of_objects_to_file()

Object.write_to_file()