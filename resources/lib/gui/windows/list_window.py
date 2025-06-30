from resources.lib.gui.windows.base_window import BaseWindow
from resources.lib.modules.globals import g
from resources.lib.modules.navigation import push
import xbmc
import xbmcgui


class ListWindow(BaseWindow):
    """Full-screen list for showing search results or lists."""

    def __init__(self, xml_file, location, items=None, title="", list_id=None, username="me"):
        self.items = items or []
        self.title = title
        self.list_id = list_id
        self.username = username
        self.liked = False
        push(None)
        super().__init__(xml_file, location)

    def onInit(self):
        self.list_control = self.getControlList(1001)
        header = self.getControl(100)
        if isinstance(header, xbmcgui.ControlLabel):
            header.setLabel(self.title)
        self.heart_button = self.getControl(101)
        if self.list_id is not None:
            label = g.get_language_string(30724)
            if isinstance(self.heart_button, xbmcgui.ControlButton):
                self.heart_button.setLabel(label)
            self.heart_button.setVisible(True)
        else:
            self.heart_button.setVisible(False)
        self.populate_list()
        self.set_default_focus(self.list_control)
        super().onInit()

    def populate_list(self):
        self.list_control.reset()
        for item in self.items:
            label = item.get("name") or item.get("info", {}).get("title", "")
            li = self.get_list_item_with_properties(item, label)
            mediatype = item.get("info", {}).get("mediatype")
            if mediatype == g.MEDIA_MOVIE:
                action = "movieDetails"
            elif mediatype == g.MEDIA_SHOW:
                action = "showDetails"
            else:
                action = "getSources"
            url = g.create_url(
                f"plugin://{g.ADDON_ID}", {"action": action, "action_args": item.get("args")}
            )
            li.setProperty("plugin_url", url)
            self.list_control.addItem(li)

    def handle_action(self, action_id, control_id=None):
        if action_id == 7:
            if control_id == 1001:
                item = self.list_control.getSelectedItem()
                if not item:
                    return
                url = item.getProperty("plugin_url")
                if url:
                    xbmc.executebuiltin(f'RunPlugin("{url}")')
            elif control_id == 101 and self.list_id is not None:
                from resources.lib.modules.favorites import toggle_list_like

                toggle_list_like(self.list_id, self.username, self.liked)
                self.liked = not self.liked
                label_id = 30725 if self.liked else 30724
                if isinstance(self.heart_button, xbmcgui.ControlButton):
                    self.heart_button.setLabel(g.get_language_string(label_id))
