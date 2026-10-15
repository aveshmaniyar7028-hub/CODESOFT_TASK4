import csv
import math
import re
from collections import Counter

def load_movies():

    movies = []

    with open(
        "movies.csv",
        "r",
        encoding="utf-8"
    ) as file:

        reader = csv.DictReader(file)

        for row in reader:
            movies.append(row)

    return movies

def tokenize(text):

    text = text.lower()

    words = re.findall(
        r"\b[a-z]+\b",
        text
    )

    return words

def create_tfidf_vectors(movies):

    documents = []

    for movie in movies:

        text = (
            movie["genre"]
            + " "
            + movie["description"]
        )

        words = tokenize(text)

        documents.append(words)
    total_documents = len(documents)

    document_frequency = Counter()

    for document in documents:

        unique_words = set(document)

        for word in unique_words:

            document_frequency[word] += 1

    vectors = []

    for document in documents:

        word_count = Counter(document)

        total_words = len(document)

        vector = {}

        for word, count in word_count.items():

            tf = count / total_words

            idf = math.log(
                total_documents /
                (1 + document_frequency[word])
            ) + 1

            vector[word] = tf * idf

        vectors.append(vector)

    return vectors

def cosine_similarity(vector1, vector2):

    common_words = set(vector1.keys()) & set(
        vector2.keys()
    )
    dot_product = sum(
        vector1[word] * vector2[word]
        for word in common_words
    )
    magnitude1 = math.sqrt(
        sum(
            value * value
            for value in vector1.values()
        )
    )

    magnitude2 = math.sqrt(
        sum(
            value * value
            for value in vector2.values()
        )
    )

    if magnitude1 == 0 or magnitude2 == 0:

        return 0

    return dot_product / (
        magnitude1 * magnitude2
    )


def create_similarity_matrix(movies):

    tfidf_vectors = create_tfidf_vectors(
        movies
    )

    similarity_matrix = []

    for vector1 in tfidf_vectors:

        row = []

        for vector2 in tfidf_vectors:

            similarity = cosine_similarity(
                vector1,
                vector2
            )

            row.append(similarity)

        similarity_matrix.append(row)

    return similarity_matrix

def recommend_movies(
    selected_movie,
    movies,
    similarity_matrix,
    number_of_recommendations=10
):

    movie_index = None

    for i, movie in enumerate(movies):

        if movie["title"] == selected_movie:

            movie_index = i
            break

    if movie_index is None:

        return []
    scores = []

    for i, score in enumerate(
        similarity_matrix[movie_index]
    ):

        if i != movie_index:

            scores.append(
                (i, score)
            )
    scores.sort(
        key=lambda x: x[1],
        reverse=True
    )

    recommendations = []

    for index, score in scores[
        :number_of_recommendations
    ]:

        recommendations.append({

            "Movie":
                movies[index]["title"],

            "Genre":
                movies[index]["genre"],

            "Similarity (%)":
                round(
                    score * 100,
                    2
                )
        })

    return recommendations