from openai import OpenAI
from speech_client import load_config


def archive_summary(transcript_text: str):
    cfg = load_config()
    client = OpenAI(api_key=cfg.api_key, organization=cfg.organization, project=cfg.project)
    return client.responses.create(
        model="gpt-4o-mini",
        input=f"Summarize this transcription for archival indexing:\n{transcript_text}",
    )
