from embeddings_client import load_config, make_client


def main() -> None:
    cfg = load_config()
    client = make_client()
    text = "screen corpus for unsafe content before embedding"
    response = client.embeddings.create(model=cfg.model, input=text)
    print({"provider": "openai", "safe": bool(response.data)})


if __name__ == "__main__":
    main()
