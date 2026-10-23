from google.cloud import language
from google.cloud.language import enums

# Configuration
PROJECT_ID = 'your-project-id'

# Initialize client
client = language.LanguageServiceClient()

# Function to moderate profile text
def moderate_profile_text(text):
    document = language.Document(content=text, type_=enums.Document.Type.PLAIN_TEXT)
    response = client.analyze_sentiment(document)
    sentiment = response.document_sentiment
    if sentiment.score < -0.2:
        return 'Moderation required'
    return 'Moderation not required'