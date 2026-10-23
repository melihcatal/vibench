import asyncio
import os
import google.generativeai as genai
from speech_models import LiveCaption

async def summarize_meeting_chunks(transcript_chunks: list[LiveCaption]) -> str:
    """Summarizes live meeting transcript chunks using Google Generative AI (Gemini)."""
    # Configure the API key for Google Generative AI
    # os.environ["GOOGLE_API_KEY"] = "YOUR_GOOGLE_API_KEY"
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))

    # Use the appropriate model for summarization, e.g., 'gemini-pro'
    model = genai.GenerativeModel('gemini-pro')

    full_transcript = " ".join([chunk.text for chunk in transcript_chunks])
    
    if not full_transcript.strip():
        return "No transcript provided for summarization."

    prompt = f"Please summarize the following meeting transcript:
\n{full_transcript}\n\nSummary:"

    print(f"Sending {len(transcript_chunks)} chunks for summarization...")
    try:
        response = model.generate_content(prompt)
        summary = response.text
        print(f"Generated Summary: {summary}")
        return summary
    except Exception as e:
        print(f"Error summarizing with Gemini API: {e}")
        return f"Error during summarization: {e}"

async def main():
    print("Summarizing example meeting transcript chunks...")
    example_chunks = [
        LiveCaption(text="Good morning team, let's start with the Q3 review.", language="en", is_partial=False),
        LiveCaption(text="Sales are up by 15% and marketing campaigns performed well.", language="en", is_partial=False),
        LiveCaption(text="We need to address the customer feedback on product X.", language="en", is_partial=False),
        LiveCaption(text="Action item: John to investigate product X feedback.", language="en", is_partial=False)
    ]

    summary = await summarize_meeting_chunks(example_chunks)
    print(f"Final Meeting Summary: {summary}")

if __name__ == "__main__":
    asyncio.run(main())
