import os
from googleapiclient import discovery

API_KEY = os.getenv("PERSPECTIVE_API_KEY")


def check_live_caption_safety(text: str):
    if not API_KEY:
        raise ValueError("PERSPECTIVE_API_KEY environment variable not set.")

    client = discovery.build(
        "commentanalyzer",
        "v1alpha1",
        developerKey=API_KEY,
        static_discovery=False,
    )

    analyze_request = {
        "comment": {"text": text},
        "requestedAttributes": {"TOXICITY": {}},
    }

    response = client.comments().analyze(body=analyze_request).execute()

    toxicity_score = response["attributeScores"]["TOXICITY"]["summaryScore"]["value"]

    return {"text": text, "toxicity_score": toxicity_score}


if __name__ == "__main__":
    unsafe_caption = "This is a hateful and abusive comment."
    safety_check = check_live_caption_safety(unsafe_caption)
    print(f"Caption: '{safety_check['text']}'")
    print(f"Toxicity Score: {safety_check['toxicity_score']}")
