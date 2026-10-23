# platform_output_embedding.py
# [LATER-STEP]
# Embed platform outputs for evaluation or retrieval

from model_client import ManagedModelClient
from model_models import ModelInvocationResponse, EmbeddingResult


# Example: use a concrete embedding model (e.g., OpenAI text-embedding-ada-002)
def embed_output(invocation: ModelInvocationResponse) -> EmbeddingResult:
    client = ManagedModelClient(provider="openai")
    # Call the embedding endpoint
    embedding_resp = client.embeddings.create(input=invocation.output_text)
    # Build a normalized result object
    return EmbeddingResult(
        embedding=embedding_resp.data[0].embedding,  # list of floats
        model_name=embedding_resp.model,
        usage=embedding_resp.usage,
    )


@dataclass
class EmbeddingResult:
    embedding: List[float]
    model_name: str
    usage: Dict[str, int]  # provider usage dict

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


# Example usage (uncomment to test)
# if __name__ == "__main__":
#     resp = ModelInvocationResponse(run_id="r1", output_text="The sky is blue.", usage=None)
#     emb = embed_output(resp)
#     print(emb.to_dict())
