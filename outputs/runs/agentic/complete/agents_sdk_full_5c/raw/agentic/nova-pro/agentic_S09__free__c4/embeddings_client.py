import os
from azure.ai.textanalytics import TextAnalyticsClient, TextAnalyticsApiKeyCredential

class EmbeddingsClient:
    def __init__(self):
        self.endpoint = os.getenv('AZURE_TEXT_ANALYTICS_ENDPOINT')
        self.key = os.getenv('AZURE_TEXT_ANALYTICS_KEY')
        self.client = TextAnalyticsClient(endpoint=self.endpoint, credential=TextAnalyticsApiKeyCredential(self.key))
    
    def embed_text(self, text):
        result = self.client.extract_key_phrases(documents=[text])
        return result[0].key_phrases
    
    def embed_batch(self, texts):
        result = self.client.extract_key_phrases(documents=texts)
        return [doc.key_phrases for doc in result]
    
    def compute_similarity(self, embedding1, embedding2):
        # Simplified similarity computation
        return sum(1 for e1 in embedding1 if e1 in embedding2)
    
    def search(self, query_embedding, document_embeddings):
        # Simplified search implementation
        return [doc for doc in document_embeddings if any(e in query_embedding for e in doc)]