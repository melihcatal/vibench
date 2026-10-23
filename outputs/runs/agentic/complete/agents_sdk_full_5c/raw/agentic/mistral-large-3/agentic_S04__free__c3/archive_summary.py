from google.cloud import language_v1
from speech_models import SummaryRequest, SummaryResult

def archive_summary(request: SummaryRequest) -> SummaryResult:
    """Summarize transcription results using Google Cloud Natural Language API."""
    client = language_v1.LanguageServiceClient()
    document = language_v1.Document(
        content=request.transcript, type_=language_v1.Document.Type.PLAIN_TEXT
    )
    response = client.analyze_entities(request={"document": document})
    entities = [entity.name for entity in response.entities]
    summary = f"Key entities: {', '.join(entities)}. Summary: {request.transcript[:200]}..."
    return SummaryResult(summary=summary)