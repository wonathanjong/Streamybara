"""Simple onboarding wizard for first time setup."""

import xbmc
import xbmcgui

from resources.lib.modules.globals import g


class OnboardingWizard:
    def run(self):
        if g.get_bool_setting("general.onboarding_complete"):
            return

        g.set_runtime_setting("onboarding_active", True)
        try:

            steps = [
                self._welcome,
                self._configure_accounts,
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
        finally:
            g.clear_runtime_setting("onboarding_active")

    def _welcome(self):
        return xbmcgui.Dialog().yesno(
            g.ADDON_NAME,
            g.get_language_string(30700),
            g.get_language_string(30701),
        )

    def _configure_accounts(self):
        options = [
            g.get_language_string(30131),
            g.get_language_string(30339),
            g.get_language_string(30150),
            g.get_language_string(30337),
            g.get_language_string(30564),
        ]
        actions = [
            "authTrakt",
            "authPremiumize",
            "authRealDebrid",
            "authAllDebrid",
        ]
        while True:
            choice = xbmcgui.Dialog().contextmenu(options)
            if choice in (-1, len(options) - 1):
                return True
            xbmc.executebuiltin(
                f"RunPlugin(plugin://{g.ADDON_ID}/?action={actions[choice]})"
            )

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
