import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
from typing import List, Optional

from model import Song
from player import PlayerInterface
from utils import str2sec, sec2str, theme

class OOPlayerApp(tk.Tk):
    def __init__(self, player: PlayerInterface):
        super().__init__()
        self.title("OO Streaming – Music Player")
        self.configure(bg=theme['BG_MAIN'])
        self.geometry("1020x650")
        self.minsize(880, 540)

        # Injeção do player abstrato
        self.player = player

        # Estado de reprodução
        self.current: Optional[Song] = None
        self.elapsed = 0
        self.total = 0
        self.playing = False
        self.timer = None
        self.sort_dirs = {'title': True, 'artist': True, 'duration': True}

        self._setup_style()
        self._setup_layout()
        self._setup_bindings()

    def _setup_style(self):
        st = ttk.Style(self)
        st.theme_use('clam')
        st.configure('TFrame', background=theme['BG_MAIN'])
        st.configure('TLabel', background=theme['BG_MAIN'], foreground=theme['FG'], font=theme['FONT'])
        st.configure('Accent.TButton', background=theme['ACCENT'], foreground=theme['FG'],
                     font=('Segoe UI', 10, 'bold'), padding=6)
        st.map('Accent.TButton', background=[('active', '#1ed760')])
        st.configure('Treeview', background=theme['BG_LIST'], fieldbackground=theme['BG_LIST'],
                     foreground=theme['FG'], font=theme['FONT'], rowheight=26)
        st.map('Treeview', background=[('selected', theme['ACCENT'])],
               foreground=[('selected', theme['BG_MAIN'])])
        st.configure('green.Horizontal.TProgressbar', background=theme['ACCENT'], troughcolor=theme['BG_LIST'])

    def _setup_layout(self):
        # Barra de busca
        top = ttk.Frame(self)
        top.pack(fill=tk.X, padx=20, pady=(18, 10))
        ttk.Label(top, text="Buscar").pack(side=tk.LEFT)
        self.search_var = tk.StringVar()
        self.search_var.trace_add('write', self._filter)
        ttk.Entry(top, textvariable=self.search_var, width=40, font=theme['FONT']).pack(side=tk.LEFT, padx=12)

        # Conteúdo principal
        main = ttk.Frame(self)
        main.pack(fill=tk.BOTH, expand=True, padx=20)

        # Sidebar de playlists
        side = ttk.Frame(main, width=260)
        side.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 20))
        ttk.Label(side, text="Playlists", font=theme['FONT_BIG']).pack(anchor=tk.W)
        self.pl_var = tk.StringVar()
        self.pl_cb = ttk.Combobox(side, textvariable=self.pl_var, state='readonly')
        self.pl_cb.pack(fill=tk.X, pady=6)
        self.pl_cb.bind('<<ComboboxSelected>>', self._refresh_playlist)
        ttk.Button(side, text="＋ Nova Playlist", style='Accent.TButton', command=self._new_playlist).pack(fill=tk.X, pady=4)
        ttk.Button(side, text="＋ Adicionar Música", style='Accent.TButton', command=self._add_to_playlist).pack(fill=tk.X, pady=4)
        ttk.Label(side, text="Faixas", font=('Segoe UI', 12, 'bold'), padding=(0,14,0,6)).pack(anchor=tk.W)
        self.pl_listbox = tk.Listbox(side, bg=theme['BG_LIST'], fg=theme['FG'], font=theme['FONT'],
                                     selectbackground=theme['ACCENT'], activestyle='none', highlightthickness=0)
        self.pl_listbox.pack(fill=tk.BOTH, expand=True)
        ttk.Scrollbar(side, orient=tk.VERTICAL, command=self.pl_listbox.yview).place(
            in_=self.pl_listbox, relx=1, rely=0, relheight=1, anchor='ne')

        # Catálogo
        cat = ttk.Frame(main)
        cat.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        cols = ('title', 'artist', 'duration')
        self.tree = ttk.Treeview(cat, columns=cols, show='headings')
        for c, h, w in zip(cols, ('Título','Artista','Dur.'),(360,240,80)):
            self.tree.heading(c, text=h, command=lambda col=c: self._sort(col))
            self.tree.column(c, width=w, anchor=tk.W)
        self.tree.tag_configure('playing', background=theme['ACCENT'], foreground=theme['BG_MAIN'])
        self.tree.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)
        ttk.Scrollbar(cat, orient=tk.VERTICAL, command=self.tree.yview).pack(side=tk.RIGHT, fill=tk.Y)

        # Barra de reprodução
        bottom = ttk.Frame(self)
        bottom.pack(fill=tk.X, padx=20, pady=12)
        self.play_btn = ttk.Button(bottom, text='▶︎', style='Accent.TButton', width=3, command=self._toggle)
        self.play_btn.pack(side=tk.LEFT)
        self.now_lbl = ttk.Label(bottom, text='Nada tocando', foreground=theme['FG_DIM'])
        self.now_lbl.pack(side=tk.LEFT, padx=12)
        self.time_lbl = ttk.Label(bottom, text='0:00 / 0:00', foreground=theme['FG_DIM'])
        self.time_lbl.pack(side=tk.RIGHT)
        self.pg = ttk.Progressbar(bottom, style='green.Horizontal.TProgressbar', maximum=100)
        self.pg.pack(fill=tk.X, padx=10, pady=(6,0))

        # Popula lista inicial
        self._populate(self.player.list_songs())

    def _setup_bindings(self):
        self.bind('<space>', self._toggle)
        self.bind('<Control-n>', lambda e: self._new_playlist())

    # População e filtro
    def _populate(self, songs: List[Song]):
        self.tree.delete(*self.tree.get_children())
        for i, song in enumerate(songs):
            self.tree.insert('', tk.END, iid=str(i), values=(song.title, song.artist, song.duration))

    def _filter(self, *_):
        q = self.search_var.get().lower()
        filtered = self.player.catalog.filter(lambda s: q in (s.title + s.artist).lower())
        self._populate(filtered)

    def _sort(self, col: str):
        self.sort_dirs[col] = not self.sort_dirs[col]
        rev = not self.sort_dirs[col]
        if col == 'duration':
            keyfn = lambda s: str2sec(s.duration)
        else:
            keyfn = lambda s: getattr(s, col).lower()
        self.player.catalog.sort_by(keyfn, reverse=rev)
        self._filter()

    # Playlists
    def _new_playlist(self):
        name = simpledialog.askstring('Nova Playlist', 'Nome:')
        if not name:
            return
        if not self.player.create_playlist(name):
            return messagebox.showwarning('Aviso', 'Playlist já existe.')
        self._update_playlist_cb(name)

    def _add_to_playlist(self):
        if not getattr(self.player, 'playlists', None):
            return messagebox.showwarning('Aviso', 'Crie uma playlist primeiro.')
        sel = self.tree.selection()
        pl = self.pl_var.get()
        if not sel or not pl:
            return messagebox.showwarning('Aviso', 'Selecione música e playlist.')
        song = self.player.list_songs()[int(sel[0])]
        self.player.add_to_playlist(pl, song)
        self._refresh_playlist()

    def _update_playlist_cb(self, sel: Optional[str] = None):
        vals = list(getattr(self.player, 'playlists', {}).keys())
        self.pl_cb['values'] = vals
        if sel:
            self.pl_cb.set(sel)
            self._refresh_playlist()

    def _refresh_playlist(self, *_):
        self.pl_listbox.delete(0, tk.END)
        for song in self.player.get_playlist_songs(self.pl_var.get()):
            self.pl_listbox.insert(tk.END, str(song))

    # Playback
    def _toggle(self, event=None):
        if not self.current:
            sel = self.tree.selection()
            if not sel:
                return messagebox.showinfo('Info', 'Selecione música.')
            song = self.player.list_songs()[int(sel[0])]
            self._start(song, sel[0])
            return
        self.playing = not self.playing
        self.play_btn['text'] = '⏸' if self.playing else '▶︎'
        if self.playing:
            self._tick()
        else:
            if self.timer:
                self.after_cancel(self.timer)

    def _start(self, song: Song, row_id: str):
        # remove highlight anterior
        for iid in self.tree.tag_has('playing'):
            self.tree.item(iid, tags=())
        # destaca novo
        self.tree.item(row_id, tags=('playing',))
        self.tree.selection_set(row_id)
        self.tree.see(row_id)

        self.current = song
        self.elapsed = 0
        self.total = str2sec(song.duration)
        self.playing = True
        self.play_btn['text'] = '⏸'
        self.now_lbl['text'] = f"Tocando: {song.title} – {song.artist}"
        self.time_lbl['text'] = f"0:00 / {song.duration}"
        self.pg['value'] = 0
        self._tick()

    def _tick(self):
        if not self.playing:
            return
        self.elapsed += 1
        if self.elapsed >= self.total:
            self.playing = False
            self.play_btn['text'] = '▶︎'
            self.pg['value'] = 100
            return
        self.time_lbl['text'] = f"{sec2str(self.elapsed)} / {sec2str(self.total)}"
        self.pg['value'] = (self.elapsed / self.total) * 100
        self.timer = self.after(1000, self._tick)
