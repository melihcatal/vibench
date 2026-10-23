import google.generativeai as genai
import os

def embed_transcript_segments(text_segments: list[str], model_name: str = "embedding-001") -> list[list[float]]:
    """
    Embeds transcript segments for semantic retrieval using Google Gemini Embeddings.
    Requires GOOGLE_API_KEY environment variable to be set.
    """
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

    embeddings_list = []
    for segment in text_segments:
        try:
            response = genai.embed_content(
                model=model_name,
                content=segment,
                task_type="RETRIEVAL_DOCUMENT"
            )
            embeddings_list.append(response["embedding"])
            print(f"Segment embedded successfully: '{segment[:30]}...'")
        except Exception as e:
            print(f"Error embedding segment '{segment[:30]}...': {e}")
            embeddings_list.append([]) # Append an empty list or handle error as appropriate
    
    return embeddings_list
