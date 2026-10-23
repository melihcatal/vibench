from google.cloud import language_v1

class ModelClient:
    def __init__(self):
        self.client = language_v1.LanguageServiceClient()

    def summarize(self, text):
        document = language_v1.Document(content=text, type_=language_v1.Document.Type.PLAIN_TEXT)
        response = self.client.summarize(document)
        return response.summary

    def extract_json(self, text):
        document = language_v1.Document(content=text, type_=language_v1.Document.Type.PLAIN_TEXT)
        response = self.client.analyze_entities(document)
        return response.entities

    def answer_with_context(self, question, context):
        document = language_v1.Document(content=context, type_=language_v1.Document.Type.PLAIN_TEXT)
        response = self.client.analyze_sentiment(document)
        return response.document_sentiment.score

    def stream_completion(self, text):
        document = language_v1.Document(content=text, type_=language_v1.Document.Type.PLAIN_TEXT)
        response = self.client.analyze_entities(document)
        for entity in response.entities:
            yield entity.name