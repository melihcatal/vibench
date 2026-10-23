import os
from openai import OpenAI


def summarize_transcript(transcript_text: str) -> str:
    """
    Summarizes a long transcript using the OpenAI GPT-4o-mini model.
    """
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant designed to summarize meeting transcripts.",
                },
                {
                    "role": "user",
                    "content": f"Please provide a concise summary of the following transcript:\n\n{transcript_text}",
                },
            ],
            temperature=0.5,
            max_tokens=256,
        )
        summary = response.choices[0].message.content
        return summary if summary else "No summary could be generated."
    except Exception as e:
        return f"An error occurred during summarization: {e}"
