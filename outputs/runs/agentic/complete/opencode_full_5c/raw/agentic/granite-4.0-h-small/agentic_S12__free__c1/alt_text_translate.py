import json
# Placeholder for translation logic - in real usage you would call a translation service
# e.g., Google Cloud Translation API, AWS Translate, etc.


def translate(description: str, target_lang: str = "es") -> str:
    # Simulated translation for demonstration
    translation_map = {
        "cat": "gato",
        "dog": "perro",
        "tree": "árbol",
    }
    words = description.split()
    translated = [translation_map.get(w.lower(), w) for w in words]
    return " ".join(translated)


if __name__ == "__main__":
    # Example usage: replace with real description from vision pipeline
    description = "A cat sitting under a tree."
    translated = translate(description, target_lang="fr")
    print(json.dumps({"translated": translated}, indent=2))
# Integration tip: feed `description` from `DescribeImage.run` result into `translate`
