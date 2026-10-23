import os
import google.generativeai as genai

def summarize_transcript_chunk(transcript_chunk: str) -> str:
    google_api_key = os.environ.get("GOOGLE_API_KEY")

    if not google_api_key:
        raise ValueError("Please set GOOGLE_API_KEY environment variable.")

    genai.configure(api_key=google_api_key)

    # Using the gemini-pro model for text generation
    model = genai.GenerativeModel('gemini-pro')

    prompt = f"Summarize the following meeting transcript chunk in one concise sentence:\n\n{transcript_chunk}\n\nSummary:"

    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        print(f"Error summarizing transcript: {e}")
        return f"[Summary Failed: {transcript_chunk}]"

if __name__ == "__main__":
    # Example usage
    sample_chunk_1 = (
        "The team discussed the Q3 budget. Sarah presented the marketing spend, "
        "and John raised concerns about the overhead costs. We agreed to revisit the "
        "figures next Tuesday. Also, the new project proposal was briefly touched upon."
    )
    summary_1 = summarize_transcript_chunk(sample_chunk_1)
    print(f"\nChunk 1:\n{sample_chunk_1}\nSummary 1:\n{summary_1}")

    sample_chunk_2 = (
        "Action items from the previous meeting were reviewed. Mark completed the "
        "client report, and Emily finalized the design mockups. The next steps "
        "involve client feedback collection and preparing for the deployment phase."
    )
    summary_2 = summarize_transcript_chunk(sample_chunk_2)
    print(f"\nChunk 2:\n{sample_chunk_2}\nSummary 2:\n{summary_2}")
