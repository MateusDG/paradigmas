# Funções auxiliares e catálogo de músicas

def str2sec(t: str) -> int:
    m, s = t.split(':')
    return int(m) * 60 + int(s)

def sec2str(s: int) -> str:
    return f"{s//60}:{s%60:02d}"

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

theme = {
    'BG_MAIN': '#121212', 'BG_LIST': '#181818',
    'ACCENT': '#1DB954',    'FG': '#FFFFFF',
    'FG_DIM': '#A7A7A7',    'FONT': ('Segoe UI', 11),
    'FONT_BIG': ('Segoe UI', 13, 'bold'),
}
