"""Simple helper validation functions for onboarding."""


import re


def verify_provider(token):
    """Return True if the provider token appears valid.

    The token must be at least 16 alphanumeric characters which mirrors
    the format returned by common debrid services.
    """
    return bool(re.fullmatch(r"[A-Za-z0-9]{16,}", str(token or "")))


def verify_trakt(api_key):
    """Return True if the Trakt API key appears valid.

    Trakt API keys are typically hex strings; this simply checks for a
    reasonable length and character set.
    """
    return bool(re.fullmatch(r"[A-Fa-f0-9]{8,}", str(api_key or "")))
