from embeddings_client import load_config, make_client


def main() -> None:
    cfg = load_config()
    client = make_client()
    query = "traduce esta consulta para búsqueda semántica"
    response = client.embeddings.create(model=cfg.model, input=query)
    print(
        {"provider": "openai", "translated_query_embedding": response.data[0].embedding}
    )


if __name__ == "__main__":
    main()
