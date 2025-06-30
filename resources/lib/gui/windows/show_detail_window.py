from resources.lib.gui.windows.base_window import BaseWindow
from resources.lib.database.trakt_sync.shows import TraktSyncDatabase
from resources.lib.modules.globals import g
from resources.lib.modules.navigation import push
from resources.lib.modules.playback import select_preferred_source
import xbmc
import xbmcgui


class ShowDetailWindow(BaseWindow):
    """Display show details with seasons and episode list."""

    def __init__(self, xml_file, location, item_information=None):
        push(None)
        super().__init__(xml_file, location, item_information)
        self.current_season = None

    def onInit(self):
        self.season_list = self.getControlList(2001)
        self.episode_list = self.getControlList(3001)
        self.source_button = self.getControl(2002)
        self.sources = self._get_sources()
        self.selected_source = select_preferred_source(
            self.sources, g.get_int_setting("general.maxResolution", 0)
        )
        self._populate_seasons()
        self._load_selected_season()
        self.set_default_focus(self.season_list)
        super().onInit()

    def _populate_seasons(self):
        self.season_list.reset()
        trakt_id = self.item_information.get("info", {}).get("trakt_id")
        if not trakt_id:
            return
        seasons = TraktSyncDatabase().get_season_list(trakt_id, hide_unaired=False)
        for s in seasons:
            label = s["info"].get("title") or s["info"].get("season")
            li = self.get_list_item_with_properties(s, str(label))
            li.setProperty("trakt_season_id", str(s["trakt_id"]))
            self.season_list.addItem(li)

    def _load_selected_season(self):
        item = self.season_list.getSelectedItem()
        if not item:
            return
        self.current_season = int(item.getProperty("trakt_season_id"))
        self._populate_episodes(self.current_season)

    def _populate_episodes(self, season_id):
        self.episode_list.reset()
        show_id = self.item_information.get("info", {}).get("trakt_id")
        episodes = TraktSyncDatabase().get_episode_list(show_id, season_id)
        for ep in episodes:
            label = (
                f"S{ep['info'].get('season'):02}E{ep['info'].get('episode'):02} - "
                f"{ep['info'].get('title')} ({int(ep['info'].get('duration',0)/60)}m)"
            )
            li = self.get_list_item_with_properties(ep, label)
            url = g.create_url(
                f"plugin://{g.ADDON_ID}",
                {
                    "action": "getSources",
                    "action_args": ep["args"],
                    "preferred": self.selected_source.get("quality"),
                },
            )
            li.setProperty("plugin_url", url)
            self.episode_list.addItem(li)

    def _get_sources(self):
        return [
            {"quality": 1080, "label": "1080p"},
            {"quality": 720, "label": "720p"},
            {"quality": 480, "label": "480p"},
        ]

    def _choose_source(self):
        choices = [s["label"] for s in self.sources]
        idx = xbmcgui.Dialog().select(g.get_language_string(30731), choices)
        if idx != -1:
            self.selected_source = self.sources[idx]

    def handle_action(self, action_id, control_id=None):
        if action_id == 7:
            if control_id == 2001:
                self._load_selected_season()
            elif control_id == 2002:
                self._choose_source()
            elif control_id == 3001:
                item = self.episode_list.getSelectedItem()
                if item:
                    xbmc.executebuiltin(f'RunPlugin("{item.getProperty("plugin_url")}")')

