import google.generativeai as genai
import os
from speech_models import TranscriptResult

class MeetingSummarizer:
    def __init__(self, model_name: str = "gemini-pro"):
        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("Please set the GEMINI_API_KEY environment variable.")
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(model_name)

    async def summarize_chunk(self, transcript_chunk: str) -> str:
        if not transcript_chunk.strip():
            return ""
        
        prompt = f"Summarize the following meeting transcript chunk in a concise way:\n\n{transcript_chunk}\n\nSummary:"
        
        try:
            response = await self.model.generate_content_async(prompt)
            summary = response.text
            print(f"Chunk Summary: {summary}")
            return summary
        except Exception as e:
            print(f"Error summarizing chunk: {e}")
            return f"Error: Could not summarize chunk due to {e}"

if __name__ == "__main__":
    # Example usage
    summarizer = MeetingSummarizer()
    sample_transcript_chunk = """
    Good morning everyone. Today we're going to discuss the Q3 financial results. 
    Overall, the revenue increased by 15% compared to Q2, which is a great achievement. 
    However, expenses also rose due to increased marketing spend. We need to optimize our marketing strategy 
    to ensure better ROI in Q4. John, can you elaborate on the marketing expenses?
    """
    
    async def run_summary_example():
        summary = await summarizer.summarize_chunk(sample_transcript_chunk)
        print(f"Full summary: {summary}")

    import asyncio
    asyncio.run(run_summary_example())
