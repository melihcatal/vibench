import boto3
import os
from database_client import get_comprehend_client
from database_models import DocumentSummary

def summarize_document_text(document_id: str, text_content: str, language_code: str = 'en') -> DocumentSummary:
    """
    Summarizes retrieved document records using AWS Comprehend.
    Note: Comprehend does not have a direct 'summarize' API. This function will use
    detect_key_phrases to extract keywords as a form of summarization.
    For true summarization, a custom model or a different service might be needed.
    """
    comprehend = get_comprehend_client()
    try:
        # Using detect_key_phrases as a proxy for summarization/key content extraction
        key_phrases_response = comprehend.detect_key_phrases(
            Text=text_content,
            LanguageCode=language_code
        )
        key_phrases = [kp['Text'] for kp in key_phrases_response.get('KeyPhrases', [])]

        # For a simple summary, we can just join the key phrases or use the first few sentences
        # as a placeholder since Comprehend doesn't have a direct summarization API.
        # A more sophisticated approach would involve more NLP.
        summary_text = "; ".join(key_phrases)
        if not summary_text and text_content:
            # Fallback to the first sentence if no key phrases are found
            summary_text = text_content.split('.', 1)[0] + "." if '.' in text_content else text_content
            if len(summary_text) > 200: # Limit length if it's too long
                summary_text = summary_text[:200] + "..."

        return DocumentSummary(
            document_id=document_id,
            summary_text=summary_text,
            keywords=key_phrases
        )
    except Exception as e:
        print(f"Error summarizing document text with AWS Comprehend: {e}")
        raise
