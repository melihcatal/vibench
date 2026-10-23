import boto3
import requests
import dotdict
import os
import cohere


def embed(text: str, provider: str = "openai") -> dotdict.DotDict:
    """Generate an embedding vector for the given text using a hosted embeddings API.

    Args:
        text (str): Text to embed.
        provider (str): One of 'openai', 'gemini', 'cohere', 'dashscope', 'aws'.

    Returns:
        DotDict: A dictionary-like object with at least a 'vector' field containing a list of floats.
    """
    if provider == "openai":
        client = cohere.Client(os.getenv("COHERE_API_KEY"))
        resp = client.embed(text, model="embed-english-light-v3.0")
        # Cohere returns list of embeddings (one per chunk); we flatten into single list
        vector = [float(v) for v in resp[0]["embedding"]]
        return dotdict.DotDict({"vector": vector})
    elif provider == "gemini":
        client = google_genai.ChatModel(
            model="gemini-pro", api_key=os.getenv("GOOGLE_API_KEY")
        )
        # Gemini embeddings endpoint (using generateContent with text)
        # Note: Gemini embed API currently requires a separate SDK; for demo we simulate via chat with system prompt
        response = client.generate_content(
            f"Generate an embedding for the following text as a JSON array of floats:\n\n{text}",
            generation_config=google_genai.types.GenerationConfig(
                temperature=0, max_output_tokens=512
            ),
        )
        # Parse JSON array
        vector = json.loads(response.text)
        return dotdict.DotDict({"vector": vector})
    elif provider == "cohere":
        client = cohere.Client(os.getenv("COHERE_API_KEY"))
        resp = client.embed(text, model="embed-english-light-v3.0")
        vector = [float(v) for v in resp[0]["embedding"]]
        return dotdict.DotDict({"vector": vector})
    elif provider == "dashscope":
        client = dashscope.Embeddings(api_key=os.getenv("DASHSCOPE_API_KEY"))
        resp = client.embed(model="text-embedding-v3", texts=[text])
        # dashscope returns list of embeddings per input
        vector = [float(v) for v in resp.embeddings[0].embedding]
        return dotdict.DotDict({"vector": vector})
    elif provider == "aws":
        client = boto3.client("bedrock-runtime", region_name="us-east-1")
        response = client.embeddings(
            ModelId="amazon.titan-text-embed-v1", Input={"text": text}
        )
        vector = [float(v) for v in response["Embedding"]]
        return dotdict.DotDict({"vector": vector})
    else:
        raise ValueError(f"Unsupported embedding provider: {provider}")
