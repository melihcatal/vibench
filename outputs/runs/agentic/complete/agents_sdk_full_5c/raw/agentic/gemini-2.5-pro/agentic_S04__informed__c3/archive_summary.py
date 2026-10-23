import os
from openai import OpenAI

def summarize_transcript(transcript_text: str) -> str:
    """
    Summarizes a transcript using the OpenAI Chat Completions API.
    """
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    if not client.api_key:
        raise ValueError("OPENAI_API_KEY environment variable is not set.")

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant designed to summarize meeting transcripts."
                },
                {
                    "role": "user",
                    "content": f"Please provide a concise summary of the following transcript:\n\n{transcript_text}"
                }
            ],
            temperature=0.5,
            max_tokens=256,
        )
        summary = response.choices[0].message.content
        return summary.strip() if summary else "Could not generate summary."

    except Exception as e:
        print(f"An error occurred with the OpenAI API: {e}")
        return "Error: Could not generate summary."
