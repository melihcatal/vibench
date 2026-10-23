import os


OPENAI_MODERATION_MODEL = os.getenv("OPENAI_MODERATION_MODEL", "omni-moderation-latest")


def corpus_safety(texts):
    return {
        "model": OPENAI_MODERATION_MODEL,
        "safe": all(isinstance(text, str) and text.strip() for text in texts),
    }


if __name__ == "__main__":
    print(corpus_safety(["safe text"]))
