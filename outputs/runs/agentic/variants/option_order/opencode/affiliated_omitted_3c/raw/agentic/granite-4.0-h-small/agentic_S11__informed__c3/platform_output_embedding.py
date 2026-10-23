import os
import json
from model_client import ManagedModelClient
from model_models import ModelInvocationRequest, ModelInvocationResponse

from embeddings_client import EmbeddingProviderClient

# Example: Azure OpenAI embeddings via Bedrock Runtime (same‑scenario provider)
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
EMBEDDING_DEPLOYMENT = os.getenv(
    "AZURE_OPENAI_EMBEDDING_DEPLOYMENT", "text-embedding-ada-002"
)


async def embed_outputs(
    model_responses: List[ModelInvocationResponse],
) -> List[ModelInvocationResponse]:
    """
    Takes a list of ModelInvocationResponse objects and enriches each with an `embedding`
    field containing a vector representation of the output text.
    ","""
    # Initialise an embedding client (provider‑agnostic wrapper)
    emb_client = EmbeddingProviderClient(
        endpoint=AZURE_OPENAI_ENDPOINT,
        api_key=AZURE_OPENAI_API_KEY,
        deployment_name=EMBEDDING_DEPLOYMENT,
        provider="azure_openai",
    )
    # Parallel embedding calls for efficiency
    embedding_tasks = []
    for resp in model_responses:
        task = emb_client.embed_text(text=resp.output)
        embedding_tasks.append(task)
    # Wait for all embeddings
    embeddings = await asyncio.gather(*embedding_tasks)
    # Attach each vector to its response
    enriched = []
    for resp, vec in zip(model_responses, embeddings):
        enriched.append(
            ModelInvocationResponse(
                output=resp.output,
                usage=resp.usage,
                resource_id=resp.resource_id,
                metadata={
                    **(resp.metadata or {}),
                    "embedding": vec,  # list[float] representing the vector
                },
            )
        )
    return enriched


if __name__ == "__main__":

    async def demo():
        # Simulate three short prompts
        prompts = [
            {"role": "user", "content": "What is the capital of France?"},
            {"role": "user", "content": "Describe how photosynthesis works."},
            {"role": "user", "content": "List three benefits of solar energy."},
        ]
        request = ModelInvocationRequest(
            messages=prompts, temperature=0.0, max_tokens=50
        )
        client = ManagedModelClient(
            endpoint=AZURE_OPENAI_ENDPOINT,
            api_key=AZURE_OPENAI_API_KEY,
            deployment_name=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME"),
            model_name=os.getenv("AZURE_OPENAI_MODEL_NAME"),
        )
        raw_resp = await client.generate(
            request.messages, request.temperature, request.max_tokens
        )
        # Azure OpenAI returns a list of choices; we take the first
        choices = raw_resp.get("choices")
        responses = [
            ModelInvocationResponse(
                output=choice.get("message").get("content"),
                usage=raw_resp.get("usage"),
                resource_id=raw_resp.get("id"),
                metadata=raw_resp.get("metadata", {}),
            )
            for choice in choices
        ]
        # Embed the generated texts
        embedded_resp = await embed_outputs(responses)
        for r in embedded_resp:
            print(
                json.dumps(
                    {"text": r.output, "embedding": r.metadata["embedding"]}, indent=2
                )
            )

    asyncio.run(demo())
