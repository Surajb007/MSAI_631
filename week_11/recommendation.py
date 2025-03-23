import streamlit as st
import pandas as pd
from sklearn.neighbors import NearestNeighbors

# Sample Movie Dataset (Movie, Genre)
movies = {
    'movie_id': [1, 2, 3, 4, 5, 6],
    'movie_name': ['Toy Story', 'Jumanji', 'Grumpier Old Men', 'Waiting to Exhale', 'Father of the Bride Part II', 'Die Hard'],
    'genre': ['Animation', 'Adventure', 'Comedy', 'Drama', 'Comedy', 'Action']
}

# Sample Ratings Dataset (User, Movie, Rating)
ratings = {
    'user_id': [1, 1, 1, 2, 2, 3, 3],
    'movie_id': [1, 2, 3, 1, 4, 2, 5],
    'rating': [5, 4, 3, 4, 5, 5, 2]
}

# Convert to DataFrame
movies_df = pd.DataFrame(movies)
ratings_df = pd.DataFrame(ratings)

# Pivot the ratings data to get a user-item matrix
user_movie_ratings = ratings_df.pivot(index='user_id', columns='movie_id', values='rating').fillna(0)

# Build the recommendation model using Nearest Neighbors
knn = NearestNeighbors(metric='cosine', algorithm='brute')
knn.fit(user_movie_ratings.values)

def recommend_movies(user_id, n_recommendations=3):
    user_ratings = user_movie_ratings.loc[user_id].values.reshape(1, -1)
    distances, indices = knn.kneighbors(user_ratings, n_neighbors=n_recommendations)
    
    recommended_movies = []
    for idx in indices.flatten():
        movie_id = user_movie_ratings.columns[idx]
        movie_name = movies_df[movies_df['movie_id'] == movie_id]['movie_name'].values[0]
        recommended_movies.append(movie_name)
        
    return recommended_movies

# Streamlit UI
st.title("Movie Recommendation System")

# Create an input field for user ID
user_id = st.number_input("Enter User ID:", min_value=1, max_value=3, step=1)

# Button to get recommendations
if st.button("Get Recommendations"):
    if user_id:
        # Get recommendations for the selected user ID
        recommendations = recommend_movies(user_id)
        st.subheader("Recommended Movies:")
        for idx, movie in enumerate(recommendations, start=1):
            st.write(f"{idx}. {movie}")
    else:
        st.error("Please enter a valid user ID.")

