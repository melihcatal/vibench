from speech_client import get_client, get_text_model, normalize_text


def archive_summary(transcript_result):
    client = get_client()
    text = normalize_text(
        getattr(transcript_result, "text", "") or transcript_result.get("text", "")
    )
    response = client.responses.create(
        model=get_text_model(),
        input=[
            {
                "role": "system",
                "content": "Summarize transcription results for archival metadata.",
            },
            {"role": "user", "content": text},
        ],
    )
    return response.output_text
