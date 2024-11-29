from resources.lib.common.source_utils import get_best_episode_match
from resources.lib.debrid.real_debrid import RealDebrid
from resources.lib.modules.exceptions import FileIdentification
from resources.lib.modules.globals import g
from resources.lib.modules.resolver.torrent_resolvers.base_resolver import (
    TorrentResolverBase,
)


class RealDebridResolver(TorrentResolverBase):
    """
    Resolver for Real Debrid
    """

    def __init__(self):
        super().__init__()
        self.debrid_module = RealDebrid()
        self._source_normalization = (
            ("path", "path", None),
            ("bytes", "size", lambda k: (k / 1024) / 1024),
            ("size", "size", None),
            ("filename", "release_title", None),
            ("id", "id", None),
            ("link", "link", None),
            ("selected", "selected", None),
        )
        self.torrent_id = None

    def _get_files_from_check_hash(self, torrent, item_information):
        hash_check = self.debrid_module.check_hash(torrent["hash"])[torrent["hash"]]
        [value.update({"idx": key}) for sub_dict in hash_check["rd"] for key, value in sub_dict.items()]
        return hash_check

    def _get_selected_files(self, torrent_id):
        info = self.debrid_module.torrent_info(torrent_id)
        files = [i for i in info["files"] if i["selected"]]
        [i.update({"link": info["links"][idx]}) for idx, i in enumerate(files)]
        if g.get_bool_setting("rd.autodelete"):
            self.debrid_module.delete_torrent(info["id"])
        return files

    def _fetch_source_files(self, torrent, item_information):
        hash_check = self._get_files_from_check_hash(torrent, item_information)
        return self._get_selected_files(hash_check["torrent_id"])

    def resolve_stream_url(self, file_info):
        """
        Convert provided source file into a link playable through debrid service
        :param file_info: Normalised information on source file
        :return: streamable link
        """
        return self.debrid_module.resolve_hoster(file_info["link"])

    def _do_post_processing(self, item_information, torrent, identified_file):
        if identified_file is None and not g.get_bool_setting("rd.autodelete"):
            self.debrid_module.delete_torrent(self.torrent_id)
