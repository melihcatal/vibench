class EmbeddingsModels:
    def __init__(self):
        pass

    def normalize_request(self, text):
        return {'documents': [{'id': '1', 'text': text}]}

    def parse_response(self, response):
        return response['documents'][0]['embedding']