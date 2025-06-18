# Streamlit entry point
import pickle
import pandas as pd
import streamlit as st
from typing import List


def recommended_movies(movie_name: str) -> List[str]:
    movie_list = []
    try:
        movie_idx_list = sorted(list(enumerate(
            similarity[df[df["title"] == movie_name].index[0]])), reverse=True, key=lambda x: x[1])[1:6]
        for idx in movie_idx_list:
            movie_list.append(df.iloc[idx[0]]["title"])

    except Exception as E:
        movie_list = []

    return movie_list


with open('../Models/movie_list.pkl', 'rb') as f:
    df = pickle.load(f)

with open('../Models/similarity.pkl', 'rb') as f:
    similarity = pickle.load(f)


# movie_name = input("Enter a movie name: \n")
# print(recommended_movies(movie_name=movie_name))

st.title("Content Based Movie Recommender System")

movie_name = st.selectbox("Select a movie", df["title"].values)

if st.button("Recommend"):
    movie_list = recommended_movies(movie_name=movie_name)
    if movie_list:
        st.subheader("Recommended Movies")
        for movie_name in movie_list:
            st.write(movie_name)
