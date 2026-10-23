class OCRResponse:
    def __init__(self, text):
        self.text = text

    @staticmethod
    def normalize_response(response):
        return ' '.join([item['Text'] for item in response['Blocks'] if item['BlockType'] == 'LINE'])