import unittest
from Main.Main_in_Classes import VKinder
from Main.Main_in_Classes import get_photos
from Main.Main_in_Classes import to_status
from unittest.mock import patch

class TestVKinder(unittest.TestCase):

    def SetUp(self):#token:
        self.initial = VKinder('aa7e14e1506de13ea39e0250760441a78e8f8217a073a4f7770b2a13ebd827bdcedbdb92ec3fa369c2d08')

    def test_search(self):
        with patch('VKinder.input', side_effect=['1']):
            answer = self.initial.search_city_id('Спб')

        self.assertEqual(answer, 2)


