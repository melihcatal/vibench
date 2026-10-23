from google.cloud import language_v1
from speech_models import FinalResult

client = language_v1.LanguageServiceClient()

def check_unsafe_content(result: FinalResult) -> bool:
    text = result.transcript
    document = language_v1.Document(
        content=text, type_=language_v1.Document.Type.PLAIN_TEXT
    )
    response = client.analyze_sentiment(
        request={"document": document, "encoding_type": language_v1.EncodingType.UTF8}
    )
    sentiment = response.document_sentiment
    
    # Check for toxic content using sentiment score as a proxy
    return sentiment.score < -0.7 or sentiment.magnitude > 0.8