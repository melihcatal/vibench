class OCRResponse:
    def __init__(self, text):
        self.text = text

    @staticmethod
    def normalize_response(response):
        return OCRResponse(response)