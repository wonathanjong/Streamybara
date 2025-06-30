from resources.lib.indexers.trakt import TraktAPI


def like_list(trakt_id, username="me"):
    """Like a Trakt list."""
    TraktAPI().post_json(f"users/{username}/lists/{trakt_id}/like", {})


def unlike_list(trakt_id, username="me"):
    """Remove like from a Trakt list."""
    TraktAPI().delete_request(f"users/{username}/lists/{trakt_id}/like")


def toggle_list_like(trakt_id, username="me", liked=False):
    """Toggle a like status for a list."""
    if liked:
        unlike_list(trakt_id, username)
    else:
        like_list(trakt_id, username)
