from google.cloud import generativelanguage_v1beta as glm

from speech_models import normalize_transcript


def summarize_meeting(chunks: list[str]) -> str:
    client = glm.TextServiceClient()
    text = "\n".join(normalize_transcript(chunk) for chunk in chunks if chunk.strip())
    response = client.summarize_text(parent="models/text-bison-001", instances=[{"content": text}])
    return getattr(response, "summary", "")
