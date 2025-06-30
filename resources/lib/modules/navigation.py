"""Very small navigation stack to track previous plugin calls."""

_stack = []


def push(url):
    if url:
        _stack.append(url)


def pop():
    return _stack.pop() if _stack else None


def clear():
    _stack.clear()
