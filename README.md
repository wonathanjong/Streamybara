[![Kodi version](https://img.shields.io/badge/kodi%20versions-19--20-blue)](https://kodi.tv/)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
![CI](https://github.com/StreamybaraKodi/StreamybaraDevelopment/workflows/CI/badge.svg?branch=v2-Development)
[![codecov](https://codecov.io/gh/StreamybaraKodi/StreamybaraDevelopment/branch/v2-Development/graph/badge.svg?token=LCX9WOPJ2M)](https://codecov.io/gh/StreamybaraKodi/StreamybaraDevelopment)
[![License: GPL3](https://img.shields.io/badge/License-GPL3-yellow.svg)](https://opensource.org/licenses/GPL-3.0)

# Streamybara (plugin.video.streamybara)

Streamybara is a multi-source addon for Kodi with the added ability to install custom provider modules. Unlike other Kodi addons which are generally built for a single service use, Streamybara allows users to connect to multiple online/offline services at once for their viewing with a single click.

The add-on now includes a first-run onboarding wizard guiding you through
configuring debrid providers, connecting your Trakt account, adding a scraper
source and choosing a preferred resolution profile. The wizard runs automatically the
first time Streamybara launches and can later be accessed from the settings menu.
Resolution profiles include **Highest**, **High**, **Medium**, and **Low** which
select streams based on resolution and file size.

A modern home screen provides a simple navigation bar with quick access to
Home, TV, Movies, your Trakt lists, search and settings. Selecting **My Lists**
opens a menu showing all of your saved Trakt lists. Content rows now include a
"Continue Watching" carousel built from your Trakt bookmarks, a carousel for
each of your personal Trakt lists and a row of recommended movies when you are
signed into Trakt.

Search is now accessible from the navigation bar and shows results in a
dedicated list view with vertical scrolling.

Trakt lists opened in this list view include a heart button in the header to
add or remove the list from your liked lists.

Selecting any title now opens a detail page with a play button,
rich metadata and related recommendations. A new **Select Source** button lets
you override the resolution chosen from your preference setting.
Home carousels now feature a **More** button to view entire rows and a simple
back stack remembers your previous screens. The onboarding wizard verifies the
format of your provider token and Trakt API key so setup will not finish until
valid details are entered.

## Contribution

Install all dependencies in requirements.txt
```shell
pip install -r requirements.txt
```

Configure hooks for automated pre commit changes:
```sh
pre-commit install
```
Ensure that `git` is available in your PATH

## Running Tests

Execute the following to run lint checks and unit tests:

```bash
python -m py_compile streamybara.py resources/lib/gui/onboarding.py \
    resources/lib/gui/windows/home_window.py \
    resources/lib/gui/windows/list_window.py \
    resources/lib/gui/windows/movie_detail_window.py \
    resources/lib/gui/windows/show_detail_window.py \
    resources/lib/modules/router.py resources/lib/modules/search.py \
    resources/lib/modules/favorites.py
pytest -q
```

## Packaging for Kodi

To test the add-on on another device, create a zip archive of the plugin
directory. Kodi can install zipped add-ons through the **Install from zip file**
option in the Add-on Browser.

```bash
cd ..
zip -r plugin.video.streamybara.zip plugin.video.streamybara -x '*.git*' 'tests/*'
```

Copy `plugin.video.streamybara.zip` to your Kodi system and install it via the Add-on
Browser.

## FAQ

> #### How do I install a new provider?

In the settings menu of Streamybara you will find a providers tab. Inside this tab you will find the install provider package option.

> #### How do manage my providers?

Within Streamybara's settings, you will find the providers tab. Within this tab you can disable/enable single providers inside provide packs, enable/disable entire provider packages, enable/ disable automatic provider updates and manually for a update check for your providers.

> #### Streamybara won't show me season or episode lists and instead begins playing automatically?

Please disable the Auto Episode Resume setting in the general tab of Streamybara's settings.

> #### I'm experiencing an issue whilst using Streamybara. Where can I get help?
You can often find help from users in the Addons4Kodi subreddit or you are always welcome to log a github issue and I will contact you directly to investigate the issue.

## License

Licensed under The GPL License.


## [![Repography logo](https://images.repography.com/logo.svg)](https://repography.com) Recent activity [![Time period](https://images.repography.com/31557107/StreamybaraKodi/StreamybaraDevelopment/recent-activity/54b09eb47a7d1f063e1adf376fe18f03_badge.svg)](https://repography.com)
[![Timeline graph](https://images.repography.com/31557107/StreamybaraKodi/StreamybaraDevelopment/recent-activity/54b09eb47a7d1f063e1adf376fe18f03_timeline.svg)](https://github.com/StreamybaraKodi/StreamybaraDevelopment/commits)
[![Issue status graph](https://images.repography.com/31557107/StreamybaraKodi/StreamybaraDevelopment/recent-activity/54b09eb47a7d1f063e1adf376fe18f03_issues.svg)](https://github.com/StreamybaraKodi/StreamybaraDevelopment/issues)
[![Pull request status graph](https://images.repography.com/31557107/StreamybaraKodi/StreamybaraDevelopment/recent-activity/54b09eb47a7d1f063e1adf376fe18f03_prs.svg)](https://github.com/StreamybaraKodi/StreamybaraDevelopment/pulls)
[![Trending topics](https://images.repography.com/31557107/StreamybaraKodi/StreamybaraDevelopment/recent-activity/54b09eb47a7d1f063e1adf376fe18f03_words.svg)](https://github.com/StreamybaraKodi/StreamybaraDevelopment/commits)

