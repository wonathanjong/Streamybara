# Development Guidelines

- Run `python -m py_compile streamybara.py resources/lib/gui/onboarding.py resources/lib/gui/windows/home_window.py resources/lib/gui/windows/list_window.py resources/lib/gui/windows/movie_detail_window.py resources/lib/gui/windows/show_detail_window.py resources/lib/modules/router.py resources/lib/modules/search.py resources/lib/modules/favorites.py` before committing.
- Execute tests via `pytest -q`.
- Keep translations synchronized across all language files; use the English text if you don't have localized strings.
- Update the README whenever a UI element or workflow changes.
