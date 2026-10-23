import boto3

def embed_crypto_audit_notes(audit_note_text: str) -> dict:
    comprehend_client = boto3.client('comprehend')
    
    # Detect key phrases from the audit note
    key_phrases_response = comprehend_client.detect_key_phrases(Text=audit_note_text, LanguageCode='en')
    key_phrases = [phrase['Text'] for phrase in key_phrases_response['KeyPhrases']]

    # For semantic search, a more advanced approach would involve a dedicated embedding model
    # like those available through Amazon SageMaker or a pre-trained model.
    # For this example, we are using key phrases as a simplified representation for search.

    return {
        "original_note": audit_note_text,
        "extracted_key_phrases": key_phrases,
        "provider": "AWS Comprehend"
    }
