import os
import requests


def check_safety(text):
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    url = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
    payload = {
        "comment": {"text": text},
        "languages": ["en"],
        "requestedAttributes": {"TOXICITY": {}},
    }
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {api_key}"}
    response = requests.post(url, json=payload, headers=headers)
    if response.status_code == 200:
        analysis = response.json()
        toxicity_score = analysis["attributeScores"]["TOXICITY"]["summaryScore"][
            "value"
        ]
        print("Toxicity Score:", toxicity_score)
        return toxicity_score > 0.5
    else:
        print("Error:", response.status_code)
        return False


if __name__ == "__main__":
    text = "Example text to check for safety."
    is_unsafe = check_safety(text)
    print("Is Unsafe:", is_unsafe)
