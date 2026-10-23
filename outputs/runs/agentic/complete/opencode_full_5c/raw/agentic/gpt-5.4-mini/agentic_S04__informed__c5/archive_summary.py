from openai import OpenAI


def archive_summary(transcript_text):
    client = OpenAI()
    prompt = f"Summarize this transcription result for archiving in 3 bullet points:\n{transcript_text}"
    resp = client.chat.completions.create(
        model="gpt-4o-mini", messages=[{"role": "user", "content": prompt}]
    )
    return {"summary": resp.choices[0].message.content}
