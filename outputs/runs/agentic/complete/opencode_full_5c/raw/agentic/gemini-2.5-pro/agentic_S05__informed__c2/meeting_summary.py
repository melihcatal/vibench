import os
from openai import OpenAI


def summarize_meeting_chunk(transcript_chunk: str):
    """
    Summarizes a chunk of a meeting transcript using OpenAI's GPT models.
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set.")

    try:
        client = OpenAI(api_key=api_key)
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant that summarizes meeting transcripts. "
                    "Provide a concise summary of the following transcript chunk.",
                },
                {"role": "user", "content": transcript_chunk},
            ],
            temperature=0.5,
            max_tokens=150,
        )
        summary = response.choices[0].message.content
        return summary
    except Exception as e:
        print(f"OpenAI API error: {e}")
        return None
