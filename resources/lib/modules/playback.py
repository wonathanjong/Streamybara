"""Utilities for selecting preferred playback source."""

from typing import List, Optional, Dict, Any
import math

# Quality order from lowest to highest
QUALITY_LEVELS = [720, 1080, 2160]


def _parse_size(value: Any) -> float:
    """Return numeric size in GB from arbitrary value."""
    if value is None:
        return math.inf
    if isinstance(value, (int, float)):
        return float(value)
    try:
        cleaned = str(value).lower().replace("gb", "").strip()
        return float(cleaned)
    except ValueError:
        return math.inf


def select_preferred_source(
    sources: List[Dict[str, Any]],
    preference: int = 0,
    forced_quality: Optional[int] = None,
) -> Optional[Dict[str, Any]]:
    """Return the source that best matches user preference."""

    if not sources:
        return None

    sorted_sources = sorted(sources, key=lambda s: s.get("quality", 0))

    if forced_quality is not None:
        matches = [s for s in sorted_sources if s.get("quality") == forced_quality]
        if matches:
            return min(matches, key=lambda s: _parse_size(s.get("size")))

    qualities = sorted({s.get("quality", 0) for s in sorted_sources})
    highest = qualities[-1]
    lowest = qualities[0]
    second_highest = qualities[-2] if len(qualities) > 1 else highest

    if preference == 0:  # highest quality always
        candidates = [s for s in sorted_sources if s.get("quality") == highest]
        return candidates[-1]
    elif preference == 1:  # high quality
        candidates = [s for s in sorted_sources if s.get("quality") == highest]
        return min(candidates, key=lambda s: _parse_size(s.get("size")))
    elif preference == 2:  # medium quality
        candidates = [s for s in sorted_sources if s.get("quality") == second_highest]
        if candidates:
            return max(candidates, key=lambda s: _parse_size(s.get("size") or 0))
        return sorted_sources[0]
    else:  # low quality
        candidates = [s for s in sorted_sources if s.get("quality") == lowest]
        return min(candidates, key=lambda s: _parse_size(s.get("size")))
