import pickle
import streamlit as st
import requests

# Function to fetch movie posters from TMDB
def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        poster_path = data.get('poster_path')
        if poster_path:
            return f"https://image.tmdb.org/t/p/w500/{poster_path}"
    return "https://via.placeholder.com/500x750?text=No+Image"

# Function to recommend movies based on similarity
def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:6]:
        # Fetching the movie ID and title
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_names.append(movies.iloc[i[0]].title)
        # Fetching the movie poster
        recommended_movie_posters.append(fetch_poster(movie_id))
    return recommended_movie_names, recommended_movie_posters

# Streamlit App Interface
st.title('🎬 Movie Recommender System')

# Load movies and similarity data
movies = pickle.load(open('movie_list.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

# Movie selection from dropdown
movie_list = movies['title'].values
selected_movie = st.selectbox("Type or select a movie from the dropdown", movie_list)

# Button to show recommendations
if st.button('Show Recommendation'):
    recommended_movie_names, recommended_movie_posters = recommend(selected_movie)
    
    # Using st.columns to display the recommendations
    if recommended_movie_names:
        cols = st.columns(5)
        for idx, col in enumerate(cols):
            with col:
                st.text(recommended_movie_names[idx])
                st.image(recommended_movie_posters[idx], use_container_width=True)
    else:
        st.write("No recommendations available for this movie.")
