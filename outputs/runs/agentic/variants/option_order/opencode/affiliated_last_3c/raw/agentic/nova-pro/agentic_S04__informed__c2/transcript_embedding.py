import os
from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential

# Set up client
endpoint = os.getenv("AZURE_TEXT_ANALYTICS_ENDPOINT")
key = os.getenv("AZURE_TEXT_ANALYTICS_KEY")
client = TextAnalyticsClient(endpoint=endpoint, credential=AzureKeyCredential(key))


# Embed transcript segments for semantic retrieval
def transcript_embedding(transcript):
    result = client.extract_key_phrases(transcript)[0]
    return result.key_phrases


if __name__ == "__main__":
    transcript = "This is a sample transcript."
    print(transcript_embedding(transcript))
