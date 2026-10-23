import os
from safety_models import SafetyModels
from ibm_watsonx_ai.hlp.content_safety import ModerationProvider
from ibm_watsonx_ai.hlp.response_normalization import ModerationResponseParser


def embed_moderation_reason(reason_text: str) -> dict:
    """Generate embedding of moderation rationale using watsonx.ai embeddings.",
    Returns a dict with embedding vector and metadata.",
    """
    # Setup client with environment variables WATSONX_API_KEY, WATSONX_PROJECT_ID
    provider = ModerationProvider()  # using watsonx guardrails moderate endpoint
    parsed = ModerationResponseParser().parse(reason_text)
    # Use watsonx embedding endpoint (assumed available via same service)
    embedding = client.embeddings.create(
        input=reason_text, model_id="text-embedding-3-large"
    ).result["embeddings"][0]["vector"]
    return {
        "metadata": {
            "provider": "watsonx",
            "model_id": "text-embedding-3-large",
        },
        "embedding": embedding,
        "original_text": reason_text,
    }


if __name__ == "__main__":
    demo = "User provided a clear explanation for why the moderation was incorrect."
    vec = embed_moderation_reason(demo)
    print(vec)
