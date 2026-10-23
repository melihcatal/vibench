from speech_client import OpenAIHttpClient


def archive_summary(transcript_text: str) -> dict:
    client = OpenAIHttpClient()
    response = client.post(
        "/responses",
        json={
            "model": client.config.openai_reasoning_model,
            "input": f"Summarize this transcription result for archival storage: {transcript_text}",
        },
    )
    response.raise_for_status()
    return response.json()
