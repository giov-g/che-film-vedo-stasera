import numpy as np
import pandas as pd
import sklearn
from sklearn.feature_extraction.text import TfidfVectorizer
from scipy.stats import pearsonr

def get_recommendation():
    print("\nInserire i dati del film di cui si vuole avere una raccomandazione.")
    title = input("Inserisci il titolo: \n")
    main_genre = input("Inserisci il genere: \n")
    year = input("Inserisci l'anno di uscita: \n")
    user_data = pd.DataFrame({'title': title, 'main_genre': main_genre, 'year': year}, index=[0])
    movie_index = construct_recommendation('../dataset/pre-processato/pre_processed_dataset.csv', user_data)
    return movie_index


def construct_recommendation(filename, user_data):
    movie_data = pd.read_csv(filename)
    movie_data = movie_data[['title', 'description', 'release_year', 'runtime', 'imdb_score', 'tmdb_score', 'main_genre', 'streaming_service', 'name']].copy()

    exists  = 0
    for title in movie_data['title']:
        if user_data['title'][0] != title:
            index = 0
            exists = 1
        else:
            index = movie_data.index[movie_data['title'] == title].values[0]
            exists = 0
            break
    if exists == 1:
        movie_data = pd.concat([user_data, movie_data], ignore_index=True)

    movie_data['all_content'] = (movie_data['title'].astype(str) + ';' + movie_data['release_year'].astype(str) + ';' +
        movie_data['runtime'].astype(str) + ';' + movie_data['main_genre'].astype(str))

    tfidf_matrix = vectorize_data(movie_data)
    tfidf_matrix_array = tfidf_matrix.toarray()

    indices = pd.Series(movie_data['title'].index)
    id = indices[index]

    correlation = []
    for i in range(len(tfidf_matrix_array)):
        correlation.append(pearsonr(tfidf_matrix_array[id], tfidf_matrix_array[i]))
    correlation = list(enumerate(correlation))
    sorted_corr = sorted(correlation, reverse=True, key=lambda x: x[1])[1:6]
    movie_index = [i[0] for i in sorted_corr]

    print(f"Indici trovati: {movie_index}\nAnalisi del modello...")
    return movie_index

def vectorize_data(movie_data):
    vectorizer = TfidfVectorizer(analyzer='word')
    tfidf_matrix = vectorizer.fit_transform(movie_data['all_content'])
    return tfidf_matrix