import os
from openai import OpenAI


OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")
OPENAI_MODERATION_MODEL = "text-moderation-latest"


def moderate_profile_text(
    text: str,
    fields: dict = None,
) -> dict:
    client = OpenAI(api_key=OPENAI_API_KEY)

    combined_text = text
    if fields:
        field_texts = " ".join(str(v) for v in fields.values())
        combined_text = f"{text} {field_texts}"

    response = client.moderations.create(
        model=OPENAI_MODERATION_MODEL,
        input=combined_text,
    )

    result = response.results[0]
    flagged = result.flagged
    categories = dict(result.categories)
    category_scores = dict(result.category_scores)

    return {
        "flagged": flagged,
        "categories": categories,
        "category_scores": category_scores,
        "safe_for_activation": not flagged,
        "violations": [cat for cat, is_flagged in categories.items() if is_flagged],
    }


def moderate_profile_fields(
    display_name: str = "",
    bio: str = "",
    location: str = "",
    custom_fields: dict = None,
) -> dict:
    fields = {"display_name": display_name, "bio": bio, "location": location}
    if custom_fields:
        fields.update(custom_fields)

    combined_text = " ".join(str(v) for v in fields.values() if v)

    result = moderate_profile_text(text=combined_text, fields=fields)
    result["fields_checked"] = list(fields.keys())
    return result


if __name__ == "__main__":
    sample_bio = "I'm a friendly user looking forward to joining this community!"
    result = moderate_profile_text(text=sample_bio)
    print(f"Text safe: {result['safe_for_activation']}")
    print(f"Flagged: {result['flagged']}")
    if result["violations"]:
        print(f"Violations: {result['violations']}")
