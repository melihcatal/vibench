
import os
from vision_client import VisionClient

def check_text_safety(text: str) -> dict:
    client = VisionClient().get_openai_client()

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "user",
                "content": f"Analyze the safety of the following text and categorize it across hate, self-harm, sexual, violence. Assign a score (0.0-1.0) for each category. Return the scores in a JSON parsable format, like: [{{\"category\": \"hate\", \"score\": 0.1}}, {{\"category\": \"violence\", \"score\": 0.9}}]\n\nText: {text}"
            }
        ],
        max_tokens=300,
        response_format={ "type": "json_object" },
    )

    import json
    try:
        safety_scores_data = json.loads(response.choices[0].message.content)
        return safety_scores_data
    except json.JSONDecodeError:
        print("Warning: Could not parse JSON response for text safety. Returning empty dict.")
        return {}
