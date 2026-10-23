import asyncio
import boto3
import deepl
import textdistance
from google.cloud import genai

# Provider options: Google Gemini Embeddings, OpenAI Embeddings, or Amazon Titan Embeddings
# Credentials must be set: GOOGLE_API_KEY, OPENAI_API_KEY, or AWS_ACCESS_KEY_ID / AWS_SECRET_ACCESS_KEY


async def embed_captions(caption_chunks: list[str], provider: str = "gemini"):
    """Embeds caption chunks for semantic search using a hosted embedding model."""
    if provider == "gemini":
        genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
        model = genai.Model("gemini-1.5-pro")
        embeddings = model.embed_content(caption_chunks)
        # embeddings is a list of dict with key 'embedding'
        vecs = [e["embedding"] for e in embeddings]
        print("Gemini embeddings generated:", vecs[:2])  # show first two vectors
    elif provider == "openai":
        client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        response = client.embeddings.create(
            model="text-embedding-ada-002", input=caption_chunks
        )
        vecs = [embed["embedding"] for embed in response.data]
        print("OpenAI embeddings generated:", vecs[:2])
    elif provider == "titan":
        client = boto3.client("bedrock-runtime", region_name="us-east-1")
        # Titan model ID (placeholder)
        model_id = "amazon.titan-text-express-v1"
        responses = []
        for chunk in caption_chunks:
            resp = client.invoke_model(Body=chunk.encode("utf-8"), ModelId=model_id)
            # Titan returns embedding as JSON list of floats under 'embedding'
            embedding = json.loads(resp["Body"].read())["embedding"]
            responses.append(embedding)
        vecs = responses
        print("Titan embeddings generated (first two):", vecs[:2])
    else:
        raise ValueError(f"Unsupported provider: {provider}")
    return vecs


# Example usage (not executed)
# if __name__ == "__main__":
#     chunks = ["Team discussed Q2 roadmap.", "Next sprint goals defined."]
#     asyncio.run(embed_captions(chunks, provider="gemini"))
