from speech_client import get_client


def archive_summary(transcript_text: str):
    client = get_client()
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Summarize transcription results for archival storage."},
            {"role": "user", "content": transcript_text},
        ],
        temperature=0.3,
    )
    summary = completion.choices[0].message.content or ""
    return {"summary": summary, "raw": completion.model_dump()}
