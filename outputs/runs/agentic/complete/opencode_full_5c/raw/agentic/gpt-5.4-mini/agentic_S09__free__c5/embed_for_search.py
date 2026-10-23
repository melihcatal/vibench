from embeddings_client import load_config, make_client
from embeddings_models import extract_embeddings


def main() -> None:
    cfg = load_config()
    client = make_client()
    query = "best vector search strategy"
    documents = ["vector databases", "cooking recipes", "hybrid retrieval"]
    response = client.embeddings.create(model=cfg.model, input=[query] + documents)
    vectors = extract_embeddings(response)
    print({"query": vectors[0], "documents": vectors[1:]})


if __name__ == "__main__":
    main()
