from google.cloud import language_v1
from speech_models import TranscriptionResult, TranscriptionAlternative

def moderate_transcript(transcript_result: TranscriptionResult) -> List[dict]:
    """Moderates transcript text before publishing using Google Cloud Natural Language API.

    Args:
        transcript_result: The TranscriptionResult object containing the transcript to moderate.

    Returns:
        A list of dictionaries, each containing sentiment analysis results for a transcript alternative.
    """
    client = language_v1.LanguageServiceClient()
    
    moderation_results = []

    for alternative in transcript_result.alternatives:
        if not alternative.transcript:
            continue

        document = language_v1.Document(
            content=alternative.transcript,
            type_=language_v1.Document.Type.PLAIN_TEXT
        )
        
        sentiment = client.analyze_sentiment(request={'document': document}).document_sentiment
        
        moderation_results.append({
            "transcript_segment": alternative.transcript,
            "sentiment_score": sentiment.score,
            "sentiment_magnitude": sentiment.magnitude
        })

    return moderation_results
