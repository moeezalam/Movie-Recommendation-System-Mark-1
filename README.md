# CineMatch: Movie Recommendation System
GENERATED THIS DOCUMENTATION USING AI
A content-based movie recommendation system that suggests similar movies based on your preferences. The system analyzes movie features like genres, keywords, cast, crew, and plot overview to find movies with similar themes and styles.

## Features

- **Content-based recommendations**: Get movie suggestions based on themes, genres, and styles
- **Beautiful UI**: Aesthetic design inspired by IMDB and Letterboxd
- **Movie posters**: Visual representation of movies using TMDB API
- **Responsive design**: Works on various screen sizes

## Technologies Used

- Python 3.x
- Streamlit for the web interface
- Pandas for data manipulation
- Scikit-learn for machine learning algorithms
- NLTK for natural language processing
- TMDB API for movie posters and data

## How It Works

1. The system uses TMDB's 5000 Movies Dataset
2. Text data from movie features is processed using stemming and vectorization
3. Cosine similarity is calculated between movies
4. When you select a movie, the system finds the 5 most similar movies
5. Movie posters are fetched from TMDB API

## Installation

```bash
# Clone the repository
git clone https://github.com/moeezalam/Movie-Recommendation-System-Mark-1.git
cd Movie-Recommendation-System-Mark-1

# Install dependencies
pip install -r requirements.txt
```

You'll need to run movie_recommender_system.py with TMDB's dataset

```bash
# Run the application
streamlit run app.py --server.headless true
```
