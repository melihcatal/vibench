import os
from openai import OpenAI
from typing import List
from dotenv import load_dotenv

load_dotenv()

def embed_text_segments(segments: List[str], model: str = "text-embedding-ada-002") -> List[List[float]]:
    """
    Embeds transcript segments using OpenAI Embeddings API.
    """
    client = OpenAI(
        api_key=os.getenv("OPENAI_API_KEY"),
    )

    try:
        response = client.embeddings.create(input=segments, model=model)
        return [data.embedding for data in response.data]
    except Exception as e:
        print(f"Error generating embeddings with OpenAI: {e}")
        return []

if __name__ == "__main__":
    # Example usage (ensure OPENAI_API_KEY is set in your .env file)
    # sample_segments = [
    #     "Good morning everyone. Let's start the meeting.",
    #     "I'd like to discuss the new project timeline.",
    #     "The timeline has been updated. We're looking at a launch in Q4.",
    #     "That's a bit later than expected. Can we expedite some phases?"
    # ]
    # embeddings = embed_text_segments(sample_segments)
    # if embeddings:
    #     print(f"Generated {len(embeddings)} embeddings. First embedding shape: {len(embeddings[0])}")
    #     # print("First embedding:", embeddings[0])
    # else:
    #     print("Failed to generate embeddings.")
    pass
