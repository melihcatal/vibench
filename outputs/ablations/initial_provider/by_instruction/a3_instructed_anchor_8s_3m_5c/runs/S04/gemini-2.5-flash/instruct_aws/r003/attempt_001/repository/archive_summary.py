from speech_client import get_comprehend_client
from speech_models import SummaryResult

def summarize_transcript(text: str, language_code: str = "en") -> SummaryResult:
    comprehend_client = get_comprehend_client()
    try:
        # Using detect_key_phrases as a form of summarization by extracting important phrases.
        # For more advanced summarization, a generative AI model (e.g., via AWS Bedrock or SageMaker) 
        # would be more suitable, but sticking to Comprehend for direct integration as requested.
        response = comprehend_client.detect_key_phrases(
            Text=text,
            LanguageCode=language_code
        )
        key_phrases = [phrase['Text'] for phrase in response['KeyPhrases']]
        summary_text = ". ".join(key_phrases) + "."

        print(f"Transcript summarized by extracting {len(key_phrases)} key phrases.")
        return SummaryResult(
            original_text=text,
            summary_text=summary_text
        )
    except Exception as e:
        print(f"Error summarizing transcript with AWS Comprehend: {e}")
        raise
