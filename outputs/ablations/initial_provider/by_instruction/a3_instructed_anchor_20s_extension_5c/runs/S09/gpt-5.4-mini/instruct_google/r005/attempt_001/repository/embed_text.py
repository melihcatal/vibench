from embeddings_client import embed_query
from embeddings_models import vector_from_response


def embed_text(text, model=None):
    response = embed_query(text, model=model)
    return vector_from_response(response)


if __name__ == "__main__":
    import sys

    print(embed_text(sys.argv[1] if len(sys.argv) > 1 else ""))
