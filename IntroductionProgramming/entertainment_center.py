import media
import fresh_tomatoes

# Instantiate a few movie objects

toy_story = media.Movie("Toy Story",
                        "Toys - they're alive!",
                        "https://upload.wikimedia.org/wikipedia/en/1/13/Toy_Story.jpg",  #noqa
                        "https://www.youtube.com/watch?v=RmFbmlwWa0k")

big_l = media.Movie("The Big Lebowski",
                    "The Dude abides",
                    "https://upload.wikimedia.org/wikipedia/en/3/35/Biglebowskiposter.jpg",  #noqa
                    "https://www.youtube.com/watch?v=DotBPgt2Kkw")

dr_s = media.Movie("Dr Strangelove",
                   "How I Learned to Stop Worrying and Love the Bomb",
                   "https://upload.wikimedia.org/wikipedia/en/e/e6/Dr._Strangelove_poster.jpg",  #noqa
                   "https://www.youtube.com/watch?v=98NaJ8ss4sY")

b_b = media.Movie("The Blues Brothers",
                  "We're on a mission from God",
                  "https://upload.wikimedia.org/wikipedia/en/a/ae/Bluesbrothersmovieposter.jpg",  #noqa
                  "https://www.youtube.com/watch?v=A-xtJYIwfYo")

matador = media.Movie("The Matador",
                      "A salesman and a hitman walk into a bar...",
                      "https://upload.wikimedia.org/wikipedia/en/6/65/TheMatador2006.jpg",  #noqa
                      "https://www.youtube.com/watch?v=cClpPW1nyTw")


# collect movie objects into a list ...
movies = [toy_story, big_l, dr_s, b_b, matador]
# ... and pass to the open_movies_page function to create the static website
fresh_tomatoes.open_movies_page(movies)
