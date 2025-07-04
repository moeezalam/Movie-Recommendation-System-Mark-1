from movie_recommender_system import movies, recommend
import streamlit as st
import requests
import pandas as pd  # Add this import if not already present

# Set page configuration
st.set_page_config(
    page_title="Movie Recommender",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for styling
st.markdown("""
<style>
    /* Main background and text colors */
    .stApp {
        background-color: #2C2C2C;
        color: #F2E9E1;
    }
    
    /* Header styling */
    h1, h2, h3 {
        color: #DABF73;
        font-family: 'Helvetica Neue', sans-serif;
    }
    
    /* Subheader styling */
    h2 {
        border-bottom: 2px solid #A4875B;
        padding-bottom: 10px;
        margin-top: 30px;
    }
    
    /* Movie card styling */
    .movie-card {
        background-color: #3B1E1E;
        border-radius: 10px;
        padding: 15px;
        margin-bottom: 20px;
        border: 1px solid #7E6B52;
        transition: transform 0.3s;
    }
    
    .movie-card:hover {
        transform: scale(1.02);
        border-color: #FF46A3;
    }
    
    .movie-title {
        color: #DABF73;
        font-size: 1.2rem;
        font-weight: bold;
        margin-top: 10px;
    }
    
    /* Button styling */
    .stButton>button {
        background-color: #B23A48;
        color: #EADDD0;
        border: none;
        border-radius: 5px;
        padding: 10px 20px;
        font-weight: bold;
        transition: all 0.3s;
    }
    
    .stButton>button:hover {
        background-color: #FF46A3;
        color: #F2E9E1;
    }
    
    /* Selectbox styling */
    .stSelectbox>div>div {
        background-color: #4B4B3F;
        color: #EADDD0;
        border: 1px solid #7E6B52;
    }
    
    /* Footer styling */
    footer {
        border-top: 1px solid #5F6A60;
        padding-top: 10px;
        margin-top: 50px;
        color: #C9B798;
        text-align: center;
    }
    
    /* Image container */
    .poster-container {
        overflow: hidden;
        border-radius: 8px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.5);
    }
    
    /* Columns layout */
    .column-container {
        display: flex;
        flex-wrap: wrap;
        gap: 20px;
    }
</style>
""", unsafe_allow_html=True)

# TMDB API settings
API_KEY = "c08eda453b21b54e4e37f1ea4877344f"
POSTER_BASE_URL = "https://image.tmdb.org/t/p/w500"

# Function to fetch movie poster
def fetch_poster(movie_id):
    try:
        response = requests.get(f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}&language=en-US")
        data = response.json()
        poster_path = data.get('poster_path')
        if poster_path:
            return f"{POSTER_BASE_URL}{poster_path}"
        return None
    except Exception as e:
        st.error(f"Error fetching poster: {e}")
        return None

# App header with IMDB/Letterboxd style
st.markdown("""
<div style="text-align: center; padding: 20px 0; background-color: #3B1E1E; border-radius: 10px; margin-bottom: 30px;">
    <h1 style="font-size: 3rem; margin-bottom: 10px;">🎬 CineMatch</h1>
    <p style="font-size: 1.2rem; color: #C9B798;">Discover your next favorite movie</p>
</div>
""", unsafe_allow_html=True)

# Create two columns for layout
col1, col2 = st.columns([1, 3])

with col1:
    st.markdown("<h2>Find Movies</h2>", unsafe_allow_html=True)
    
    # Movie selection
    selected_movie = st.selectbox(
        'Select a movie you love',
        movies['title'].values
    )
    
    # Get the movie ID for the selected movie
    try:
        # Try to get the id from the movies DataFrame
        selected_movie_id = movies[movies['title'] == selected_movie]['id'].values[0]
    except KeyError:
        # If 'id' column doesn't exist, load the original dataset to get the ID
        original_movies = pd.read_csv(r'C:\Users\moeez\Documents\Machine Learning Projects\tmdb_5000_movies.csv')
        selected_movie_id = original_movies[original_movies['title'] == selected_movie]['id'].values[0]
    
    # Fetch and display the poster for the selected movie
    selected_poster = fetch_poster(selected_movie_id)
    if selected_poster:
        st.markdown(f"""
        <div class="movie-card">
            <div class="poster-container">
                <img src="{selected_poster}" width="100%">
            </div>
            <div class="movie-title">{selected_movie}</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Recommend button
    if st.button('Get Recommendations'):
        with st.spinner('Finding perfect matches for you...'):
            recommended_movies = recommend(selected_movie)

with col2:
    st.markdown("<h2>Recommended Movies</h2>", unsafe_allow_html=True)
    
    # Check if recommendations exist
    if 'recommended_movies' in locals():
        if recommended_movies:
            # Create a 3-column layout for recommendations
            rec_cols = st.columns(3)
            
            for i, movie in enumerate(recommended_movies):
                col_index = i % 3
                with rec_cols[col_index]:
                    poster_url = fetch_poster(movie['id'])
                    if poster_url:
                        st.markdown(f"""
                        <div class="movie-card">
                            <div class="poster-container">
                                <img src="{poster_url}" width="100%">
                            </div>
                            <div class="movie-title">{movie['title']}</div>
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.markdown(f"""
                        <div class="movie-card">
                            <div style="height: 300px; background-color: #4B4B3F; display: flex; align-items: center; justify-content: center;">
                                <span>No poster available</span>
                            </div>
                            <div class="movie-title">{movie['title']}</div>
                        </div>
                        """, unsafe_allow_html=True)
        else:
            st.info("No recommendations found. Please try another movie.")
    else:
        st.markdown("""
        <div style="text-align: center; padding: 50px 0; color: #C9B798;">
            <p style="font-size: 1.5rem;">Select a movie and click 'Get Recommendations' to see matches</p>
            <p style="font-size: 1rem; margin-top: 20px;">Our algorithm will find movies with similar themes, genres, and styles</p>
        </div>
        """, unsafe_allow_html=True)

# Footer
st.markdown("""
<footer>
    <p>Powered by TMDB API | Created with ❤️ using Streamlit</p>
</footer>
""", unsafe_allow_html=True)