import os
from googleapiclient import discovery
from googleapiclient.errors import HttpError
from identity_models import RegisterUserRequest

# Initialize Google Cloud Natural Language API client
client = discovery.build(
    "language", 
    "v1", 
    developerKey=os.getenv("GOOGLE_API_KEY"),
    discoveryServiceUrl="https://language.googleapis.com/$discovery/rest?version=v1"
)


def moderate_profile_text(text: str) -> bool:
    """Moderate profile text using Google Cloud Natural Language API."""
    try:
        request_body = {
            "document": {
                "type": "PLAIN_TEXT",
                "content": text
            },
            "encodingType": "UTF8"
        }
        response = client.documents().analyzeSentiment(body=request_body).execute()
        sentiment = response.get("documentSentiment", {}).get("score", 0)
        
        # Check for toxic content using sentiment score and magnitude
        if sentiment < -0.5:
            return False
        
        # Additional check for explicit content
        response = client.documents().analyzeEntitySentiment(body=request_body).execute()
        for entity in response.get("entities", []):
            if entity.get("salience", 0) > 0.5 and entity.get("sentiment", {}).get("score", 0) < -0.7:
                return False
        
        return True
    except HttpError as e:
        print(f"Moderation error: {e}")
        return False