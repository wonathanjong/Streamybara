from resources.lib.gui.windows.base_window import BaseWindow
from resources.lib.database.trakt_sync.movies import TraktSyncDatabase
from resources.lib.modules.globals import g
from resources.lib.modules.navigation import push
from resources.lib.common import tools
from resources.lib.modules.playback import select_preferred_source
import xbmc
import xbmcgui


class MovieDetailWindow(BaseWindow):
    """Display details for a movie with play controls and recommendations."""

    def __init__(self, xml_file, location, item_information=None):
        push(None)
        super().__init__(xml_file, location, item_information)

    def onInit(self):
        self.play_button = self.getControl(2001)
        self.source_button = self.getControl(2002)
        self.recommend_list = self.getControlList(3001)
        self.sources = self._get_sources()
        self.selected_source = select_preferred_source(
            self.sources, g.get_int_setting("general.maxResolution", 0)
        )
        self._populate_recommendations()
        self.set_default_focus(control_id=2001)
        super().onInit()

    def _populate_recommendations(self):
        self.recommend_list.reset()
        trakt_id = self.item_information.get("info", {}).get("trakt_id")
        if not trakt_id:
            return
        recs = TraktSyncDatabase().extract_trakt_page(
            f"movies/{trakt_id}/related", extended="full", page=1
        )
        for item in recs[:10]:
            li = self.get_list_item_with_properties(item, item["info"]["title"])
            url = g.create_url(
                f"plugin://{g.ADDON_ID}",
                {"action": "movieDetails", "action_args": item["args"]},
            )
            li.setProperty("plugin_url", url)
            self.recommend_list.addItem(li)

    def _get_sources(self):
        return [
            {"quality": 1080, "label": "1080p"},
            {"quality": 720, "label": "720p"},
            {"quality": 480, "label": "480p"},
        ]

    def _choose_source(self):
        choices = [s["label"] for s in self.sources]
        index = xbmcgui.Dialog().select(g.get_language_string(30731), choices)
        if index != -1:
            self.selected_source = self.sources[index]

    def handle_action(self, action_id, control_id=None):
        if action_id == 7:
            if control_id == 2001:
                url = g.create_url(
                    f"plugin://{g.ADDON_ID}",
                    {
                        "action": "getSources",
                        "action_args": self.item_information.get("args"),
                        "preferred": self.selected_source.get("quality"),
                    },
                )
                xbmc.executebuiltin(f'RunPlugin("{url}")')
            elif control_id == 2002:
                self._choose_source()
            elif control_id == 3001:
                item = self.recommend_list.getSelectedItem()
                if item:
                    xbmc.executebuiltin(f'RunPlugin("{item.getProperty("plugin_url")}")')

