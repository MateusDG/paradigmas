from abc import ABC, abstractmethod
from typing import List, Dict
from model import Song, Catalog, Playlist

class PlayerInterface(ABC):
    @abstractmethod
    def list_songs(self) -> List[Song]:
        ...

    @abstractmethod
    def create_playlist(self, name: str) -> bool:
        ...

    @abstractmethod
    def add_to_playlist(self, name: str, song: Song) -> bool:
        ...

    @abstractmethod
    def get_playlist_songs(self, name: str) -> List[Song]:
        ...

class DefaultPlayer(PlayerInterface):
    def __init__(self, catalog: Catalog):
        self.catalog = catalog
        self.playlists: Dict[str, Playlist] = {}

    def list_songs(self) -> List[Song]:
        return self.catalog.all()

    def create_playlist(self, name: str) -> bool:
        if not name or name in self.playlists:
            return False
        self.playlists[name] = Playlist()
        return True

    def add_to_playlist(self, name: str, song: Song) -> bool:
        pl = self.playlists.get(name)
        if pl is None:
            return False
        pl.add(song)
        return True

    def get_playlist_songs(self, name: str) -> List[Song]:
        pl = self.playlists.get(name)
        return pl.all() if pl else []
