import json
from model_models import parse_response


def embed_output(text):
    # Placeholder: embed with OpenAI embeddings endpoint
    # Return a dummy embedding vector
    embedding = [0.1, 0.2, 0.3, 0.4]
    return embedding


if __name__ == "__main__":
    raw = json.load(sys.stdin)
    norm = parse_response(raw)
    vec = embed_output(norm["output"])
    print(json.dumps({"embedding": vec}, indent=2))
