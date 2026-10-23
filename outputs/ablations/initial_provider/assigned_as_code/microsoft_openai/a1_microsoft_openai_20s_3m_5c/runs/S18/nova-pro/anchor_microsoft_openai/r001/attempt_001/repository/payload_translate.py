import os
from azure.cognitiveservices.language.textanalytics import TextAnalyticsClient
from msrest.authentication import CognitiveServicesCredentials

def translate_payload(text, source_language='en', target_language='es'):
    credentials = CognitiveServicesCredentials(os.getenv('AZURE_TEXT_ANALYTICS_KEY'))
    client = TextAnalyticsClient(endpoint=os.getenv('AZURE_TEXT_ANALYTICS_ENDPOINT'), credentials=credentials)
    response = client.translate(documents=[{'id': '1', 'text': text}], to=target_language)
    return response[0].translations[0].text

if __name__ == '__main__':
    text = 'Hello, world!'
    print(translate_payload(text))