from django.shortcuts import render,HttpResponse
import pickle
import requests
import numpy as np
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from config import *

def home(request):
    return render(request, "index.html")

def rcs_home(request):
    return render(request, "home.html")

def get_token():
    url = "https://accounts.spotify.com/api/token"

    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }

    data = {
        "grant_type": "client_credentials",
        "client_id": client_id,
        "client_secret": client_secret
    }
    # Send the POST request
    response = requests.post(url, headers=headers, data=data)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Print the response content (JSON data)
        return response.json()["access_token"]
    else:
        # Print an error message if the request was not successful
        print("Error:", response.status_code)

def fetch_song_poster(song_id, size=300):
    # Get the access token
    token = get_token()
    
    # Define the URL and headers
    url = f"https://api.spotify.com/v1/tracks/{song_id}"
    headers = {
        "Authorization": f"Bearer {token}"
    }

    # Send the GET request
    response = requests.get(url, headers=headers)
    
    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Get the list of images from the response
        images = response.json()["album"]["images"]
        
        # Find the image with the desired size
        for image in images:
            if image["height"] == size and image["width"] == size:
                return image["url"]
        
        # If no image with the desired size is found, return None
        return None
    else:
        # Print an error message if the request was not successful
        print("Error:", response.status_code)


def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={timdb_token}&language=en-US"
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path


def get_top_50_movies(movies):
    movies_data = []
    for _, row in movies[:50].iterrows():
        temp = []
        genres = row.genres[:2]
        genres = " ".join(genres)        
        temp.extend([row.original_title, row.poster, genres])
        movies_data.append(temp)
    return movies_data

def get_songs_data(songs_df):
    songs_data = []
    for _, row in songs_df.iterrows():
        temp = []
        temp.extend([row.track_name, row.poster, row.artists])
        songs_data.append(temp)
    return songs_data


def recommend_movies(movies,similarity,movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movies_data = []
    for i in distances[1:6]:
        temp = []
        movie_id = movies.iloc[i[0]].id
        temp.append(fetch_poster(movie_id))
        temp.append(movies.iloc[i[0]].title)
        recommended_movies_data.append(temp)
    return recommended_movies_data

def recommend_songs(song):
    suggestions = []
    for i in range(6):
        songs = pickle.load(open(f'data/songs/songs_df_{i}.pkl','rb'))
        similarity_score = pickle.load(open(f'data/songs/similarity_scores_{i}.pkl','rb'))
        try:
            movie_index = songs[songs['track_name']==song].index[0]
            if movie_index == None:
                continue
            distances = similarity_score[movie_index]
            movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x:x[1])[1:6]
            for i in movies_list:
                poster = fetch_song_poster(songs.iloc[i[0]]['track_id'])
                songs.loc[i[0], 'poster'] = poster
                suggestions.append(songs.iloc[i[0]])
            return suggestions
        except Exception as e:
            continue


def recommend_books(books,books_pt,similarity_scores,book_name):
    book_index = np.where(books_pt.index==book_name)[0][0]
    distances = similarity_scores[book_index]
    suggestions = sorted(enumerate(distances), key=lambda x: x[1], reverse=True)[1:6] # 0th index is the book itself
    data = []
    for i in suggestions:
        item = []
        temp_df = books[books['Book-Title'] == books_pt.index[i[0]]]
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
        data.append(item)
    return data

def rcs_recommend(request):
    path = request.path
    if path == "/rcs/recommend_movies":
        movies = pickle.load(open('data/movies/movies.pkl','rb'))
        similarity = pickle.load(open('data/movies/movies_similarity.pkl','rb'))
        user_input = request.POST.get('movie')
        recommended_movies_data = recommend_movies(movies,similarity,user_input)
        return render(request, 'recommended_movies.html', {'recommended_movies_data': recommended_movies_data, 'user_input': user_input})
    
    elif path == "/rcs/recommend_books":
        books_df = pickle.load(open('data/books/books_df.pkl','rb'))
        books_pt = pickle.load(open('data/books/books_pt.pkl','rb'))
        similarity_scores = pickle.load(open('data/books/books_similarity_scores.pkl','rb'))

        user_input = request.POST.get('book_name')
        recommended_books_data = recommend_books(books_df,books_pt,similarity_scores,user_input)
        return render(request, 'recommended_books.html', {'recommended_books_data': recommended_books_data, 'user_input': user_input})
    
    elif path == "/rcs/recommend_songs":
        user_input = request.POST.get('song_name')
        recommended_songs_data = recommend_songs(user_input)
        return render(request, 'recommended_songs.html', {'recommended_songs_data': recommended_songs_data, 'user_input': user_input})

    else:
        return HttpResponse("Invalid URL")

        
def rcs(request):
    path = request.path
    if path == "/rcs/movies":
        popular_movies_df = pickle.load(open("data/movies/popular_movies.pkl", "rb"))
        movies_data = get_top_50_movies(popular_movies_df)
        return render(request, 'movies.html', {'movies_data': movies_data})
    
    elif path == "/rcs/songs":
        # track_id	artists	album_name	track_name	track_genre
        popular_songs_df = pickle.load(open("data/songs/top_songs_df.pkl", "rb"))
        songs_data = get_songs_data(popular_songs_df)
        
        return render(request, 'songs.html', {'songs_data': songs_data})
    
    elif path == "/rcs/books":
        popular_books_df = pickle.load(open("data/books/popular_books.pkl", "rb"))
        books_data = zip(
            popular_books_df['Book-Title'].values,
            popular_books_df['Image-URL-M'].values,
            popular_books_df['Book-Author'].values
        )
        return render(request, 'books.html', {'books_data': books_data})
    
    else:
        return HttpResponse("Invalid URL")