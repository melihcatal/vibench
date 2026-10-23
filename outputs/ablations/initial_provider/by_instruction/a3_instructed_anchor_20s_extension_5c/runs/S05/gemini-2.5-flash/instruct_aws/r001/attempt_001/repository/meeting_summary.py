import asyncio
from google.cloud import aiplatform
import os

# Initialize Vertex AI (replace with your project and location)
# In a real application, ensure these are set in your environment or explicitly passed.
PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT_ID", "your-gcp-project-id")
LOCATION = os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1")

# Initialize Vertex AI SDK if not already done. This should ideally be done once.
try:
    aiplatform.init(project=PROJECT_ID, location=LOCATION)
except RuntimeError as e:
    if "Vertex AI SDK has already been initialized" in str(e):
        pass # Already initialized, safe to ignore
    else:
        raise

async def summarize_meeting_chunks(transcript_chunk_async_generator, model_name="gemini-pro"):
    """
    Summarizes live meeting transcript chunks using Google Cloud Vertex AI's TextGenerationModel.

    Args:
        transcript_chunk_async_generator: An async generator that yields transcript chunks (strings).
        model_name (str): The name of the Vertex AI model to use for summarization (e.g., "gemini-pro").

    Yields:
        A dictionary containing the original chunk and its summarized version.
    """
    try:
        # Ensure the model is loaded asynchronously if available or handle blocking call appropriately
        # For simplicity, we'll assume synchronous model loading and asynchronous prediction.
        model = aiplatform.GenerativeModel(model_name=model_name)
    except Exception as e:
        print(f"Error loading Vertex AI model '{model_name}': {e}")
        return

    print(f"Summarizing meeting transcripts using Vertex AI model: {model_name}...")

    async for chunk in transcript_chunk_async_generator:
        if not chunk.strip():
            continue

        prompt = f"Summarize the following meeting transcript chunk concisely: {chunk}"

        try:
            response = await asyncio.to_thread(model.generate_content, prompt)
            # Accessing response attributes, assuming TextGenerationResponse structure
            if response.candidates and response.candidates[0].content.parts:
                summary = response.candidates[0].content.parts[0].text
                yield {"original_chunk": chunk, "summary": summary}
            else:
                yield {"original_chunk": chunk, "summary": "No summary generated."}
        except Exception as e:
            print(f"Error during summarization: {e}")
            yield {"original_chunk": chunk, "summary": f"Error summarizing: {e}"}

if __name__ == "__main__":
    async def mock_transcript_chunks():
        yield "The team discussed the Q3 sales report. John presented the key figures, highlighting a 15% increase in revenue. Sarah raised concerns about market competition in the upcoming quarter."
        await asyncio.sleep(1)
        yield "Further discussion ensued regarding the marketing strategy. It was decided that a new digital campaign targeting younger demographics would be launched next month. The budget for this campaign was approved."
        await asyncio.sleep(1)
        yield "Action items include John finalizing the Q3 report, Sarah researching competitor strategies, and Mark starting the new marketing campaign planning."

    async def main():
        print("Starting meeting summarization...")
        async for result in summarize_meeting_chunks(mock_transcript_chunks()):
            print(f"Original Chunk: {result["original_chunk"]}\nSummary: {result["summary"]}\n")

    asyncio.run(main())
