import unittest
from unittest.mock import patch
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "resources", "lib"))

import types
sys.modules.setdefault("xbmc", types.ModuleType("xbmc"))
sys.modules.setdefault("xbmcgui", types.ModuleType("xbmcgui"))
sys.modules.setdefault("xbmcvfs", types.ModuleType("xbmcvfs"))
sys.modules.setdefault("xbmcaddon", types.ModuleType("xbmcaddon"))
sys.modules.setdefault("xbmcplugin", types.ModuleType("xbmcplugin"))
mock_uni = types.ModuleType("unidecode")
mock_uni.unidecode = lambda x: x
sys.modules.setdefault("unidecode", mock_uni)
mock_globals = types.ModuleType("resources.lib.modules.globals")
class DummyG:
    def get_language_string(self, _):
        return ""

mock_globals.g = DummyG()
sys.modules.setdefault("resources.lib.modules.globals", mock_globals)
mock_trakt = types.ModuleType("resources.lib.indexers.trakt")
class DummyTrakt:
    def post_json(self, *_, **__):
        pass
    def delete_request(self, *_, **__):
        pass

mock_trakt.TraktAPI = DummyTrakt
sys.modules.setdefault("resources.lib.indexers.trakt", mock_trakt)

from modules import favorites


class TestFavorites(unittest.TestCase):
    def test_like_list_calls_trakt(self):
        with patch('modules.favorites.TraktAPI') as api:
            favorites.like_list(1, 'me')
            api.return_value.post_json.assert_called_with('users/me/lists/1/like', {})

    def test_unlike_list_calls_trakt(self):
        with patch('modules.favorites.TraktAPI') as api:
            favorites.unlike_list(2, 'foo')
            api.return_value.delete_request.assert_called_with('users/foo/lists/2/like')

    def test_toggle_list_like(self):
        with patch('modules.favorites.like_list') as like, patch('modules.favorites.unlike_list') as unlike:
            favorites.toggle_list_like(3, liked=False)
            like.assert_called_once_with(3, 'me')
            favorites.toggle_list_like(3, liked=True)
            unlike.assert_called_once_with(3, 'me')


if __name__ == '__main__':
    unittest.main()
