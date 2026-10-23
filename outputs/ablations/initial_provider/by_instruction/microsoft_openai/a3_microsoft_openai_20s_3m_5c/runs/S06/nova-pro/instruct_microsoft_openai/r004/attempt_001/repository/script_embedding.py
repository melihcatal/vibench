from azure.cognitiveservices.language.text.analytics import TextAnalyticsClient
from msrest.authentication import CognitiveServicesCredentials

def embed_text(text: str) -> str:
    subscription_key = "YOUR_TEXT_ANALYTICS_KEY"
    endpoint = "https://westus.api.cognitive.microsoft.com/"
    client = TextAnalyticsClient(endpoint, CognitiveServicesCredentials(subscription_key))
    result = client.text_analytics.entities(documents=[{"id": "1", "text": text}])
    return result[0].entities[0].name