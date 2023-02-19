from tkinter.font import BOLD
from tkinter.ttk import Treeview
from VSM_Functions import *

import tkinter as tk
from tkinter import ttk
from tkinter import *
from tkinter.messagebox import showinfo





def select():
    msg = print_result(cosine_score(suchterm.get(), K=3), games_reviewed)
    showinfo(
        title='Information',
        message=msg
    )

def select2():

    result_df = print_result(cosine_score(suchterm.get(), K=47), games_reviewed, tag.get(), top = 10)
    print(result_df)
    print(tag.get())

    for item in result_list.get_children():
        result_list.delete(item)

    
    games = result_df['title']
    review_count = result_df['review_count']
    recommendation_ratio = result_df['recommendation_ratio']
    avg_playtime = result_df['avg_playtime']
    for i in range(0,len(games)):
        # print(i)
        result_list.insert(parent='',index='end',iid=i,text='',
        values=(i+1,games[i],review_count[i],recommendation_ratio[i], avg_playtime[i]))






#---------------------
#--------------- Hauptfenster
#---------------------
root = tk.Tk()
root.geometry("1000x1000")
# root.resizable(False, False)
root.title('CAS - Information Retrieval')

#---------------------
#--------------- Titel
#---------------------
titel = Label(root, text = "Steam Reviews")
titel.config(font = ("Courier", 20, BOLD))

#---------------------
#--------------- Beschreibung
#---------------------
beschreibung = """Wisst ihr einfach nicht welches Spiel ihr als nächstes spielen sollt?
Ja dann ist dieses Tool eure Lösung! Dieses Tool ist von Spielern für Spieler und gibt euch die Möglichkeit anhand von Steam Reviews euer nächstes Spiel zu finden!

Gibt unten eure Suchbegriffe ein und erhaltet die Top 10 Spiele basierend eurer Anfrage.

47 Spiele sind in der Datenbank verfügbar.

Game:                   Titel des Spiels
Review Count:           Anzahl der Reviews
Recommendation Ratio:   Empfehlungsrate in Prozent
Avg. Playtime:          Durchschnittliche Spielzeit der Reviewer
"""

desc = Text(root, height=15, width = 30, font=("Courier", 12))
desc.insert('end', beschreibung)
desc.config(state='disabled')



#---------------------
#--------------- Liste mit den Games
#---------------------
game_frame = Frame(root)

# scrollbar
game_scroll = Scrollbar(game_frame)

game_list = Treeview(game_frame, yscrollcommand=game_scroll.set)
game_scroll.config(command=game_list.yview)

# style = ttk.Style()
# style.configure('mytreeview.Headings', background='gray', font=('Arial Bold', 10))
style = ttk.Style()
style.configure(".", font=('Helvetica', 10), foreground="white")
style.configure("Treeview", foreground='red')
style.configure("Treeview.Heading", font=('Helvetica', 12, BOLD), foreground='black')


# Spalten definieren
game_list['columns'] = ('id','title', 'review_count', 'recommendation_ratio', 'avg_playtime')

game_list.column("#0", width = 0, stretch = NO)
game_list.column("id", anchor = CENTER, width = 50)
game_list.column("title", anchor = CENTER, width = 250)
game_list.column("review_count", anchor = CENTER, width = 160)
game_list.column("recommendation_ratio", anchor = CENTER, width = 200)
game_list.column("avg_playtime", anchor = CENTER, width = 160)

game_list.heading("#0", text = "", anchor = CENTER)
game_list.heading("id", text = "Index", anchor = CENTER)
game_list.heading("title", text = "Game", anchor = CENTER)
game_list.heading("review_count", text = "Review Count", anchor = CENTER)
game_list.heading("recommendation_ratio", text = "Recommendation Ratio", anchor = CENTER)
game_list.heading("avg_playtime", text = "Avg. Playtime", anchor = CENTER)

# Daten hinzufügen

games = games_reviewed['title']
review_count = games_reviewed['review_count']
recommendation_ratio = games_reviewed['recommendation_ratio'].round(2)*100
avg_playtime = games_reviewed['avg_playtime'].round(2)
print(len(games))
for i in range(0,len(games)):
    # print(i)
    game_list.insert(parent='',index='end',iid=i,text='',
    values=(i+1,games[i],review_count[i],recommendation_ratio[i], avg_playtime[i]))


#---------------------
#--------------- Suchfeld eingabe
#---------------------
suchfeld = Label(root, text = "Suchbegriff eingabe")
suchfeld.config(font = ("Courier", 20, BOLD))


#---------------------
#--------------- Query
#---------------------
query_frame = Frame(root)

# Query
suchterm = tk.StringVar()

suchterm_label = Label(query_frame, text="Bitte Suchbegriffe eingeben:")
suchterm_label.config(font = ("Courier", 10))
suchterm_entry = Entry(query_frame, textvariable=suchterm)

# search button
search_button = Button(query_frame, text="Resultat", command=select2)

#---------------------
#--------------- Drop Down Menu
#---------------------
tag = tk.StringVar()
tag.set('All')

drop = OptionMenu(root, tag, *unique_tags)



#---------------------
#--------------- Resultaten Bereich
#---------------------
resultat_label = Label(root, text = "Resultat")
resultat_label.config(font = ("Courier", 20, BOLD))

#---------------------
#--------------- Resultat Tabelle
#---------------------
result_frame = Frame(root)

# scrollbar
result_scroll = Scrollbar(result_frame)

result_list = Treeview(result_frame, yscrollcommand=game_scroll.set)
result_scroll.config(command=result_list.yview)

# Spalten definieren
result_list['columns'] = ('id','title', 'review_count', 'recommendation_ratio', 'avg_playtime')

result_list.column("#0", width = 0, stretch = NO)
result_list.column("id", anchor = CENTER, width = 50)
result_list.column("title", anchor = CENTER, width = 250)
result_list.column("review_count", anchor = CENTER, width = 160)
result_list.column("recommendation_ratio", anchor = CENTER, width = 200)
result_list.column("avg_playtime", anchor = CENTER, width = 160)

result_list.heading("#0", text = "", anchor = CENTER)
result_list.heading("id", text = "Index", anchor = CENTER)
result_list.heading("title", text = "Game", anchor = CENTER)
result_list.heading("review_count", text = "Review Count", anchor = CENTER)
result_list.heading("recommendation_ratio", text = "Recommendation Ratio", anchor = CENTER)
result_list.heading("avg_playtime", text = "Avg. Playtime", anchor = CENTER)


#---------------------
#--------------- GUI Manager
#---------------------
titel.pack()
desc.pack(padx=5, pady=5, fill='x')

game_frame.pack(padx=5, pady=5)
game_scroll.pack(side=RIGHT, fill = Y)
game_list.pack()



suchfeld.pack()
drop.pack()

query_frame.pack(padx=5, pady=5, fill='x', expand=True)
suchterm_entry.focus()
suchterm_label.pack(padx=5, pady=5, side=LEFT)

suchterm_entry.pack(fill='x', expand=True)
search_button.pack(fill='x', expand=True, pady=10)

resultat_label.pack()

result_frame.pack(padx=5, pady=5)
result_scroll.pack(side=RIGHT, fill = Y)
result_list.pack()


root.mainloop()