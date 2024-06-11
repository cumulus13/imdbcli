import sys

import imdb
import requests
from bs4 import BeautifulSoup

def get_movie_info(movie_name):
    # Create an instance of the IMDb class
    ia = imdb.IMDb()

    # Search for movies with the provided name
    search_results = ia.search_movie(movie_name)

    if not search_results:
        print(f"No results found for '{movie_name}'")
        return

    # Select the first result (most relevant)
    movie = search_results[0]
    ia.update(movie)

    # Fetch detailed info about the movie
    movie_id = movie.movieID
    movie_info = ia.get_movie(movie_id)

    # Extract relevant information
    title = movie_info.get('title')
    year = movie_info.get('year')
    plot = movie_info.get('plot outline')
    director = ', '.join(str(d) for d in movie_info.get('director', []))
    cast = ', '.join(str(c) for c in movie_info.get('cast', [])[:5])

    # Get the IMDb URL
    imdb_url = f"https://www.imdb.com/title/tt{movie_id}/"

    # Fetch the IMDb page to find the trailer URL
    trailer_url = get_trailer_url(imdb_url)

    # Print movie information
    print(f"Title: {title}")
    print(f"Year: {year}")
    print(f"Plot: {plot}")
    print(f"Director: {director}")
    print(f"Cast: {cast}")
    print(f"IMDb URL: {imdb_url}")
    print(f"Trailer URL: {trailer_url}")

def get_trailer_url(imdb_url):
    response = requests.get(imdb_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    trailer_tag = soup.find('a', {'class': 'slate_button'})
    
    if trailer_tag:
        return 'https://www.imdb.com' + trailer_tag['href']
    return "No trailer available"

if __name__ == '__main__':
    #movie_name = input("Enter the movie name: ")
    movie_name = sys.argv[1]
    get_movie_info(movie_name)
