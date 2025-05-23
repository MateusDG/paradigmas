#!/usr/bin/env python3
# imperative_gui.py

import tkinter as tk
from tkinter import ttk, simpledialog, messagebox

# Paleta
BG_MAIN, BG_LIST = "#121212", "#181818"
ACCENT, FG, FG_DIM = "#1DB954", "#FFFFFF", "#A7A7A7"
FONT, FONT_BIG = ("Segoe UI", 11), ("Segoe UI", 13, "bold")

# Catálogo
songs_catalog = [
    {"title":"Imagine","artist":"John Lennon","duration":"3:07"},
    {"title":"Billie Jean","artist":"Michael Jackson","duration":"4:54"},
    {"title":"Bohemian Rhapsody","artist":"Queen","duration":"5:55"},
    {"title":"Numb","artist":"Linkin Park","duration":"3:06"},
    {"title":"In the End","artist":"Linkin Park","duration":"3:36"},
    {"title":"Breaking the Habit","artist":"Linkin Park","duration":"3:16"},
    {"title":"Shape of You","artist":"Ed Sheeran","duration":"3:53"},
    {"title":"Blinding Lights","artist":"The Weeknd","duration":"3:20"},
    {"title":"Rolling in the Deep","artist":"Adele","duration":"3:48"},
    {"title":"Bad Guy","artist":"Billie Eilish","duration":"3:14"},
    {"title":"Uptown Funk","artist":"Mark Ronson ft. Bruno Mars","duration":"4:30"},
    {"title":"Evidências","artist":"Chitãozinho & Xororó","duration":"4:50"},
    {"title":"Ai Se Eu Te Pego","artist":"Michel Teló","duration":"3:39"},
    {"title":"Que Sorte a Nossa","artist":"Matheus & Kauan","duration":"3:33"},
    {"title":"Atrasadinha","artist":"Felipe Araújo","duration":"3:12"},
    {"title":"Deixa Acontecer","artist":"Grupo Revelação","duration":"4:23"},
    {"title":"A Amizade é Tudo","artist":"Fundo de Quintal","duration":"3:56"},
    {"title":"Livre pra Voar","artist":"Soweto","duration":"4:05"},
    {"title":"Temporal","artist":"Art Popular","duration":"4:15"},
    {"title":"Tempo Perdido","artist":"Legião Urbana","duration":"4:21"},
    {"title":"Anna Júlia","artist":"Los Hermanos","duration":"3:46"},
    {"title":"Pintor do Mundo","artist":"Nenhum de Nós","duration":"4:02"},
    {"title":"Smells Like Teen Spirit","artist":"Nirvana","duration":"5:01"},
    {"title":"Paradise","artist":"Coldplay","duration":"4:38"},
    {"title":"Havana","artist":"Camila Cabello","duration":"3:37"},
    {"title":"Despacito","artist":"Luis Fonsi","duration":"4:42"},
    {"title":"Senhoras e Senhores","artist":"Jorge & Mateus","duration":"3:25"},
    {"title":"Suíte 14","artist":"Henrique & Diego","duration":"3:49"},
    {"title":"Te Assumi pro Brasil","artist":"Matheus & Kauan","duration":"3:08"},
    {"title":"Hear Me Now","artist":"Alok","duration":"3:12"},
    {"title":"Ocean","artist":"Bebe Rexha & David Guetta","duration":"3:35"},
]
playlists: dict[str, list[dict]] = {}

# Converte mm:ss em segundos e vice-versa
_str2sec = lambda t: int(t.split(":")[0])*60 + int(t.split(":")[1])
_sec2str = lambda s: f"{s//60}:{s%60:02d}"

class PlayerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Imperative Player")
        self.configure(bg=BG_MAIN)
        self.geometry("1020x650")
        self.minsize(880,540)

        # Estado de reprodução
        self.current_song = None
        self.elapsed = 0
        self.total = 0
        self.playing = False
        self.timer = None
        self.sort_dirs = {"title": True, "artist": True, "duration": True}

        self._style()
        self._layout()
        self._setup_bindings()

    # ---------- Estilo ----------
    def _style(self):
        st = ttk.Style(self)
        st.theme_use("clam")
        st.configure("TFrame", background=BG_MAIN)
        st.configure("TLabel", background=BG_MAIN, foreground=FG, font=FONT)
        st.configure("Accent.TButton",
                     background=ACCENT, foreground=FG,
                     font=("Segoe UI",10,"bold"), padding=6)
        st.map("Accent.TButton", background=[("active","#1ed760")])
        st.configure("Treeview",
                     background=BG_LIST, fieldbackground=BG_LIST,
                     foreground=FG, font=FONT, rowheight=26)
        st.map("Treeview",
               background=[("selected",ACCENT)],
               foreground=[("selected",BG_MAIN)])
        st.configure("green.Horizontal.TProgressbar",
                     background=ACCENT, troughcolor=BG_LIST)

    # ---------- Layout ----------
    def _layout(self):
        # Barra de busca
        top = ttk.Frame(self); top.pack(fill=tk.X, padx=20, pady=(18,10))
        ttk.Label(top, text="Buscar").pack(side=tk.LEFT)
        self.search = tk.StringVar()
        self.search.trace_add("write", self._filter)
        ttk.Entry(top, textvariable=self.search, width=40, font=FONT).pack(side=tk.LEFT, padx=12)

        # Conteúdo principal
        main = ttk.Frame(self); main.pack(fill=tk.BOTH, expand=True, padx=20)
        # Sidebar de playlists
        side = ttk.Frame(main, width=260); side.pack(side=tk.LEFT, fill=tk.Y, padx=(0,20))
        ttk.Label(side, text="Playlists", font=FONT_BIG).pack(anchor=tk.W)
        self.cb_var = tk.StringVar()
        self.cb = ttk.Combobox(side, textvariable=self.cb_var, state="readonly")
        self.cb.pack(fill=tk.X, pady=6); self.cb.bind("<<ComboboxSelected>>", self._refresh_lb)
        ttk.Button(side, text="＋ Nova", style="Accent.TButton", command=self._new_pl).pack(fill=tk.X, pady=4)
        ttk.Button(side, text="＋ Adicionar Música", style="Accent.TButton", command=self._add_to_pl).pack(fill=tk.X, pady=4)
        ttk.Label(side, text="Faixas", font=("Segoe UI",12,"bold"), padding=(0,14,0,6)).pack(anchor=tk.W)
        self.lb = tk.Listbox(side, bg=BG_LIST, fg=FG, font=FONT,
                             selectbackground=ACCENT, activestyle="none", highlightthickness=0)
        self.lb.pack(fill=tk.BOTH, expand=True)
        ttk.Scrollbar(side, orient=tk.VERTICAL, command=self.lb.yview).place(
            in_=self.lb, relx=1, rely=0, relheight=1, anchor='ne')

        # Catálogo de músicas
        cat = ttk.Frame(main); cat.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        cols = ("title","artist","duration")
        self.tree = ttk.Treeview(cat, columns=cols, show="headings")
        for c, hdr, w in zip(cols, ("Título","Artista","Dur."),(360,240,80)):
            self.tree.heading(c, text=hdr, command=lambda col=c: self._sort(col))
            self.tree.column(c, width=w, anchor=tk.W)
        self._populate(songs_catalog)
        self.tree.tag_configure("playing", background=ACCENT, foreground=BG_MAIN)
        self.tree.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)
        ttk.Scrollbar(cat, orient=tk.VERTICAL, command=self.tree.yview).pack(side=tk.RIGHT, fill=tk.Y)

        # Barra de reprodução
        bottom = ttk.Frame(self); bottom.pack(fill=tk.X, padx=20, pady=12)
        self.play_btn = ttk.Button(bottom, text="▶︎", style="Accent.TButton", width=3, command=self._toggle)
        self.play_btn.pack(side=tk.LEFT)
        self.now = ttk.Label(bottom, text="Nada tocando", foreground=FG_DIM)
        self.now.pack(side=tk.LEFT, padx=12)
        self.time_lbl = ttk.Label(bottom, text="0:00 / 0:00", foreground=FG_DIM)
        self.time_lbl.pack(side=tk.RIGHT)
        self.pg = ttk.Progressbar(bottom, style="green.Horizontal.TProgressbar", maximum=100)
        self.pg.pack(fill=tk.X, padx=10, pady=(6,0))

    # ---------- Atalhos -----------
    def _setup_bindings(self):
        self.bind("<space>", self._toggle)
        self.bind("<Control-n>", lambda e: self._new_pl())

    # ---------- Operações de dados ----------
    def _populate(self, data):
        self.tree.delete(*self.tree.get_children())
        for i, s in enumerate(data):
            self.tree.insert("", tk.END, iid=str(i), values=(s["title"], s["artist"], s["duration"]))

    def _filter(self, *_):
        q = self.search.get().lower()
        self._populate([s for s in songs_catalog if q in (s["title"] + s["artist"]).lower()])

    def _sort(self, col):
        self.sort_dirs[col] = not self.sort_dirs[col]
        rev = not self.sort_dirs[col]
        keyfn = (lambda s: _str2sec(s[col])) if col=="duration" else (lambda s: s[col].lower())
        songs_catalog.sort(key=keyfn, reverse=rev)
        self._filter()

    # ---------- Playlists ----------
    def _new_pl(self):
        name = simpledialog.askstring("Nova Playlist", "Nome:")
        if not name: return
        if name in playlists:
            return messagebox.showwarning("Aviso", "Já existe.")
        playlists[name] = []
        self._update_cb(name)

    def _add_to_pl(self):
        if not playlists:
            return messagebox.showwarning("Aviso", "Crie playlist primeiro.")
        sel = self.tree.selection(); pl = self.cb_var.get()
        if not sel or not pl:
            return messagebox.showwarning("Aviso", "Selecione música e playlist.")
        playlists[pl].append(songs_catalog[int(sel[0])])
        self._refresh_lb()

    def _update_cb(self, sel=None):
        self.cb["values"] = list(playlists.keys())
        if sel:
            self.cb.set(sel)
            self._refresh_lb()

    def _refresh_lb(self, *_):
        self.lb.delete(0, tk.END)
        for s in playlists.get(self.cb_var.get(), []):
            self.lb.insert(tk.END, f"{s['title']} – {s['artist']} ({s['duration']})")

    # ---------- Player ----------
    def _toggle(self, event=None):
        if not self.current_song:
            sel = self.tree.selection()
            if not sel:
                return messagebox.showinfo("Info", "Selecione música.")
            self._start(songs_catalog[int(sel[0])], sel[0])
            return
        self.playing = not self.playing
        self.play_btn.configure(text="⏸" if self.playing else "▶︎")
        if self.playing:
            self._tick()
        else:
            self.after_cancel(self.timer)

    def _start(self, song, row_id):
        for iid in self.tree.tag_has("playing"):
            self.tree.item(iid, tags=())
        self.tree.item(row_id, tags=("playing",))
        self.tree.selection_set(row_id)
        self.tree.see(row_id)

        self.current_song = song
        self.elapsed = 0
        self.total = _str2sec(song["duration"])
        self.playing = True
        self.play_btn.configure(text="⏸")
        self.now.configure(text=f"Tocando: {song['title']} – {song['artist']}")
        self.pg["value"] = 0
        self.time_lbl.configure(text=f"0:00 / {song['duration']}")
        self._tick()

    def _tick(self):
        if not self.playing:
            return
        self.elapsed += 1
        if self.elapsed >= self.total:
            self.playing = False
            self.play_btn.configure(text="▶︎")
            self.pg["value"] = 100
            return
        self.time_lbl.configure(
            text=f"{_sec2str(self.elapsed)} / {_sec2str(self.total)}"
        )
        self.pg["value"] = (self.elapsed / self.total) * 100
        self.timer = self.after(1000, self._tick)

if __name__ == "__main__":
    PlayerApp().mainloop()
