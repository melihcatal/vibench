from speech_client import build_client, get_openai_text_model


def archive_summary(transcript_text: str):
    client = build_client()
    return client.responses.create(
        model=get_openai_text_model(),
        input=f"Summarize this transcription for archival indexing:\n{transcript_text}",
    )
