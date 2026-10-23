import asyncio
from typing import List
import vertexai
from vertexai.preview.generative_models import GenerativeModel, Part, Image
from speech_models import SpeechRecognitionResult

# Google Cloud Generative AI uses the `vertexai` SDK
# and `GenerativeModel` for its operations (e.g., Gemini-Pro).


def initialize_vertex_ai(project: str, location: str):
    vertexai.init(project=project, location=location)


async def summarize_text_chunk(text_chunk: str) -> str:
    """
    Summarizes a single text chunk using Google Cloud Generative AI (Gemini-Pro).

    Args:
        text_chunk: The text chunk to summarize.

    Returns:
        The summarized text.
    """
    # Initialize Vertex AI (ensure project and location are set, e.g., in environment variables
    # or explicitly initialized once in your application startup).
    # For this example, we assume it's initialized elsewhere or will be initialized with dummy values.
    try:
        # Ensure Vertex AI is initialized. Replace with your project and region.
        # This should ideally be done once at application startup.
        # For demonstration, we'll try to initialize it here if not already.
        if not vertexai.initializer._is_initialized:
            initialize_vertex_ai(project="your-gcp-project-id", location="us-central1")
    except Exception:
        # If initialization fails (e.g., project not set), proceed with a warning.
        print(
            "Warning: Vertex AI not explicitly initialized with project/location. "
            "Ensure `gcloud auth application-default login` has been run or "
            "project/location are set programmatically."
        )

    model = GenerativeModel("gemini-pro")

    # A simple prompt for summarization. For better results, consider more elaborate prompting strategies.
    prompt = f"Summarize the following meeting transcript chunk concisely: {text_chunk}"

    response = model.generate_content([prompt])

    if response.candidates and response.candidates[0].content.parts:
        return response.candidates[0].content.parts[0].text
    return ""


async def meeting_summary_stream(caption_stream_generator, buffer_size: int = 5):
    """
    Asynchronously summarizes chunks of live meeting transcripts.

    Args:
        caption_stream_generator: An async generator yielding SpeechRecognitionResult objects.
        buffer_size: Number of final captions to buffer before attempting to summarize.

    Yields:
        Tuple[List[str], str]: Original caption chunks and their summary.
    """
    print("Starting live meeting summary...")
    caption_buffer: List[str] = []
    async for caption_result in caption_stream_generator:
        if caption_result.is_final and caption_result.transcript.strip():
            caption_buffer.append(caption_result.transcript)
            if len(caption_buffer) >= buffer_size:
                text_to_summarize = " ".join(caption_buffer)
                summary = await summarize_text_chunk(text_to_summarize)
                print(f"Summarized {len(caption_buffer)} captions: {summary}")
                yield caption_buffer, summary
                caption_buffer = []
