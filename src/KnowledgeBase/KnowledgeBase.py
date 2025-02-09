import pandas as pd

def string_cleaning(s):
    if isinstance(s, str):
        return s.replace("'", "").encode('ascii', 'ignore').decode()
    return str(s)

class KnowledgeBase:
    def createKB(self):
        df = pd.read_csv('../../dataset/pre-processato/pre_processed_dataset.csv')
        columns_to_string = ['title', 'description', 'streaming_service', 'imdb_score', 'main_genre', 'name']
        df[columns_to_string] = df[columns_to_string].apply(lambda x: x.apply(string_cleaning))

        with open('../KB.pl', 'w') as f:
            # Direttiva per predicati discontigui
            f.write(":- discontiguous title/2.\n")
            f.write(":- discontiguous description/2.\n")
            f.write(":- discontiguous release_year/2.\n")
            f.write(":- discontiguous runtime/2.\n")
            f.write(":- discontiguous main_genre/2.\n")
            f.write(":- discontiguous name/2.\n")
            f.write(":- discontiguous streaming_service/2.\n")
            f.write(":- discontiguous imdb_score/2.\n")
            f.write(":- discontiguous monthly_subscription_cost/2.\n")

            # Scrittura dei fatti
            for index, row in df.iterrows():
                f.write(f"title({row['id']}, '{row['title']}').\n")
                f.write(f"description({row['id']}, '{row['description']}').\n")
                f.write(f"release_year({row['id']}, {row['release_year']}).\n")
                f.write(f"runtime({row['id']}, {row['runtime']}).\n")
                f.write(f"main_genre({row['id']}, '{row['main_genre']}').\n")
                f.write(f"name({row['id']}, '{row['name']}').\n")
                f.write(f"imdb_score({row['id']}, {row['imdb_score']}).\n")
                f.write(f"streaming_service({row['id']}, '{row['streaming_service']}').\n")
                f.write(f"monthly_subscription_cost({row['id']}, {row['monthly_subscription_cost']}).\n")

            # Scrittura delle regole
            rules = [
                # Prezzo di sottoscrizione
                "prezzo_economy(ID) :- monthly_subscription_cost(ID, Cost), Cost < 9.99.\n",
                "prezzo_medio(ID) :- monthly_subscription_cost(ID, Cost), Cost = 9.99.\n",
                "prezzo_costoso(ID) :- monthly_subscription_cost(ID, Cost), Cost > 9.99.\n",

                # Anno di uscita
                "film_recente(ID) :- release_year(ID, Uscita), Uscita > 2010.\n",
                "film_tra_2000_2010(ID) :- release_year(ID, Uscita), 2000 =< Uscita, Uscita =< 2010.\n",
                "film_pre_2000(ID) :- release_year(ID, Uscita), Uscita < 2000.\n",

                # Genere principale
                "film_genre(ID, Genre) :- main_genre(ID, Genre).\n",

                # Durata del film
                "film_breve_durata(ID) :- runtime(ID, Durata), Durata =< 60.\n",
                "film_media_durata(ID) :- runtime(ID, Durata), 60 < Durata, Durata =< 90.\n",
                "film_lunga_durata(ID) :- runtime(ID, Durata), Durata > 90.\n",

                # Valutazione film
                "film_valutazione_bassa(ID) :- imdb_score(ID, Score), Score =< 6.\n",
                "film_valutazione_buona(ID) :- imdb_score(ID, Score), Score >= 6.1, Score =< 8.\n",
                "film_valutazione_eccellente(ID) :- imdb_score(ID, Score), Score >= 8.1, Score =< 10.\n",

                # Utilizzo di film_durata per ottenere la durata in categorie
                "film_durata(ID, breve) :- film_breve_durata(ID).\n",
                "film_durata(ID, media) :- film_media_durata(ID).\n",
                "film_durata(ID, lunga) :- film_lunga_durata(ID).\n",

                # Combinazioni di anno e genere
                "recente_genre(ID, Genre) :- film_recente(ID), film_genre(ID, Genre).\n",
                "tra_2000_2010_genre(ID, Genre) :- film_tra_2000_2010(ID), film_genre(ID, Genre).\n",
                "pre_2000_genre(ID, Genre) :- film_pre_2000(ID), film_genre(ID, Genre).\n",

                # Combinazioni di anno, genere e durata
                "recente_genre_durata(ID, Genre, DurataCat) :- recente_genre(ID, Genre), film_durata(ID, DurataCat).\n",
                "tra_2000_2010_genre_durata(ID, Genre, DurataCat) :- tra_2000_2010_genre(ID, Genre), film_durata(ID, DurataCat).\n",
                "pre_2000_genre_durata(ID, Genre, DurataCat) :- pre_2000_genre(ID, Genre), film_durata(ID, DurataCat).\n",

                # Definizione di film_durata per ottenere la durata in categorie
                "film_valutazione(ID, bassa):- film_valutazione_bassa(ID).\n"
                "film_valutazione(ID, buona):- film_valutazione_buona(ID).\n"
                "film_valutazione(ID, eccellente):- film_valutazione_eccellente(ID).\n"
            ]

            for rule in rules:
                f.write(rule)

            # Combinazioni per ogni genere
            genres = ['western', 'scifi', 'romance', 'drama', 'horror', 'thriller', 'comedy', 'crime', 'documentation',
                      'family', 'action', 'fantasy', 'animation', 'music', 'history', 'war', 'european', 'sport',
                      'reality']

            for genre in genres:
                f.write(f"recente_{genre}_breve(ID) :- recente_genre_durata(ID, '{genre}', breve).\n")
                f.write(f"recente_{genre}_media(ID) :- recente_genre_durata(ID, '{genre}', media).\n")
                f.write(f"recente_{genre}_lunga(ID) :- recente_genre_durata(ID, '{genre}', lunga).\n")
                f.write(f"tra_2000_2010_{genre}_breve(ID) :- tra_2000_2010_genre_durata(ID, '{genre}', breve).\n")
                f.write(f"tra_2000_2010_{genre}_media(ID) :- tra_2000_2010_genre_durata(ID, '{genre}', media).\n")
                f.write(f"tra_2000_2010_{genre}_lunga(ID) :- tra_2000_2010_genre_durata(ID, '{genre}', lunga).\n")
                f.write(f"pre_2000_{genre}_breve(ID) :- pre_2000_genre_durata(ID, '{genre}', breve).\n")
                f.write(f"pre_2000_{genre}_media(ID) :- pre_2000_genre_durata(ID, '{genre}', media).\n")
                f.write(f"pre_2000_{genre}_lunga(ID) :- pre_2000_genre_durata(ID, '{genre}', lunga).\n")

kb = KnowledgeBase()
kb.createKB()
