from openai import OpenAI
import os

def summarize_transcript_with_openai(transcript_text: str, model: str = "gpt-3.5-turbo") -> str:
    """
    Summarizes transcription results using OpenAI's GPT models.
    """
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are a helpful assistant that summarizes meeting transcripts."},
            {"role": "user", "content": f"Please summarize the following transcript:

{transcript_text}"
            }
        ],
        max_tokens=200
    )

    return response.choices[0].message.content.strip()
