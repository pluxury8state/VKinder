import unittest
from Main.Main_in_Classes import VKinder as vk
import pymongo
from pprint import pprint
import json
from tests.data_test import data
from tests.data_to_test_list_of_objects_to_file import data_dict_of_photos_and_people, data_list_of_photos


class TestVKinder(unittest.TestCase):

    def setUp(self):#token:
        self.obj = vk('c9bbbe5274c51ed456346b91da5f413ef86fa19f598f61f0c19114c2579bf1ea820275f8275cc9c2caf4c')

    def test_search(self):

        self.obj.search(2, 18, 1, 6)
        self.assertIsNotNone(self.obj.id_list)

    def test_get_user_and_photos_info(self):
        self.obj.client = pymongo.MongoClient()
        self.obj.searches = self.obj.client['test_13']
        self.obj.already_watched_ids = []
        self.obj.id_list = [301899876, 301200789, 275751557, 441019152, 388692919, 506248072, 503531122, 464586548, 456003705, 475383464, 235613977, 475058473, 464586548]
        self.obj.get_user_and_photos_info()
        with open('test_data', 'w', encoding='utf-8') as file:
            json.dump(self.obj.list_of_photos, file, ensure_ascii=False, indent=2)
        ids = []
        for i in self.obj.searches.Already_watched.find():
            ids.append(i['user_id'])
        pprint(ids)
        print(len(ids))
        self.assertEqual(len(ids), 13)
        self.assertEqual(len(self.obj.list_of_photos), 10)
        self.obj.already_watched_ids = ids
        self.obj.get_user_and_photos_info()
        self.assertEqual(len(self.obj.list_of_photos), 0)
        self.obj.searches.drop_collection('Already_watched')



    def test_sort_top_3_photos(self):
        self.obj.list_of_photos = data
        self.obj.sort_top_3_photos()

        self.assertLessEqual(len(self.obj.dict_photos_and_people[301899876]), 3)
        for photo in self.obj.dict_photos_and_people[301899876]:
            self.assertIn(photo, [456245053, 456243508, 456241206])
        self.assertLessEqual(len(self.obj.dict_photos_and_people[441019152]), 3)
        for photo in self.obj.dict_photos_and_people[441019152]:
            self.assertIn(photo, [456239345, 456241636, 456239838])

    def test_list_of_objects_to_file(self):
        self.obj.dict_photos_and_people = data_dict_of_photos_and_people
        self.obj.list_of_photos = data_list_of_photos
        self.obj.list_of_objects_to_file()
        ids = ['241041574', '233162309']
        self.assertIn(ids[0], self.obj.list_of_objects[0]['account_link'])
        self.assertLessEqual(len(self.obj.list_of_objects[0]['photo_urls']), 3)
        self.assertIn(ids[1], self.obj.list_of_objects[1]['account_link'])
        self.assertLessEqual(len(self.obj.list_of_objects[1]['photo_urls']), 3)
