import asyncio
from openai import OpenAI
from speech_client import SpeechClient
from speech_models import TranscriptResult

async def summarize_meeting_transcript_chunk(transcript_text: str) -> str:
    client = SpeechClient().get_openai_client()

    if not client.api_key:
        print("OpenAI API key not configured. Please set OPENAI_API_KEY environment variable.")
        return ""

    # OpenAI model identification signal: 'chat.completions.create' method and 'model' parameter
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo", # Or "gpt-4", etc. depending on availability and desired quality
            messages=[
                {"role": "system", "content": "You are a helpful assistant that summarizes meeting transcripts concisely."},
                {"role": "user", "content": f"Summarize the following meeting transcript chunk:\n\n{transcript_text}"}
            ],
            temperature=0.7, # Adjust for creativity vs. factual accuracy
            max_tokens=150, # Limit summary length
        )
        summary = response.choices[0].message.content.strip()
        return summary
    except Exception as e:
        print(f"Error summarizing transcript chunk with OpenAI: {e}")
        return ""

async def simulated_transcript_chunks(num_chunks: int = 3):
    chunks = [
        "The team discussed the Q3 marketing strategy, focusing on digital campaigns and social media outreach. Key performance indicators were reviewed, showing a slight dip in engagement but an increase in conversion rates.",
        "Action items include revising the content calendar, allocating more budget to influencer marketing, and scheduling a follow-up meeting to finalize the ad copy for the new product launch.",
        "John suggested exploring new platforms like TikTok for brand visibility, while Sarah emphasized the importance of A/B testing all new creative assets before full deployment."
    ]
    for i in range(min(num_chunks, len(chunks))):
        yield TranscriptResult(transcript=chunks[i], is_partial=False, language_code="en-US")
        await asyncio.sleep(1)

if __name__ == "__main__":
    async def main():
        print("Demonstrating meeting summary generation using OpenAI.")
        full_transcript = []
        async for chunk_result in simulated_transcript_chunks():
            full_transcript.append(chunk_result.transcript)
            print(f"Processing chunk: {chunk_result.transcript}")
            summary = await summarize_meeting_transcript_chunk(chunk_result.transcript)
            print(f"Chunk Summary: {summary}\n")

        if full_transcript:
            print("--- Final Summary of all chunks (simulated as one request) ---")
            final_summary = await summarize_meeting_transcript_chunk(" ".join(full_transcript))
            print(f"Combined Summary: {final_summary}")
    asyncio.run(main())
