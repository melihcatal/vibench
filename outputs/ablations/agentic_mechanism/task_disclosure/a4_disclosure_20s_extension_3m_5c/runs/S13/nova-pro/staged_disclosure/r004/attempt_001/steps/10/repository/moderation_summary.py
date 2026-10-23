from azure.cognitiveservices.vision.contentmoderator import ContentModeratorClient
from msrest.authentication import CognitiveServicesCredentials

# Initialize the Content Moderator client
client = ContentModeratorClient(credentials=CognitiveServicesCredentials('YOUR_API_KEY'), endpoint='https://YOUR_ENDPOINT.cognitiveservices.azure.com/')

def summarize_moderation_decisions(text):
    # Call the Content Moderator API to moderate the text
    moderation_result = client.text_moderation.screen_text(text=text, language='eng', autocorrect=True, pii=True, classify=True)
    
    # Summarize the moderation decisions
    summary = {
        'status': moderation_result.status,
        'is_adult_classified': moderation_result.adult_classification_result.is_adult_classified,
        'is_racy_classified': moderation_result.racy_classification_result.is_racy_classified,
        'is_spam_classified': moderation_result.spam_classification_result.is_spam_classified,
        'detected_language': moderation_result.detected_language,
        'autocorrect_result': moderation_result.autocorrect_result,
        'pii_result': moderation_result.pii_result,
        'classification_result': moderation_result.classification_result
    }
    return summary

# Example usage
text = 'This is a sample text for moderation.'
summary = summarize_moderation_decisions(text)
print(summary)