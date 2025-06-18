import pickle
import requests
import pandas as pd
import streamlit as st
from typing import List

# Page configuration
st.set_page_config(page_title="Movie Recommender",
                   page_icon="🎬", layout="centered")

# Custom CSS styling for a modern UI
st.markdown("""
    <style>
    .title {
        text-align: center;
        font-size: 36px;
        color: #FFFFFF;
        background-color: #6c63ff;
        padding: 15px;
        border-radius: 10px;
        margin-bottom: 30px;
    }
    .stButton > button {
        background-color: #6c63ff;
        color: white;
        padding: 0.6em 1.2em;
        font-size: 16px;
        border-radius: 8px;
        border: none;
        transition: 0.3s;
    }
    .stButton > button:hover {
        background-color: #5848c2;
    }
    </style>
""", unsafe_allow_html=True)

# App title
st.markdown('<div class="title">🎬 Content-Based Movie Recommender</div>',
            unsafe_allow_html=True)

# Load pickled data


@st.cache_resource
def load_data():
    with open('../Models/movie_list.pkl', 'rb') as f:
        df = pickle.load(f)
    with open('../Models/similarity.pkl', 'rb') as f:
        similarity = pickle.load(f)
    return df, similarity


df, similarity = load_data()

# Movie recommendation logic


def recommended_movies(movie_name: str) -> List[str]:
    try:
        index = df[df["title"] == movie_name].index[0]
        distances = list(enumerate(similarity[index]))
        movie_idx_list = sorted(
            distances, key=lambda x: x[1], reverse=True)[1:6]
        return [df.iloc[i[0]]["title"] for i in movie_idx_list]
    except:
        return []

# Poster fetc Logic


def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(
        movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path


# UI components
selected_movie = st.selectbox("🎥 Choose a movie you like:", df["title"].values)

if st.button("🔍 Recommend"):
    with st.spinner("Finding similar movies..."):
        recommendations = recommended_movies(selected_movie)
        if recommendations:
            st.success("Top 5 Recommendations Just for You 👇")

            # Display recommendations in columns
            cols = st.columns(5)
            for i, movie in enumerate(recommendations):
                with cols[i]:
                    st.markdown(
                        f"""
                        <div class="movie-card">
                            <img src="https://via.placeholder.com/150x225?text=Poster" width="100%%" />
                            <div class="movie-title">{movie}</div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
        else:
            st.error("❌ Sorry, we couldn't find recommendations for that movie.")
