from resources.lib.database.trakt_sync.movies import TraktSyncDatabase


def search_movies(query):
    """Return a list of movie items matching query."""
    db = TraktSyncDatabase()
    results = db.extract_trakt_page(
        "search/movie",
        query=query,
        fields="title,aliases",
        extended="full",
        page=1,
        hide_watched=False,
        hide_unaired=False,
    )
    return [m for m in results if float(m.get("trakt_object", {}).get("info", {}).get("score", 1)) > 0]
