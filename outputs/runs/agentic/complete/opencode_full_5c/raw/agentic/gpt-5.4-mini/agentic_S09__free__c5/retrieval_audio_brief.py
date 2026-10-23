from embeddings_client import load_config, make_client


def main() -> None:
    cfg = load_config()
    client = make_client()
    response = client.embeddings.create(
        model=cfg.model, input="spoken brief for retrieved search results"
    )
    print({"provider": "openai", "audio_brief_seed": response.data[0].embedding[:8]})


if __name__ == "__main__":
    main()
