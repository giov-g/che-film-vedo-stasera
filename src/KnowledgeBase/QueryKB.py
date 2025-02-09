from pyswip import Prolog

def main():
    prolog = Prolog()
    prolog.consult('KB.pl')     # Assicurati che questo carichi correttamente la tua KB
    film_ids = []               # Lista di supporto per memorizzare i risultati della ricerca

    while True:
        try:
            choice = int(input("\nScegliere quale funzione eseguire:\n"
                "1. Trova un film dato il periodo d'uscita, il genere e la durata\n"
                "2. Dato il genere ed una tipologia di valutazione, determina i film migliori secondo l'indice IMDD\n"
                "3. Trovare la miglior piattaforma di streaming (devi aver eseguito 1.)\n"
                "0. Esci\nInserisci un valore: "))
            if choice == 1:
                film_ids = find_films(prolog)
            if choice == 2:
                find_best_score(prolog)
            elif choice == 3:
                if film_ids:
                    find_platform(prolog, film_ids)
                else:
                    print("Devi aver ricercato un film (eseguire scelta 1.)")
            elif choice == 0:
                break
        except ValueError:
            print("Input non valido, devi inserire un numero")


def find_films(prolog):
    uscita = None
    genere = None
    durata = None
    film_ids = []

    while uscita is None:
        try:
            uscita_input = int(input("\nInserisci il periodo relativo all'anno di uscita del film\n"
                                     "1. recente\n2. tra 2000 e 2010\n3. fino al 2000\n"))
            if uscita_input == 1:
                uscita = "recente"
            elif uscita_input == 2:
                uscita = "tra_2000_2010"
            elif uscita_input == 3:
                uscita = "pre_2000"
            else:
                print("Scelta non consentita! Inserire un valore tra 1 e 3...")
        except ValueError:
            print("Input non valido. Inserisci un numero.")

    while genere is None:
        try:
            genere_input = int(input("Inserisci il genere cui vorresti appartenga il film\n"
                    "1. western\t2. scifi\t3. romance\n4. drama\t5. horror\t6. thriller\n7. comedy\t"
                    "8. crime\t9. documentation\n10. family\t11. action\t12. fantasy\n13. animation\t"
                    "14. music\t15. history\n16. war\t17. european\t18. sport\n19. reality\n"))
            genres = ["western", "scifi", "romance", "drama", "horror", "thriller", "comedy", "crime",
                      "documentation", "family", "action", "fantasy", "animation", "music", "history",
                      "war", "european", "sport", "reality"]

            if 1 <= genere_input <= 19:
                genere = genres[genere_input - 1]
            else:
                print("Scelta non consentita! Inserire un valore tra 1 e 19...")
        except ValueError:
            print("Input non valido. Inserisci un numero.")

    while durata is None:
        try:
            durata_input = int(input("Inserisci la durata del film\n1. breve\n2. media\n3. lunga\n"))
            if durata_input == 1:
                durata = "breve"
            elif durata_input == 2:
                durata = "media"
            elif durata_input == 3:
                durata = "lunga"
            else:
                print("Scelta non consentita! Inserire un valore tra 1 e 3...")
        except ValueError:
            print("Input non valido. Inserisci un numero.")

    query = f"{uscita}_{genere}_{durata}(ID)"
    try:
        results = list(prolog.query(query))
        if not results:
            print("Nessun film rispetta questi criteri")
            return []

        ids_set = set()
        print("I film trovati sono:")
        for element in results:
            film_id = element["ID"]
            if film_id not in ids_set:
                film_name_query = f"title({film_id}, Title)"
                name_results = list(prolog.query(film_name_query))
                if name_results:
                    film_name = name_results[0]["Title"]
                    print(film_id, film_name)
                    film_ids.append(film_id)
                ids_set.add(film_id)
    except Exception as e:
        print(f"Errore durante l'esecuzione della query: {e}")
    return film_ids





def find_best_score(prolog):
    genre = None
    valutazione = None
    film_scores = {}

    genres = ["western", "scifi", "romance", "drama", "horror", "thriller", "comedy", "crime",
              "documentation", "family", "action", "fantasy", "animation", "music", "history",
              "war", "european", "sport", "reality"]
    valutazioni = ["bassa" , "buona" , "eccellente"]

    while genre is None:
        try:
            genere_input = int(input("Inserisci il genere di cui vorresti trovare il miglior film\n"
                             "1. western\t2. scifi\t3. romance\n4. drama\t5. horror\t6. thriller\n7. comedy\t"
                             "8. crime\t9. documentation\n10. family\t11. action\t12. fantasy\n13. animation\t"
                             "14. music\t15. history\n16. war\t17. european\t18. sport\n19. reality\n"))
            if 1 <= genere_input <= 19:
                genre = genres[genere_input - 1]
            else:
                print("Inserire un valore tra 1 e 19...\n")
        except ValueError:
            print("Input non valido. Inserisci un numero.")

    while valutazione is None:
        try:
            valutazione_input = int(input("Inserisci la valutazione del film\n1. bassa\n2. buona\n3. eccellente\n"))
            if 1 <= valutazione_input <= 3:
                valutazione = valutazioni[valutazione_input - 1]
            else:
                print("Inserire un valore tra 1 e 3...\n")
        except ValueError:
            print("Input non valido. Inserisci un numero.")

    genre_query = f"film_genre(FilmID, '{genre}')"
    film_ids = []

    try:
        results = list(prolog.query(genre_query))
        for result in results:
            film_id = result["FilmID"]

            valutazione_query = f"film_valutazione({film_id}, Valutazione)"
            valutazione_result = list(prolog.query(valutazione_query))
            if not valutazione_result or valutazione_result[0]["Valutazione"] != valutazione:
                continue

            score_query = f"imdb_score({film_id}, Score)"
            score_results = list(prolog.query(score_query))
            if score_results:
                film_scores[film_id] = score_results[0]["Score"]

        sorted_films = sorted(film_scores.items(), key=lambda x: x[1], reverse=True)
        film_ids = [film[0] for film in sorted_films[:10]]  # Prendiamo i primi 10 migliori film

    except Exception as e:
        print(f"Errore nella query del genere: {e}")
        return

    # Se nessun film è stato trovato
    if not film_ids:
        print("Nessun film trovato per questo genere\n")
        return

    # Stampiamo i migliori film trovati
    print("I migliori film trovati:")
    for film_id, score in sorted_films[:10]:
        print(f"Film ID: {film_id}, IMDb Score: {score}")






def find_platform(prolog, film_ids):
    platform_count = {}
    price_filters = []

    # Selezione del prezzo
    while not price_filters:
        try:
            price_input = int(input("Seleziona il costo dell'abbonamento:\n1. economico\n2. medio\n3. costoso\n"))
            if price_input == 1:
                price_filters = ["prezzo_economy"]
            elif price_input == 2:
                price_filters = ["prezzo_economy", "prezzo_medio"]
            elif price_input == 3:
                price_filters = ["prezzo_economy", "prezzo_medio", "prezzo_costoso"]
            else:
                print("Scelta non consentita! Inserire un valore tra 1 e 3...")
        except ValueError:
            print("Input non valido. Inserisci un numero.")

    for film_id in film_ids:
        query = f"streaming_service({film_id}, Piattaforma)"
        try:
            results = list(prolog.query(query))
            for result in results:
                piattaforma = result["Piattaforma"]
                price_match = False
                for price_filter in price_filters:
                    price_query = f"{price_filter}({film_id})"
                    price_results = list(prolog.query(price_query))
                    if price_results:
                        price_match = True
                        break

                if price_match:
                    if piattaforma in platform_count:
                        platform_count[piattaforma] += 1
                    else:
                        platform_count[piattaforma] = 1
        except Exception as e:
            print(f"Errore durante l'esecuzione della query per {film_id}: {e}")

    if platform_count:
        best_platform = max(platform_count, key=platform_count.get)
        print(f"La piattaforma consigliata è: {best_platform}")
        print(f"Numero di film disponibili su {best_platform}: {platform_count[best_platform]}")
    else:
        print("La ricerca non ha prodotto risultati.")

if __name__ == "__main__":
    main()
