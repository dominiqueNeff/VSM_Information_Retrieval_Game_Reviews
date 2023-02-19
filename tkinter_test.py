import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showinfo

import pandas as pd

import nltk
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
# nltk.download('stopwords')

import numpy as np
import re

import operator

import pickle

from funktionen import *



# root window
root = tk.Tk()
root.geometry("300x150")
root.resizable(False, False)
root.title('CAS - Information Retrieval')

stopwords = set(stopwords.words('english'))

data = pd.read_csv('./data/steam_game_reviews.csv')

corpus = data.loc[:,['title','reviews_combined']]

with open('./data/index.pickle', 'rb') as handle:
    index = pickle.load(handle)

def select():
    msg = 'Antwort: Die 5 am höchsten bewerteten Games für den Suchterm sind:\n {}'.format(evaluateScores(calculateScores(index, suchterm.get()), corpus, 5))
    showinfo(
        title='Information',
        message=msg
    )


# store email address and password
suchterm = tk.StringVar()

# Sign in frame
signin = ttk.Frame(root)
signin.pack(padx=10, pady=10, fill='x', expand=True)

# email
suchterm_label = ttk.Label(signin, text="Suchterm:")
suchterm_label.pack(fill='x', expand=True)

suchterm_entry = ttk.Entry(signin, textvariable=suchterm)
suchterm_entry.pack(fill='x', expand=True)
suchterm_entry.focus()

# search button
search_button = ttk.Button(signin, text="Resultat", command=select)
search_button.pack(fill='x', expand=True, pady=10)


root.mainloop()