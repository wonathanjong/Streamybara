from resources.lib.gui.windows.base_window import BaseWindow
from resources.lib.modules.globals import g
from resources.lib.database.trakt_sync.bookmark import TraktSyncDatabase
from resources.lib.database.trakt_sync.movies import (
    TraktSyncDatabase as MoviesDatabase,
)
from resources.lib.modules.listsHelper import ListsHelper
import xbmcgui
import xbmc


class HomeWindow(BaseWindow):
    """Simple home window with top navigation bar."""

    def __init__(self, xml_file, location):
        super().__init__(xml_file, location)

    def onInit(self):
        self.nav_list = self.getControlList(1001)
        self.continue_list = self.getControlList(2001)
        self.continue_more = self.getControl(2002)
        self.lists_list = self.getControlList(3001)
        self.lists_more = self.getControl(3002)
        self.recommend_list = self.getControlList(4001)
        self.recommend_more = self.getControl(4002)
        self._populate_nav()
        self._populate_continue()
        self._populate_trakt_lists()
        self._populate_recommendations()
        self.set_default_focus(self.nav_list)
        super().onInit()

    def _populate_nav(self):
        self.nav_list.reset()
        items = [
            (30709, ""),
            (30710, "showsHome"),
            (30711, "moviesHome"),
            (30712, "myTraktLists&mediatype=movies"),
            (30713, "openSearch"),
            (30714, "openSettings"),
        ]
        for label_id, action in items:
            item = xbmcgui.ListItem(g.get_language_string(label_id))
            item.setProperty("action", action)
            self.nav_list.addItem(item)

    def _populate_continue(self):
        self.continue_list.reset()
        self.continue_items = []
        bookmark_db = TraktSyncDatabase()
        items = (
            bookmark_db.get_all_bookmark_items("movie")
            + bookmark_db.get_all_bookmark_items("episode")
        )[:10]
        for item in items:
            li = self.get_list_item_with_properties(item, item.get("name", ""))
            li.setProperty("action", "getSources")
            li.setProperty("action_args", item.get("args", ""))
            url = g.create_url(
                f"plugin://{g.ADDON_ID}", {"action": "getSources", "action_args": item.get("args", "")}
            )
            li.setProperty("plugin_url", url)
            self.continue_list.addItem(li)
            self.continue_items.append(item)

    def _populate_trakt_lists(self):
        self.lists_list.reset()
        self.trakt_list_items = []
        lists = ListsHelper().lists_database.extract_trakt_page(
            "users/me/lists", "movie", page=1, pull_all=True, ignore_cache=True
        )
        for item in lists[:10]:
            li = self.get_list_item_with_properties(item, item["info"]["name"])
            li.setProperty("action", "traktList")
            args = {
                "trakt_id": item["info"]["trakt_id"],
                "username": item["info"].get("username", "me"),
            }
            url = g.create_url(f"plugin://{g.ADDON_ID}", {"action": "traktList", "action_args": args})
            li.setProperty("plugin_url", url)
            self.lists_list.addItem(li)
            self.trakt_list_items.append(item)

    def _populate_recommendations(self):
        self.recommend_list.reset()
        self.recommend_items = []
        if not g.get_setting("trakt.auth"):
            return
        recs = MoviesDatabase().extract_trakt_page(
            "recommendations/movies", extended="full", page=1
        )
        for item in recs[:10]:
            li = self.get_list_item_with_properties(
                item, item["info"].get("title", "")
            )
            url = g.create_url(
                f"plugin://{g.ADDON_ID}",
                {"action": "movieDetails", "action_args": item["args"]},
            )
            li.setProperty("plugin_url", url)
            self.recommend_list.addItem(li)
            self.recommend_items.append(item)

    def handle_action(self, action_id, control_id=None):
        if action_id == 7:
            if control_id == 1001:
                item = self.nav_list.getSelectedItem()
                if not item:
                    return
                action = item.getProperty("action")
                if action == "openSearch":
                    self._open_search()
                elif action:
                    xbmc.executebuiltin(
                        f'RunPlugin("plugin://{g.ADDON_ID}/?action={action}")'
                    )
                else:
                    xbmc.executebuiltin(f'RunPlugin("plugin://{g.ADDON_ID}")')
                return
            elif control_id in (2001, 3001, 4001):
                control = self.getControlList(control_id)
                item = control.getSelectedItem()
                if not item:
                    return
                url = item.getProperty("plugin_url")
                if not url:
                    action = item.getProperty("action")
                    args = item.getProperty("action_args")
                    url = g.create_url(
                        f"plugin://{g.ADDON_ID}", {"action": action, "action_args": args}
                    )
                xbmc.executebuiltin(f'RunPlugin("{url}")')
                return
            elif control_id == 2002:
                self._open_more_continue()
            elif control_id == 3002:
                self._open_more_lists()
            elif control_id == 4002:
                self._open_more_recommendations()
            return

    def _open_search(self):
        from resources.lib.modules.search import search_movies
        from resources.lib.gui.windows.list_window import ListWindow
        from resources.lib.database.skinManager import SkinManager

        query = xbmcgui.Dialog().input(g.get_language_string(30713))
        if not query:
            return
        results = search_movies(query)
        if not results:
            xbmcgui.Dialog().ok(g.ADDON_NAME, g.get_language_string(30717))
            return
        window = ListWindow(
            *SkinManager().confirm_skin_path("list.xml"),
            items=results,
            title=g.get_language_string(30717) % query,
        )
        window.doModal()
        del window

    def _open_more_continue(self):
        from resources.lib.gui.windows.list_window import ListWindow
        from resources.lib.database.skinManager import SkinManager

        window = ListWindow(
            *SkinManager().confirm_skin_path("list.xml"),
            items=self.continue_items,
            title=g.get_language_string(30715),
        )
        window.doModal()
        del window

    def _open_more_lists(self):
        from resources.lib.gui.windows.list_window import ListWindow
        from resources.lib.database.skinManager import SkinManager

        window = ListWindow(
            *SkinManager().confirm_skin_path("list.xml"),
            items=self.trakt_list_items,
            title=g.get_language_string(30716),
        )
        window.doModal()
        del window

    def _open_more_recommendations(self):
        from resources.lib.gui.windows.list_window import ListWindow
        from resources.lib.database.skinManager import SkinManager

        window = ListWindow(
            *SkinManager().confirm_skin_path("list.xml"),
            items=self.recommend_items,
            title=g.get_language_string(30723),
        )
        window.doModal()
        del window

