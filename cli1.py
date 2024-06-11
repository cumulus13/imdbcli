import sys

import imdb
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

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
    options = Options()
    options.headless = True
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
    
    try:
        driver.get(imdb_url)
        trailer_element = driver.find_element(By.XPATH, "//a[contains(@class, 'slate_button')]")
        trailer_url = trailer_element.get_attribute('href')
        return 'https://www.imdb.com' + trailer_url if trailer_url else "No trailer available"
    except Exception as e:
        print(f"Error finding trailer: {e}")
        return "No trailer available"
    finally:
        driver.quit()

if __name__ == '__main__':
    #movie_name = input("Enter the movie name: ")
    movie_name = sys.argv[1]
    get_movie_info(movie_name)
