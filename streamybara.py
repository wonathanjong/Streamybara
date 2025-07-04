import sys

from resources.lib.modules import router
from resources.lib.modules.globals import g
from resources.lib.gui.onboarding import OnboardingWizard
from resources.lib.modules.streamybaraMonitor import ONWAKE_NETWORK_UP_DELAY
from resources.lib.modules.timeLogger import TimeLogger


def _sleeping_retry_handler():
    sleeping = False

    if g.PLATFORM == "android":
        attempts = 0
        while (
            attempts <= ONWAKE_NETWORK_UP_DELAY
            and (sleeping := g.get_bool_runtime_setting("system.sleeping", False))
            and not g.wait_for_abort(1)
        ):
            attempts += 1
        if sleeping and not g.abort_requested():
            g.log(
                f"Ignoring {g.REQUEST_PARAMS.get('action', '')} plugin action as system is supposed to be \"sleeping\"",
                "info",
            )

    return not sleeping


def streamybara_endpoint():
    try:
        g.init_globals(sys.argv)

        if _sleeping_retry_handler() and not g.abort_requested():
            OnboardingWizard().run()
            if not g.get_bool_setting("general.onboarding_complete"):
                return
            with TimeLogger(f"{g.REQUEST_PARAMS.get('action', '')}"):
                router.dispatch(g.REQUEST_PARAMS)

    except Exception:
        g.cancel_directory()
        raise

    finally:
        g.deinit()


if __name__ == "__main__":  # pragma: no cover
    streamybara_endpoint()
