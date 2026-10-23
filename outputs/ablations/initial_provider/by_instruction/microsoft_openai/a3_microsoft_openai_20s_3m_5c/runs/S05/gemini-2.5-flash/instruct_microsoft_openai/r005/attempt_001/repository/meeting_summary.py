import os
import asyncio
from anthropic import Anthropic
from typing import AsyncGenerator, Dict, Any

# Anthropic Claude client setup
# Ensure ANTHROPIC_API_KEY environment variable is set.

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

async def summarize_meeting_chunks(transcript_chunk_generator: AsyncGenerator[str, None], model_name: str = "claude-3-opus-20240229") -> AsyncGenerator[Dict[str, Any], None]:
    if not ANTHROPIC_API_KEY:
        print("WARNING: Anthropic API key is not set. Please set ANTHROPIC_API_KEY environment variable.")
        # In a real application, you might raise an error or exit.
        # For this example, we will proceed but it will fail if the key is truly missing.
        return

    client = Anthropic(api_key=ANTHROPIC_API_KEY)

    print(f"Starting meeting summarization using Anthropic Claude model: {model_name}...")
    print("Please ensure your ANTHROPIC_API_KEY is correctly set.")

    async for transcript_chunk in transcript_chunk_generator:
        if not transcript_chunk.strip():
            continue

        try:
            # Anthropic API call for summarization
            # For real-time chunks, we summarize each chunk. 
            # A more sophisticated system might accumulate chunks and summarize periodically.
            response = client.messages.create(
                model=model_name,
                max_tokens=100, # Limit summary length for chunks
                messages=[
                    {
                        "role": "user",
                        "content": f"Summarize the following meeting transcript chunk concisely: {transcript_chunk}"
                    }
                ]
            )
            summary = response.content[0].text if response.content else ""
            
            yield {
                "transcript_chunk": transcript_chunk,
                "summary": summary.strip()
            }

        except Exception as e:
            print(f"Error summarizing transcript chunk '{transcript_chunk}': {e}")
            yield {"error": str(e), "transcript_chunk": transcript_chunk}

if __name__ == "__main__":
    async def dummy_transcript_stream():
        chunks = [
            "Good morning everyone. Today we are going to discuss the Q3 financial results. Overall, the revenue has increased by 15%.",
            "However, operating expenses also saw a slight rise due to new marketing campaigns launched last month.",
            "We need to review the budget for next quarter and ensure we are on track with our profitability goals. John, can you provide an update on the marketing ROI?",
            "Yes, the initial numbers for the new campaign look promising, but it's still early to see the full impact. We expect more data next week."
        ]
        for chunk in chunks:
            await asyncio.sleep(2) # Simulate chunks arriving over time
            yield chunk

    async def main():
        print("Running meeting summary example with Anthropic Claude.")
        async for result in summarize_meeting_chunks(dummy_transcript_stream()):
            if "summary" in result:
                print(f"Chunk: '{result['transcript_chunk']}'")
                print(f"Summary: {result['summary']}")
                print("---------------------")
            elif "error" in result:
                print(f"Error summarizing chunk '{result['transcript_chunk']}': {result['error']}")

    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Summarization stopped.")
    except Exception as e:
        print(f"An error occurred: {e}")
