import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv() # Load environment variables from .env file

# OpenAI API Key from environment variable
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY environment variable not set.")

client = OpenAI(api_key=OPENAI_API_KEY)

def summarize_meeting_chunk(transcript_chunk: str, model: str = "gpt-3.5-turbo") -> str:
    """
    Summarizes a chunk of live meeting transcript using OpenAI GPT.
    """
    if not transcript_chunk.strip():
        return ""

    print(f"Summarizing chunk using OpenAI {model}...")
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant that summarizes meeting transcripts concisely."},
                {"role": "user", "content": f"Summarize the following meeting transcript chunk:\n\n{transcript_chunk}\n\nSummary:"}
            ],
            temperature=0.7,
            max_tokens=150,
            top_p=1.0,
            frequency_penalty=0.0,
            presence_penalty=0.0
        )
        summary = response.choices[0].message.content.strip()
        return summary
    except Exception as e:
        print(f"Error summarizing with OpenAI GPT: {e}")
        return f"Error summarizing: {e}"

if __name__ == "__main__":
    # This is a placeholder for receiving live transcript chunks.
    dummy_transcript_chunks = [
        "The team discussed the Q3 marketing strategy, focusing on digital ad spend and social media campaigns. John presented the preliminary results from the A/B testing, showing a 15% improvement in click-through rates for variant B.",
        "Sarah brought up concerns about budget allocations for the new product launch. We need to review the financial projections next week. A follow-up meeting was scheduled for Friday to iron out the details.",
        "Action items include: John to prepare a detailed report on A/B testing. Sarah to update the budget spreadsheet. Everyone to review the Q3 marketing plan before the next meeting."
    ]

    print("Starting meeting summary simulation...")
    for i, chunk in enumerate(dummy_transcript_chunks):
        print(f"\n--- Chunk {i+1} ---")
        print(f"Original: {chunk}")
        summary = summarize_meeting_chunk(chunk)
        print(f"Summary: {summary}")
