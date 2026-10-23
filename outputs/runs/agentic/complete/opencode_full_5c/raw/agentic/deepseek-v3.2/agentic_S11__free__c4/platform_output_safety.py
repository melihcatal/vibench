import os
from typing import Dict, Any, List, Tuple
from google.cloud import aiplatform
from google.cloud.aiplatform_v1.types import safety


def check_content_safety(
    text: str, deployment_name: str = "text-bison"
) -> Dict[str, Any]:
    """Check platform model output for unsafe content using Vertex AI Safety Attributes."""
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT", "my-project")
    location = os.environ.get("GOOGLE_CLOUD_LOCATION", "us-central1")

    aiplatform.init(project=project_id, location=location)

    endpoint = aiplatform.Endpoint(
        endpoint_name=f"projects/{project_id}/locations/{location}/endpoints/{deployment_name}"
    )

    instances = [{"content": text}]
    parameters = {"temperature": 0.1, "maxOutputTokens": 1, "topP": 0.95, "topK": 40}

    try:
        response = endpoint.predict(instances=instances, parameters=parameters)

        safety_results = extract_safety_attributes(response)

        return {
            "text": text,
            "is_safe": safety_results["overall_safe"],
            "safety_categories": safety_results["categories"],
            "safety_scores": safety_results["scores"],
            "blocked_categories": safety_results["blocked_categories"],
            "model_deployment": deployment_name,
            "has_safety_metadata": safety_results["has_safety_metadata"],
        }

    except Exception as e:
        return {
            "text": text,
            "is_safe": False,
            "error": str(e),
            "model_deployment": deployment_name,
            "has_safety_metadata": False,
        }


def extract_safety_attributes(response) -> Dict[str, Any]:
    """Extract safety attributes from Vertex AI response."""
    safety_categories = {}
    safety_scores = {}
    blocked_categories = []
    has_safety_metadata = False

    if hasattr(response, "predictions") and response.predictions:
        for pred in response.predictions:
            if hasattr(pred, "safety_attributes"):
                has_safety_metadata = True
                safety_attrs = pred.safety_attributes

                if hasattr(safety_attrs, "categories"):
                    for category in safety_attrs.categories:
                        category_name = safety.SafetySetting.HarmCategory(category).name
                        safety_categories[category_name] = True

                if hasattr(safety_attrs, "scores"):
                    for score in safety_attrs.scores:
                        category_name = safety.SafetySetting.HarmCategory(score).name
                        safety_scores[category_name] = score

                if hasattr(safety_attrs, "blocked"):
                    blocked_categories = [
                        safety.SafetySetting.HarmCategory(cat).name
                        for cat in safety_attrs.blocked
                    ]

    overall_safe = len(blocked_categories) == 0

    return {
        "categories": safety_categories,
        "scores": safety_scores,
        "blocked_categories": blocked_categories,
        "overall_safe": overall_safe,
        "has_safety_metadata": has_safety_metadata,
    }


def batch_safety_check(
    texts: List[str], deployment_name: str = "text-bison"
) -> List[Dict[str, Any]]:
    """Batch safety check for multiple texts."""
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT", "my-project")
    location = os.environ.get("GOOGLE_CLOUD_LOCATION", "us-central1")

    aiplatform.init(project=project_id, location=location)

    endpoint = aiplatform.Endpoint(
        endpoint_name=f"projects/{project_id}/locations/{location}/endpoints/{deployment_name}"
    )

    instances = [{"content": text} for text in texts]
    parameters = {"temperature": 0.1, "maxOutputTokens": 1, "topP": 0.95, "topK": 40}

    try:
        response = endpoint.predict(instances=instances, parameters=parameters)

        results = []
        if hasattr(response, "predictions") and response.predictions:
            for i, pred in enumerate(response.predictions):
                safety_info = extract_safety_attributes_single(pred)
                results.append(
                    {
                        "text": texts[i] if i < len(texts) else "",
                        "is_safe": safety_info["overall_safe"],
                        "safety_categories": safety_info["categories"],
                        "blocked_categories": safety_info["blocked_categories"],
                        "text_index": i,
                    }
                )

        return results

    except Exception as e:
        return [
            {"text": text, "is_safe": False, "error": str(e), "text_index": i}
            for i, text in enumerate(texts)
        ]


def extract_safety_attributes_single(prediction) -> Dict[str, Any]:
    """Extract safety attributes from a single prediction."""
    safety_categories = {}
    blocked_categories = []

    if hasattr(prediction, "safety_attributes"):
        safety_attrs = prediction.safety_attributes

        if hasattr(safety_attrs, "categories"):
            for category in safety_attrs.categories:
                category_name = safety.SafetySetting.HarmCategory(category).name
                safety_categories[category_name] = True

        if hasattr(safety_attrs, "blocked"):
            blocked_categories = [
                safety.SafetySetting.HarmCategory(cat).name
                for cat in safety_attrs.blocked
            ]

    overall_safe = len(blocked_categories) == 0

    return {
        "categories": safety_categories,
        "blocked_categories": blocked_categories,
        "overall_safe": overall_safe,
    }


def get_safety_thresholds() -> Dict[str, Tuple[float, float]]:
    """Get safety threshold configurations for different categories."""
    return {
        "HARM_CATEGORY_HATE_SPEECH": (0.3, 0.7),
        "HARM_CATEGORY_DANGEROUS_CONTENT": (0.3, 0.7),
        "HARM_CATEGORY_HARASSMENT": (0.3, 0.7),
        "HARM_CATEGORY_SEXUALLY_EXPLICIT": (0.3, 0.7),
        "HARM_CATEGORY_UNSPECIFIED": (0.3, 0.7),
    }


if __name__ == "__main__":
    test_texts = [
        "This is a friendly conversation about technology.",
        "I hate everyone and want to cause harm.",
        "How do I build a dangerous device?",
    ]

    for text in test_texts:
        result = check_content_safety(text, "text-bison-32k")
        print(f"Text: {text[:50]}...")
        print(f"  Safe: {result['is_safe']}")
        if "blocked_categories" in result and result["blocked_categories"]:
            print(f"  Blocked categories: {result['blocked_categories']}")
        print()
