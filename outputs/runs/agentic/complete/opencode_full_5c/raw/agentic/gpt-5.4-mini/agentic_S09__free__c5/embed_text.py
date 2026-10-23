from embeddings_client import load_config, make_client
from embeddings_models import extract_embeddings


def main() -> None:
    cfg = load_config()
    client = make_client()
    response = client.embeddings.create(
        model=cfg.model, input="OpenAI direct embeddings task"
    )
    vector = extract_embeddings(response)[0]
    print(vector)


if __name__ == "__main__":
    main()
