from google.cloud import language_v1 as language

from speech_models import ArchiveSummaryRequest, normalize_transcript_text


def archive_summary(transcript):
    client = language.LanguageServiceClient()
    text = normalize_transcript_text(transcript)
    request = ArchiveSummaryRequest(transcript=text)
    document = language.Document(content=request.transcript, type_=language.Document.Type.PLAIN_TEXT)
    response = client.analyze_syntax(document=document)
    return {
        "tokens": len(response.tokens),
        "language": response.language,
    }
