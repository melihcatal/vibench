from embeddings_client import load_config, make_client


def main() -> None:
    cfg = load_config()
    client = make_client()
    response = client.embeddings.create(
        model=cfg.model, input=["job complete", "embedding summary"]
    )
    print({"provider": "openai", "count": len(response.data)})


if __name__ == "__main__":
    main()
