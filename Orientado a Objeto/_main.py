from model import Song, Catalog
from player import DefaultPlayer
from gui import OOPlayerApp
from utils import songs_catalog

if __name__ == '__main__':
    catalog = Catalog([Song(**d) for d in songs_catalog])
    player = DefaultPlayer(catalog)
    OOPlayerApp(player).mainloop()
