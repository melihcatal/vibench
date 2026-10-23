import os
from openai import OpenAI

def summarize_transcript(transcript_text: str) -> str:
    """
    Summarizes the transcript text using OpenAI GPT model.
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY is not set in environment variables.")

    client = OpenAI(api_key=api_key)
    
    prompt = f"Please provide a concise summary of the following transcript:\n\n{transcript_text}"
    
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an expert summarizer."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.7,
            max_tokens=150,
        )
        summary = response.choices[0].message.content
        return summary.strip() if summary else "Could not generate summary."
    except Exception as e:
        return f"An error occurred with the OpenAI API: {e}"
