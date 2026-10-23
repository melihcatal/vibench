import json
from vision_models import NormalizedResponse


def check_safety(labels: List[str]) -> bool:
    # Simple unsafe word filter - replace with provider's policy engine for images
    unsafe_words = {"bomb", "weapon", "drugs", "nudity", "violence", "hate"}
    return not any(word.lower() in unsafe_words for word in labels)


if __name__ == "__main__":
    # Replace with actual labels from `DetectImageLabels.run` or provider response
    sample_labels = ["dog", "cat", "mountain"]
    safe = check_safety(sample_labels)
    print(json.dumps({"safe": safe}, indent=2))
