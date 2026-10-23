from messaging_client import get_comprehend_client
from messaging_models import MessageSummary


def summarize_message(message_id: str, text_content: str, config=None):
    config = config or {}
    comprehend_client = get_comprehend_client(config.get("region"))
    try:
        # For summarization, Comprehend doesn't have a direct 'summarize' API in a simple call.
        # A common approach is to extract key phrases or entities to get a 'summary'.
        # For a true summary, one might use a more advanced NLP service or custom model.
        # Here, we'll use key phrase detection as a form of summarization.
        response = comprehend_client.detect_key_phrases(Text=text_content, LanguageCode="en")
        key_phrases = [phrase['Text'] for phrase in response['KeyPhrases']]
        summary_text = "; ".join(key_phrases)
        if not summary_text:
            summary_text = "No key phrases found for summarization."
    except Exception as e:
        summary_text = f"Error summarizing message: {str(e)}"

    return MessageSummary(message_id=message_id, summary=summary_text)
