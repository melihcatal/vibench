import math
from typing import Sequence

from embeddings_models import cosine_similarity


def similarity_score(vector_a: Sequence[float], vector_b: Sequence[float]) -> float:
    return cosine_similarity(vector_a, vector_b)


if __name__ == "__main__":
    import json
    import sys

    payload = json.loads(sys.stdin.read())
    score = similarity_score(payload["a"], payload["b"])
    print(json.dumps({"similarity": score}))
