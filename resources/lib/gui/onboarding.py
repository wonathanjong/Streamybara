"""Simple onboarding wizard for first time setup."""

import xbmcgui
import xbmc

from resources.lib.modules.globals import g
from resources.lib.modules.validation import verify_provider, verify_trakt


class OnboardingWizard:
    def run(self):
        if g.get_bool_setting("general.onboarding_complete"):
            return

        steps = [
            self._welcome,
            self._configure_provider,
            self._configure_trakt,
            self._configure_scraper,
            self._select_resolution,
        ]
        for step in steps:
            if g.abort_requested():
                return
            if not step():
                return
        g.set_setting("general.onboarding_complete", True)
        xbmcgui.Dialog().ok(g.ADDON_NAME, g.get_language_string(30704))

    def _welcome(self):
        return xbmcgui.Dialog().yesno(
            g.ADDON_NAME,
            g.get_language_string(30700),
            g.get_language_string(30701),
        )

    def _configure_provider(self):
        options = ["Real-Debrid", "AllDebrid"]
        while True:
            choice = xbmcgui.Dialog().select(
                g.get_language_string(30702), options
            )
            if choice == -1:
                return False
            while True:
                token = xbmcgui.Dialog().input(g.get_language_string(30726))
                if token is None:
                    return False
                if verify_provider(token):
                    g.set_setting("debrid.provider", options[choice])
                    g.set_setting("debrid.token", token)
                    return True
                xbmcgui.Dialog().ok(g.ADDON_NAME, g.get_language_string(30727))

    def _configure_trakt(self):
        if not xbmcgui.Dialog().yesno(
            g.ADDON_NAME,
            g.get_language_string(30707),
        ):
            return False
        while True:
            key = xbmcgui.Dialog().input(g.get_language_string(30728))
            if not key:
                return False
            if verify_trakt(key):
                g.set_setting("trakt.api_key", key)
                break
            xbmcgui.Dialog().ok(g.ADDON_NAME, g.get_language_string(30729))
        return True

    def _configure_scraper(self):
        text = xbmcgui.Dialog().input(
            g.get_language_string(30705),
            type=xbmcgui.INPUT_ALPHANUM,
        )
        if text is None:
            return False
        if text:
            g.set_setting("scraper.url", text)
        return True

    def _select_resolution(self):
        labels = [
            g.get_language_string(30598),
            g.get_language_string(30599),
            g.get_language_string(30600),
            g.get_language_string(30601),
        ]
        choice = xbmcgui.Dialog().select(
            g.get_language_string(30706), labels
        )
        if choice == -1:
            return False
        g.set_setting("general.maxResolution", choice)
        return True
