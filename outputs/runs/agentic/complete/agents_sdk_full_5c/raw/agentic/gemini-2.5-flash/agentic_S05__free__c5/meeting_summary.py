import asyncio
import os
from collections import deque
from typing import AsyncIterable, Tuple, List

import openai

# Configure OpenAI API key
# export OPENAI_API_KEY="your-openai-api-key"
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

class MeetingSummarizer:
    def __init__(self, api_key: str, model_name: str = "gpt-4-turbo-preview", summary_window_size: int = 10):
        if not api_key:
            raise ValueError("OpenAI API key must be provided.")
        self.client = openai.OpenAI(api_key=api_key)
        self.model_name = model_name
        self.transcript_buffer = deque(maxlen=summary_window_size) # Store last N final transcripts
        print(f"Initialized MeetingSummarizer with model: {self.model_name}")

    async def summarize_chunk(self, transcript_chunk: str) -> str:
        """Generates a summary for a given chunk of transcript."""
        if not transcript_chunk.strip():
            return ""

        messages = [
            {"role": "system", "content": "You are a helpful assistant that summarizes meeting transcripts. Keep summaries concise and focused on key points."},
            {"role": "user", "content": f"Summarize the following meeting transcript chunk:\n\n{transcript_chunk}"}
        ]
        
        try:
            response = await asyncio.to_thread(
                self.client.chat.completions.create,
                model=self.model_name,
                messages=messages,
                max_tokens=150, # Limit summary length
                temperature=0.7,
            )
            return response.choices[0].message.content.strip()
        except openai.APIError as e:
            print(f"OpenAI API Error during summarization: {e}")
            return "Error summarizing chunk."
        except Exception as e:
            print(f"Unexpected error during summarization: {e}")
            return "Error summarizing chunk."

    async def summarize_recent_dialogue(self) -> str:
        """Summarizes the content in the recent transcript buffer."""
        if not self.transcript_buffer:
            return "No recent dialogue to summarize."
        
        combined_dialogue = " ".join(self.transcript_buffer)
        if not combined_dialogue.strip():
            return "No meaningful dialogue for summary."

        messages = [
            {"role": "system", "content": "You are a helpful assistant that summarizes meeting dialogues. Create a brief summary of the key points discussed recently. Focus on main topics and decisions."},
            {"role": "user", "content": f"Summarize the recent meeting dialogue:\n\n{combined_dialogue}"}
        ]

        try:
            response = await asyncio.to_thread(
                self.client.chat.completions.create,
                model=self.model_name,
                messages=messages,
                max_tokens=200, 
                temperature=0.6,
            )
            return response.choices[0].message.content.strip()
        except openai.APIError as e:
            print(f"OpenAI API Error during summary of recent dialogue: {e}")
            return "Error summarizing recent dialogue."
        except Exception as e:
            print(f"Unexpected error during summary of recent dialogue: {e}")
            return "Error summarizing recent dialogue."

    async def process_live_transcripts(self, transcript_stream: AsyncIterable[Tuple[str, bool]]):
        """Processes a stream of live transcripts and yields summaries."""
        print("\n--- Meeting Summary Pipeline ---")
        async for transcript, is_final in transcript_stream:
            if is_final and transcript.strip():
                self.transcript_buffer.append(transcript)
                print(f"Final Transcript Added: {transcript}")
                
                # Optionally summarize each final chunk or provide periodic full summary
                chunk_summary = await self.summarize_chunk(transcript)
                print(f"  Chunk Summary: {chunk_summary}")
                
                # Provide a rolling summary of recent dialogue every few chunks
                if len(self.transcript_buffer) == self.transcript_buffer.maxlen:
                    recent_summary = await self.summarize_recent_dialogue()
                    print(f"  Recent Dialogue Summary (last {self.transcript_buffer.maxlen} chunks): {recent_summary}")
                    # Clear the buffer after summarizing to start a new window
                    self.transcript_buffer.clear()
                
                yield transcript, chunk_summary, is_final
            elif transcript.strip():
                print(f"Partial Transcript: {transcript}")
                yield transcript, None, is_final

async def mock_meeting_transcript_stream():
    """A mock async generator for meeting transcript chunks."""
    yield "Good morning everyone.", False
    await asyncio.sleep(0.5)
    yield "Good morning everyone. Let's start with the agenda for today.", True
    await asyncio.sleep(1)
    yield "The first item is about Q1 financial results.", True
    await asyncio.sleep(1)
    yield "We saw strong growth in key markets.", False
    await asyncio.sleep(0.5)
    yield "We saw strong growth in key markets, especially in Europe and Asia.", True
    await asyncio.sleep(1)
    yield "The second item is regarding the new product launch next quarter.", True
    await asyncio.sleep(1.5)
    yield "The marketing team has prepared a comprehensive strategy.", True
    await asyncio.sleep(1)
    yield "We need to finalize the budget and allocate resources.", True

async def main():
    api_key = OPENAI_API_KEY
    if not api_key:
        print("Warning: OPENAI_API_KEY environment variable not set. Summarization will not work.")
        print("Please set the OPENAI_API_KEY environment variable.")
        return

    summarizer = MeetingSummarizer(api_key=api_key, summary_window_size=3)
    async for transcript, summary, is_final in summarizer.process_live_transcripts(mock_meeting_transcript_stream()):
        pass # The pipeline function already prints.

if __name__ == "__main__":
    asyncio.run(main())
