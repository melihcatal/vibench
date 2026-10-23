class ImageDetectionRequest:
    def __init__(self, image_content: bytes):
        self.image_content = image_content


class LabelDetectionResponse:
    def __init__(self, labels):
        self.labels = labels


class TextDetectionResponse:
    def __init__(self, text):
        self.text = text


class SafeSearchDetectionResponse:
    def __init__(self, adult, spoof, medical, violence, racy):
        self.adult = adult
        self.spoof = spoof
        self.medical = medical
        self.violence = violence
        self.racy = racy


class ImageDescriptionResponse:
    def __init__(self, description):
        self.description = description
