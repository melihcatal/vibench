from speech_client import get_openai_client, get_translation_model


def archive_summary(transcript_text):
    client = get_openai_client()
    prompt = f"Summarize this meeting transcript for archival storage:\n{transcript_text}"
    response = client.responses.create(model=get_translation_model(), input=prompt)
    return response.output_text
