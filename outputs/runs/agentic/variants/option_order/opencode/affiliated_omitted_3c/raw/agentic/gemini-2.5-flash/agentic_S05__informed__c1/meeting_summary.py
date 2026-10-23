import os
from openai import OpenAI  # Using OpenAI chat completions API


def summarize_meeting_chunks(text_chunks: list[str]):
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable must be set.")

    client = OpenAI(api_key=api_key)

    full_text = " ".join(text_chunks)

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  # Using GPT-3.5-turbo model
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant that summarizes meeting transcripts.",
                },
                {
                    "role": "user",
                    "content": f"Please summarize the following meeting transcript: {full_text}",
                },
            ],
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"OpenAI summary error: {e}")
        return None
