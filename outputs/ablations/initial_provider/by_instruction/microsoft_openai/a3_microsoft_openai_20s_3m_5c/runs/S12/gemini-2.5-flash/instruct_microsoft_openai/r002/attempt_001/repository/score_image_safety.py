
import os
from vision_client import VisionClient
from vision_models import ImageAnalysisRequest, ImageSafetyResponse, SafetyScore

def score_image_safety(request: ImageAnalysisRequest) -> ImageSafetyResponse:
    client = VisionClient().get_openai_client()

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "Analyze the safety of this image across categories like hate, self-harm, sexual, violence. Assign a score (0.0-1.0) for each category. Return the scores in a JSON parsable format, like: [{"category": "hate", "score": 0.1}, {"category": "violence", "score": 0.9}]"},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": request.image_url,
                        },
                    },
                ],
            }
        ],
        max_tokens=300,
        response_format={ "type": "json_object" },
    )

    import json
    try:
        safety_scores_data = json.loads(response.choices[0].message.content)
        safety_scores = []
        for item in safety_scores_data.get("safety_scores", []): # Assuming the JSON output has a 'safety_scores' key
            safety_scores.append(SafetyScore(category=item["category"], score=item["score"]))
    except (json.JSONDecodeError, KeyError):
        print("Warning: Could not parse JSON response for image safety. Returning empty scores.")
        safety_scores = []

    return ImageSafetyResponse(safety_scores=safety_scores)
