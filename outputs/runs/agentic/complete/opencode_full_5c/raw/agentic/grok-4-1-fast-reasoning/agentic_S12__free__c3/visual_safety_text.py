from openai import OpenAI
from vision_models import ImageLabels
from typing import Dict


def visual_safety_text(labels: ImageLabels) -> Dict:
    client = OpenAI()
    text = " ".join(labels.labels)
    response = client.moderations.create(input=text)
    result = response.results[0]
    return {
        "flagged": result.flagged,
        "categories": dict(result.categories),
        "category_scores": dict(result.category_scores),
    }
