from google.cloud import generativelanguage_v1beta as genai

from speech_models import normalize_text


def meeting_summary(payload, config=None):
    config = config or {}
    client = genai.TextServiceClient()
    prompt = normalize_text(" ".join(payload.get("chunks", [])))
    response = client.generate_text(request={"model": config.get("model", "models/text-bison-001"), "prompt": {"text": prompt}})
    return {"summary": response.candidates[0].output if response.candidates else ""}
