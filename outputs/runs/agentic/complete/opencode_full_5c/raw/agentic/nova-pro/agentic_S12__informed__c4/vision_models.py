class VisionResponse:
    def __init__(self, labels):
        self.labels = labels

    @staticmethod
    def normalize(response):
        return VisionResponse(response["Labels"])
