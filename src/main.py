from src.Ontology import Ontology
from src import KNNRecommender
from src.KnowledgeBase import QueryKB

class Main:
    def run(self):
        while True:
            print("\nSelezionare un'operazione:\n1. Utilizzare l'ontologia\n2. Utilizzare la KnowledgeBase\n"
                  "3. Utilizzare un Recommender System per i film\n0. Uscire")
            your_choice = input("Inserisci un valore: ")
            if your_choice == '1':
                Ontology.main()
            elif your_choice == '2':
                QueryKB.main()
            elif your_choice == '3':
                KNNRecommender.main()
            elif your_choice == '0':
                break

if __name__ == "__main__":
    Main().run()