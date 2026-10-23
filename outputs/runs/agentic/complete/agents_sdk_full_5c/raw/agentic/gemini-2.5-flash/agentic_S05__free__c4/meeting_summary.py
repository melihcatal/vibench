from google.cloud import aiplatform
import os

def summarize_text_vertex_ai(
    text: str,
    project_id: str,
    location: str = "us-central1",
    model_id: str = "text-bison@001", # Concrete model identifier for summarization
    temperature: float = 0.2,
    max_output_tokens: int = 256,
    top_p: float = 0.8,
    top_k: int = 40,
) -> str:
    """
    Summarizes a given text using a Google Cloud Vertex AI generative model.

    Args:
        text: The text content to summarize.
        project_id: The Google Cloud project ID.
        location: The Vertex AI endpoint location.
        model_id: The specific model ID for summarization (e.g., "text-bison@001").
        temperature: Controls the randomness of the output. Lower values mean less random.
        max_output_tokens: Maximum number of tokens to generate in the summary.
        top_p: The maximum cumulative probability of tokens to consider for sampling.
        top_k: The maximum number of tokens to consider for sampling.

    Returns:
        The summarized text.
    """
    aiplatform.init(project=project_id, location=location)

    from vertexai.preview.language_models import TextGenerationModel

    model = TextGenerationModel.from_pretrained(model_id)

    prompt = f"Summarize the following meeting transcript:\n\n{text}\n\nSummary:"

    response = model.predict(
        prompt,
        temperature=temperature,
        max_output_tokens=max_output_tokens,
        top_p=top_p,
        top_k=top_k,
    )
    return response.text

async def summarize_meeting_transcript_chunks(transcript_stream_gen, project_id: str, min_chunk_size: int = 1000):
    """
    Aggregates transcript chunks and summarizes them when a sufficient size is reached.

    Args:
        transcript_stream_gen: An async generator yielding (transcript, is_final) tuples.
        project_id: Your Google Cloud project ID.
        min_chunk_size: Minimum character length of aggregated transcript before summarizing.

    Yields:
        Tuples of (summary_text, original_chunk_count) when a summary is generated.
    """
    current_transcript_buffer = []
    current_buffer_length = 0
    chunk_count = 0

    async for transcript, is_final in transcript_stream_gen:
        if transcript.strip():
            current_transcript_buffer.append(transcript)
            current_buffer_length += len(transcript)
            chunk_count += 1

            if is_final and current_buffer_length >= min_chunk_size:
                full_chunk = " ".join(current_transcript_buffer)
                summary = summarize_text_vertex_ai(full_chunk, project_id)
                yield summary, chunk_count

                # Reset buffer after summarizing
                current_transcript_buffer = []
                current_buffer_length = 0
                chunk_count = 0
            elif is_final and current_transcript_buffer: # Summarize even if small, if it's the very end of a segment
                 full_chunk = " ".join(current_transcript_buffer)
                 summary = summarize_text_vertex_ai(full_chunk, project_id)
                 yield summary, chunk_count
                 current_transcript_buffer = []
                 current_buffer_length = 0
                 chunk_count = 0

    # Summarize any remaining text in the buffer at the very end of the stream
    if current_transcript_buffer and current_buffer_length > 0:
        full_chunk = " ".join(current_transcript_buffer)
        summary = summarize_text_vertex_ai(full_chunk, project_id)
        yield summary, chunk_count

if __name__ == '__main__':
    # Example usage:
    # import asyncio
    #
    # GOOGLE_CLOUD_PROJECT = os.getenv("GOOGLE_CLOUD_PROJECT", "your-gcp-project-id")
    #
    # async def dummy_transcript_source():
    #     yield "Hello everyone, welcome to the meeting today.", False
    #     await asyncio.sleep(0.1)
    #     yield "We will be discussing the Q3 financial results and future projections.", True
    #     await asyncio.sleep(0.1)
    #     yield "The marketing team will present their strategy for the new product launch next month.", False
    #     await asyncio.sleep(0.1)
    #     yield "Sales have been strong, exceeding our expectations in Europe and Asia.", True
    #     await asyncio.sleep(0.1)
    #     yield "However, we need to improve our market share in North America.", False
    #     await asyncio.sleep(0.1)
    #     yield "Any questions or comments from the team?", True
    #
    # async def main():
    #     print(f"Summarizing meeting transcripts for project {GOOGLE_CLOUD_PROJECT}...")
    #     async for summary, original_chunks in summarize_meeting_transcript_chunks(
    #         dummy_transcript_source(), GOOGLE_CLOUD_PROJECT, min_chunk_size=100
    #     ):
    #         print(f"--- Summary of {original_chunks} chunks ---")
    #         print(summary)
    #
    # if GOOGLE_CLOUD_PROJECT == "your-gcp-project-id":
    #     print("Please set the GOOGLE_CLOUD_PROJECT environment variable or replace 'your-gcp-project-id'.")
    # else:
    #     asyncio.run(main())
    pass
