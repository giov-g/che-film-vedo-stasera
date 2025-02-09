from owlready2 import *

def main():
    while (True):
        print("\nSelezionare un'operazione:\n1. Visualizzare le classi\n2. Visualizzare le proprietà d'oggetto\n3."
              " Visualizzare le proprietà dei dati\n4. Eseguire una query\n0. Uscire\n")
        menu_answer = input("Inserire scelta: ")

        ontology_path = 'Ontology/Ontology.owx'
        ontology = get_ontology(ontology_path).load()

        if menu_answer == '1':
            print("Le classi dell'ontologia sono: ")
            classes = ontology.classes()
            for item in classes:
                print(f"- {item}")
            while (True):
                print("\nSelezionare una delle seguenti classi:\n1. Film\n2. Genere\n"
                      "3. Studio di produzione\n4. Anno di rilascio\n5. Piattaforma di streaming\n0. Uscita")
                class_answer = input("Inserire scelta: ")

                if class_answer == '1':
                    print("\nLista dei film: ")
                    film = ontology.search(is_a=ontology.Film)
                    for item in film:
                        print(f"- {item}")
                elif class_answer == '2':
                    print("\nGeneri: ")
                    genre = ontology.search(is_a=ontology.Genre)
                    for item in genre:
                        print(f"- {item}")
                elif class_answer == '3':
                    print("\nStudi di produzione: ")
                    film_production_studio = ontology.search(is_a=ontology.ProductionStudios)
                    for item in film_production_studio:
                        print(f"- {item}")
                elif class_answer == '4':
                    print("\nAnni di rilascio: ")
                    year = ontology.search(is_a=ontology.ReleaseYear)
                    for item in year:
                        print(f"- {item}")
                elif class_answer == '5':
                    print("\nLista piattaforme di streaming: ")
                    streaming_service = ontology.search(is_a=ontology.StreamingPlatform)
                    for item in streaming_service:
                        print(f"- {item}")
                elif class_answer == '0':
                    break
                else:
                    print("Scelta non consentita! Inserire un valore tra 0 e 5...")

        elif menu_answer == '2':
            print("\nProprietà d'oggetto presenti nell'ontologia:")
            object_properties = ontology.object_properties()
            for item in object_properties:
                print(f"- {item}")

        elif menu_answer == '3':
            print("\nProprietà dei dati presenti nell'ontologia:")
            data_properties = ontology.data_properties()
            for item in data_properties:
                print(f"- {item}")

        elif menu_answer == '4':
            while True:
                print("\n1) Lista dei film presenti su 'Amazon'\n""2) Lista film di genere 'comedy'\n"
                      "3) Film di durata superiore a 70 min\n" "0) Torna indietro\n")

                query_choice = input("Inserire un valore: ")
                if query_choice == '1':
                    print("Film presenti su Amazon: ")
                    amazon_films = ontology.search(is_a=ontology.Film,
                                                   is_distribuited_by=ontology.search(is_a=ontology.Amazon))
                    for item in amazon_films:
                        print(f"- {item}")
                elif query_choice == '2':
                    print("Film di genere comedy:")
                    scifi_films = ontology.search(is_a=ontology.Film, has_genre=ontology.search(is_a=ontology.comedy))
                    for item in scifi_films:
                        print(f"- {item}")
                elif query_choice == '3':
                    print("Film di durata superiore a 70 minuti:")
                    films = [film for film in ontology.Film.instances() if
                             hasattr(film, "runtime") and film.runtime[0] > 70]
                    for item in films:
                        print(f"- {item}")

                elif query_choice == '0':
                    break

        elif menu_answer == '0':
            break

if __name__ == "__main__":
    main()