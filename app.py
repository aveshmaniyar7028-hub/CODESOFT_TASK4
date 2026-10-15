import streamlit as st

from recommendation import (
    load_movies,
    create_similarity_matrix,
    recommend_movies
)

st.set_page_config(
    page_title="Movie Recommendation System",
    page_icon="🎬",
    layout="wide"
)

st.title(
    "🎬 Movie Recommendation System"
)

st.write(
    "Select a movie you like and "
    "get similar movie recommendations."
)

movies = load_movies()

similarity_matrix = (
    create_similarity_matrix(movies)
)

st.sidebar.header(
    "🎯 Your Preferences"
)


selected_movie = st.sidebar.selectbox(

    "Select your favourite movie:",

    [
        movie["title"]
        for movie in movies
    ]
)


number_of_recommendations = (
    st.sidebar.slider(
        "Number of recommendations:",
        3,
        10,
        5,
    )
)


selected_details = None

for movie in movies:

    if movie["title"] == selected_movie:

        selected_details = movie
        break


st.subheader(
    "🎥 Selected Movie"
)


st.markdown(
    f"## {selected_details['title']}"
)


st.write(
    f"**Genre:** "
    f"{selected_details['genre']}"
)


st.write(
    f"**Description:** "
    f"{selected_details['description']}"
)


if st.button(
    "🎯 Recommend Movies",
    type="secondary"
):

    recommendations = recommend_movies(

        selected_movie,

        movies,

        similarity_matrix,

        number_of_recommendations
    )


    st.subheader(
        "✨ Recommended Movies"
    )


    if recommendations:

        st.table(
            recommendations
        )

        st.success(
            "Recommendations generated successfully!"
        )

    else:

        st.warning(
            "No recommendations found."
        )

with st.expander(
    "📊 View Movie Dataset"
):

    for movie in movies:

        st.write(
            f"**{movie['title']}** — "
            f"{movie['genre']}"
        )

        st.write(
            movie["description"]
        )

        st.divider()



st.divider()

st.caption(
    "Content-Based Filtering | "
    "TF-IDF | Cosine Similarity | "
    "Python"
)