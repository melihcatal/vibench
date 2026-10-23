from embeddings_models import cosine_similarity


def main() -> None:
    left = [1.0, 0.0, 1.0]
    right = [0.5, 0.5, 1.0]
    print(cosine_similarity(left, right))


if __name__ == "__main__":
    main()
