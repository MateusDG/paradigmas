from dataclasses import dataclass
from typing import List, Optional, TypeVar, Generic, Callable, Any

T = TypeVar('T')

class Collection(Generic[T]):
    def __init__(self, items: Optional[List[T]] = None):
        self._items: List[T] = list(items) if items else []

    def add(self, item: T) -> None:
        self._items.append(item)

    def all(self) -> List[T]:
        return list(self._items)

    def clear(self) -> None:
        self._items.clear()

@dataclass
class Song:
    title: str
    artist: str
    duration: str

    def __str__(self) -> str:
        return f"{self.title} – {self.artist} ({self.duration})"

class Catalog(Collection[Song]):
    def filter(self, predicate: Callable[[Song], bool]) -> List[Song]:
        return [s for s in self._items if predicate(s)]

    def sort_by(self, keyfn: Callable[[Song], Any], reverse: bool = False) -> None:
        self._items.sort(key=keyfn, reverse=reverse)

class Playlist(Collection[Song]):
    pass
