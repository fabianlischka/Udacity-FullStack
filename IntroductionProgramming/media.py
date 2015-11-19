import webbrowser

class Movie():
    def __init__(self, mt, ms, mpu, mtu):
        self.title = mt
        self.storyline = ms
        self.poster_image_url = mpu
        self.trailer_youtube_url = mtu

    def show_trailer(self):
        webbrowser.open(self.trailer_youtube_url)
