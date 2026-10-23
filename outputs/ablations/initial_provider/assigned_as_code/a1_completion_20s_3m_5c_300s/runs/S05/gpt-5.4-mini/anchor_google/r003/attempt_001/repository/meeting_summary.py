from speech_client import vertex_ai_init
from speech_models import SummaryRequest, normalize_transcript
from vertexai.generative_models import GenerativeModel


def meeting_summary(payload, config=None):
    vertex_ai_init()
    request = SummaryRequest(transcript_chunks=payload["transcript_chunks"])
    model = GenerativeModel("gemini-1.5-pro")
    prompt = "Summarize this meeting transcript:\n" + "\n".join(normalize_transcript(chunk) for chunk in request.transcript_chunks)
    response = model.generate_content(prompt)
    return {"summary": response.text}
