import media
import fresh_tomatoes

toy_story = media.Movie("Toy Story",
                        "Toys - they're alive!",
                        "https://upload.wikimedia.org/wikipedia/en/1/13/Toy_Story.jpg",
                        "https://www.youtube.com/watch?v=RmFbmlwWa0k")


movies = [toy_story]

open_movies_page(movies)
