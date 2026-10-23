import json
import sys

from embeddings_models import cosine_similarity


def score_similarity(left: list[float], right: list[float]) -> float:
    return cosine_similarity(left, right)


def main() -> None:
    left = json.loads(sys.argv[1])
    right = json.loads(sys.argv[2])
    print(json.dumps({"similarity": score_similarity(left, right)}))


if __name__ == "__main__":
    main()
