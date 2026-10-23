import os
from typing import AsyncIterable

import google.generativeai as genai

from speech_models import TranscriptSegment

async def meeting_summary(transcript_segments: AsyncIterable[TranscriptSegment]):
    # Configure the Gemini API client
    # Ensure GOOGLE_API_KEY is set in your environment variables
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))

    model = genai.GenerativeModel('gemini-pro') # Using gemini-pro for text summarization
    
    full_transcript_buffer = []
    async for segment in transcript_segments:
        full_transcript_buffer.append(segment.text)
        
        # For demonstration, we'll summarize every N final segments or after a certain buffer size.
        # In a real application, you'd likely summarize at intervals or based on meeting structure.
        if segment.is_final and len(full_transcript_buffer) >= 5: # Summarize every 5 final segments
            text_to_summarize = " ".join(full_transcript_buffer)
            prompt = f"Please provide a concise summary of the following meeting transcript chunk: {text_to_summarize}"
            
            try:
                response = model.generate_content(prompt)
                summary = response.text
                print(f"Summary of chunk: {summary}")
                yield {"summary": summary, "source_text": text_to_summarize}
                full_transcript_buffer = [] # Reset buffer after summarization
            except Exception as e:
                print(f"Error generating summary: {e}")
                # Optionally yield an error or handle it differently
                full_transcript_buffer = [] # Clear buffer even on error to prevent re-processing the same chunk
    
    # Summarize any remaining text at the end of the stream
    if full_transcript_buffer:
        text_to_summarize = " ".join(full_transcript_buffer)
        prompt = f"Please provide a concise summary of the following meeting transcript chunk: {text_to_summarize}"
        try:
            response = model.generate_content(prompt)
            summary = response.text
            print(f"Final Summary of remaining chunk: {summary}")
            yield {"summary": summary, "source_text": text_to_summarize}
        except Exception as e:
            print(f"Error generating final summary: {e}")
