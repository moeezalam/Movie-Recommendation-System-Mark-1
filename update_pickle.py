import pandas as pd
import pickle
import ast
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.stem.porter import PorterStemmer

print("Loading CSV files...")
# Load CSVs with absolute paths
movies = pd.read_csv(r'C:\Users\moeez\Documents\Machine Learning Projects\tmdb_5000_movies.csv')
credits = pd.read_csv(r'C:\Users\moeez\Documents\Machine Learning Projects\tmdb_5000_credits.csv')

print("Merging datasets...")
# Merge on title
movies = movies.merge(credits, on='title')

# Keep required columns - including 'id' for poster fetching
movies = movies[['id', 'title', 'overview', 'genres', 'keywords', 'cast', 'crew']]
movies.dropna(inplace=True)

print("Processing data...")
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

# Create new DataFrame - including 'id' for poster fetching
new_df = movies[['id', 'title', 'tags']].copy()
new_df['tags'] = new_df['tags'].apply(lambda x: " ".join(x).lower())

print("Applying stemming...")
# Stemming
ps = PorterStemmer()
def stem(text):
    return " ".join([ps.stem(i) for i in text.split()])

new_df['tags'] = new_df['tags'].apply(stem)

print("Calculating similarity...")
# Vectorization
cv = CountVectorizer(max_features=5000, stop_words='english')
vectors = cv.fit_transform(new_df['tags']).toarray()

# Cosine similarity
similarity = cosine_similarity(vectors)

print("Saving pickle files...")
# Save the movies DataFrame and similarity matrix as pickle files
movies_dict = new_df.to_dict()
pickle.dump(movies_dict, open('movies_dict.pkl', 'wb'))
pickle.dump(similarity, open('similarity.pkl', 'wb'))

print("Done! Pickle files updated with 'id' column.")