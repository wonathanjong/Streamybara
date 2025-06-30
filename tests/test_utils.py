import json
import urllib.parse as parse
import unittest


def create_url(base_url, params):
    if params is None:
        return base_url
    if "action_args" in params and isinstance(params["action_args"], dict):
        params["action_args"] = json.dumps(params["action_args"], sort_keys=True)
    return f"{base_url}/?{parse.urlencode(sorted(params.items()))}"


class TestCreateURL(unittest.TestCase):
    def test_create_url_encodes_args(self):
        url = create_url("plugin://addon", {"action": "do", "action_args": {"id": 1}})
        self.assertEqual(
            url,
            "plugin://addon/?action=do&action_args=%7B%22id%22%3A+1%7D",
        )


if __name__ == "__main__":
    unittest.main()
