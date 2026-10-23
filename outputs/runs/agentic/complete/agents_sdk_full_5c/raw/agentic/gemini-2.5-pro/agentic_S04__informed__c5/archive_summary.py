import os
from openai import OpenAI


def summarize_transcript(transcript_text: str) -> str:
    """
    Summarizes a long transcript using the OpenAI GPT model.

    Args:
        transcript_text: The full text of the transcription.

    Returns:
        A concise summary of the transcript.
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set.")

    client = OpenAI(api_key=api_key)

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant that summarizes meeting transcripts. "
                               "Provide a concise summary covering the key topics and action items discussed.",
                },
                {"role": "user", "content": transcript_text},
            ],
            temperature=0.5,
            max_tokens=256,
        )
        summary = response.choices[0].message.content
        return summary.strip() if summary else "No summary could be generated."
    except Exception as e:
        print(f"An error occurred while summarizing: {e}")
        raise

