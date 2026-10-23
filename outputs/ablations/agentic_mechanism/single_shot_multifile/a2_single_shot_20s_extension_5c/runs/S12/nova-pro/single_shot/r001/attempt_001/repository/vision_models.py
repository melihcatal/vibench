class VisionResponse:
    def __init__(self, objects=None, caption=None, text=None, adult=None):
        self.objects = objects
        self.caption = caption
        self.text = text
        self.adult = adult