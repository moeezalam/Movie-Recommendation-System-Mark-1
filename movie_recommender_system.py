import numpy as np
import pandas as pd
import ast
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.stem.porter import PorterStemmer
import pickle

# Load the movies_dict pickle file
try:
    movies_dict = pickle.load(open('movies_dict.pkl', 'rb'))
    # Convert the dictionary to a DataFrame
    movies = pd.DataFrame(movies_dict)
    
    # This is what app.py is importing
    # No need to reprocess all the data since we already have the pickle files
    
except Exception as e:
    print(f"Error loading pickle files: {e}")
    print("Regenerating model from scratch...")
    
    # If pickle files are corrupted or missing, regenerate them
    # Load CSVs with absolute paths
    movies = pd.read_csv(r'C:\Users\moeez\Documents\Machine Learning Projects\tmdb_5000_movies.csv')
    credits = pd.read_csv(r'C:\Users\moeez\Documents\Machine Learning Projects\tmdb_5000_credits.csv')

    # Merge on title
    movies = movies.merge(credits, on='title')

    # Keep required columns - now including 'id' for poster fetching
    movies = movies[['id', 'title', 'overview', 'genres', 'keywords', 'cast', 'crew']]
    movies.dropna(inplace=True)

    # Convert JSON-like strings to list of names
    def convert(obj):
        return [i['name'] for i in ast.literal_eval(obj)]

    def convert3(obj):
        return [i['name'] for i in ast.literal_eval(obj)[:3]]

    def convert4(obj):
        crew = ast.literal_eval(obj)
        return [member['name'] for member in crew if member.get('job') == "Director"]

    # Apply converters
    movies['genres'] = movies['genres'].apply(convert)
    movies['keywords'] = movies['keywords'].apply(convert)
    movies['cast'] = movies['cast'].apply(convert3)
    movies['crew'] = movies['crew'].apply(convert4)

    # Preprocess text fields
    movies['overview'] = movies['overview'].apply(lambda x: x.split())
    for col in ['genres', 'keywords', 'cast', 'crew']:
        movies[col] = movies[col].apply(lambda x: [i.replace(" ", "") for i in x])

    # Create tags column
    movies['tags'] = movies['overview'] + movies['genres'] + movies['keywords'] + movies['cast'] + movies['crew']

    # Create new DataFrame - now including 'id' for poster fetching
    new_df = movies[['id', 'title', 'tags']].copy()
    new_df['tags'] = new_df['tags'].apply(lambda x: " ".join(x).lower())

    # Stemming
    ps = PorterStemmer()
    def stem(text):
        return " ".join([ps.stem(i) for i in text.split()])

    new_df['tags'] = new_df['tags'].apply(stem)

    # Vectorization
    cv = CountVectorizer(max_features=5000, stop_words='english')
    vectors = cv.fit_transform(new_df['tags']).toarray()

    # Cosine similarity
    similarity = cosine_similarity(vectors)

    # Save the movies DataFrame and similarity matrix as pickle files
    movies_dict = new_df.to_dict()
    pickle.dump(movies_dict, open('movies_dict.pkl', 'wb'))
    pickle.dump(similarity, open('similarity.pkl', 'wb'))
    
    # Update movies to be the new_df for consistency
    movies = new_df

# Define the recommendation function - now returning movie IDs as well
def recommend(movie):
    try:
        # Load similarity matrix if not already loaded
        if 'similarity' not in globals():
            global similarity
            similarity = pickle.load(open('similarity.pkl', 'rb'))
            
        movie_index = movies[movies['title'] == movie].index[0]
        distances = similarity[movie_index]
        movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
        
        recommended_movies = []
        for i in movies_list:
            movie_id = movies.iloc[i[0]].id
            movie_title = movies.iloc[i[0]].title
            recommended_movies.append({'title': movie_title, 'id': movie_id})
        return recommended_movies
    except Exception as e:
        print(f"Error in recommendation: {e}")
        return []

# Test the function if this file is run directly
if __name__ == "__main__":
    # Try to recommend a popular movie as a test
    try:
        print("Testing recommendation system...")
        print(recommend("Avatar"))
    except Exception as e:
        print(f"Test failed: {e}")