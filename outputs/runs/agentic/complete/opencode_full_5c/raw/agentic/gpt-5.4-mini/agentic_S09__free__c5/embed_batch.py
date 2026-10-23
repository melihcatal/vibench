from embeddings_client import load_config, make_client
from embeddings_models import batch_results, extract_embeddings


def main() -> None:
    cfg = load_config()
    client = make_client()
    texts = ["semantic search", "retrieval ranking", "document clustering"]
    response = client.embeddings.create(model=cfg.model, input=texts)
    results = batch_results(texts, extract_embeddings(response))
    print([item.vector for item in results])


if __name__ == "__main__":
    main()
