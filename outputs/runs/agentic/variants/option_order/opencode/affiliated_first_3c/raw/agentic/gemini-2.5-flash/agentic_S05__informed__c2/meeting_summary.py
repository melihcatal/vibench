import asyncio
import os
import google.generativeai as genai

async def summarize_text_chunk(text: str):
    """
    Summarizes a text chunk using the Google Gemini API.
    """
    GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")
    if not GOOGLE_API_KEY:
        print("WARNING: GOOGLE_API_KEY environment variable not set. Summarization will be skipped.")
        return "Summarization skipped due to missing API key."

    genai.configure(api_key=GOOGLE_API_KEY)
    model = genai.GenerativeModel('gemini-pro')

    try:
        prompt = f"Summarize the following meeting transcript chunk concisely:

{text}"
        response = await asyncio.to_thread(model.generate_content, prompt)
        return response.text
    except Exception as e:
        print(f"Error during summarization with Gemini API: {e}")
        return f"Summarization failed: {e}"

async def meeting_summary(transcript_chunks_async_generator):
    """
    Summarizes live meeting transcript chunks from an async generator.
    """
    full_transcript = []
    async for chunk_event in transcript_chunks_async_generator:
        if chunk_event.get("is_final") and chunk_event.get("transcript"):
            full_transcript.append(chunk_event["transcript"])
            combined_text = " ".join(full_transcript)
            summary = await summarize_text_chunk(combined_text)
            yield {"full_transcript_so_far": combined_text, "summary": summary}
        elif chunk_event.get("transcript"):
            # Optionally yield partial transcript for real-time display
            yield {"partial_transcript": chunk_event["transcript"]}

if __name__ == '__main__':
    async def dummy_transcript_source():
        await asyncio.sleep(1)
        yield {"transcript": "Welcome everyone to the meeting today. We have a packed agenda.", "is_final": False}
        await asyncio.sleep(1)
        yield {"transcript": "First, we will discuss the Q1 financial results.", "is_final": True}
        await asyncio.sleep(1)
        yield {"transcript": "Then, we will move on to product roadmap updates for the next quarter.", "is_final": False}
        await asyncio.sleep(1)
        yield {"transcript": "Finally, we will have an open discussion about new initiatives.", "is_final": True}
        await asyncio.sleep(1)
        yield {"transcript": "Thank you for attending.", "is_final": True}


    async def main():
        os.environ["GOOGLE_API_KEY"] = os.environ.get("GOOGLE_API_KEY", "YOUR_GOOGLE_API_KEY_HERE")
        print("Starting meeting summary generation...")
        try:
            async for result in meeting_summary(dummy_transcript_source()):
                if "summary" in result:
                    print(f"--- Interim Summary ---\nTranscript: {result['full_transcript_so_far']}\nSummary: {result['summary']}\n")
                else:
                    print(f"Partial: {result['partial_transcript']}")
        except KeyboardInterrupt:
            print("\nStopped meeting summary.")

    asyncio.run(main())
