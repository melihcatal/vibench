from openai import OpenAI


def archive_summary(segments):
    client = OpenAI()
    text = "\n".join(segment.get("text", "") for segment in segments)
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {
                "role": "user",
                "content": f"Summarize this transcription for archival use:\n{text}",
            }
        ],
    )
    return response.choices[0].message.content
