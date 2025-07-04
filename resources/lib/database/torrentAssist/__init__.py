import collections

from resources.lib.database import Database
from resources.lib.modules.globals import g

schema = {
    'torrents': {
        'columns': collections.OrderedDict(
            [
                ("debrid_id", ["TEXT", "NOT NULL", "PRIMARY KEY"]),
                ("provider", ["TEXT", "NOT NULL"]),
                ("status", ["TEXT", "NOT NULL"]),
                ("release_title", ["TEXT", "NOT NULL"]),
                ("progress", ["TEXT", "NOT NULL"]),
            ]
        ),
        "table_constraints": [],
        "default_seed": [],
    }
}


class TorrentAssist(Database):
    """
    Database to monitor downloads of torrents initiated by Streamybara
    """

    def __init__(self):
        super().__init__(g.TORRENT_ASSIST, schema)
        self.table_name = next(iter(schema))

    def get_assist_torrents(self):
        """
        Fetches all known transfers
        :return: List of transfer records
        :rtype: list
        """
        return self.fetchall("SELECT * FROM torrents")

    def clear_non_active_assist(self):
        """
        Remove all records of transfers that have completed or failed
        :return: None
        :rtype: None
        """
        self.execute_sql(
            ["DELETE FROM torrents WHERE status = 'failed'", "DELETE FROM torrents WHERE status = 'finished'"]
        )

    def add_assist_torrent(self, debrid_id, provider, status, release_title, progress):
        """
        Add or update a transfer record
        :param debrid_id: ID of debrid provider
        :type debrid_id: str
        :param provider: Provider item was sourced by
        :type provider: str
        :param status: Current status of the transfer
        :type status: str
        :param release_title: Release title of the transferring item
        :type release_title: str
        :param progress: Current progress of item
        :type progress: str
        :return: None
        :rtype: None
        """
        self.execute_sql(
            "REPLACE INTO torrents (debrid_id, provider, status, release_title, progress) " "VALUES (?, ?, ?, ?, ?)",
            (debrid_id, provider, status, release_title, progress),
        )
