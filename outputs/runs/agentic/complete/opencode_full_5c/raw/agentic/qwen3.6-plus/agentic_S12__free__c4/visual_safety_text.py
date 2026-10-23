import os
from openai import OpenAI
from vision_models import ImageLabel, SafetyScore


def get_moderation_client():
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is required")
    client = OpenAI(
        api_key=api_key,
        base_url="https://api.openai.com/v1",
    )
    return client


def check_text_safety(text: str) -> SafetyScore:
    client = get_moderation_client()
    response = client.moderations.create(
        model="omni-moderation-latest",
        input=text,
    )
    result = response.results[0]
    categories = {}
    flagged = []
    is_safe = not result.flagged
    for cat_name, flagged_value in result.categories.model_dump().items():
        score = result.category_scores.model_dump().get(cat_name, 0.0)
        categories[cat_name] = score
        if flagged_value:
            flagged.append(cat_name)
    overall_score = (
        min(
            (score for score in categories.values()),
            default=0.0,
        )
        if flagged
        else max(
            (score for score in categories.values()),
            default=1.0,
        )
    )
    return SafetyScore(
        is_safe=is_safe,
        categories=categories,
        overall_score=overall_score,
        flagged_categories=flagged,
    )


def check_labels_safety(labels: list[ImageLabel]) -> SafetyScore:
    combined_text = ", ".join(label.name for label in labels)
    return check_text_safety(combined_text)


def check_description_safety(description: str) -> SafetyScore:
    return check_text_safety(description)


if __name__ == "__main__":
    sample_labels = [
        ImageLabel("beach", 0.95, "nature"),
        ImageLabel("ocean", 0.92, "nature"),
    ]
    result = check_labels_safety(sample_labels)
    print(f"Safe: {result.is_safe}")
    print(f"Flagged: {result.flagged_categories}")
