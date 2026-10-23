import os


class VisionModels:
    # Pass-through model identifiers for same-scenario steps
    # In production these would be replaced with concrete provider IDs (e.g., model: 'google-vision-annotate')
    MODEL_MAP = {
        "detect_image_labels": "google-vision-label",
        "describe_image": "google-vision-describe",
        "detect_image_text": "google-vision-ocr",
        "score_image_safety": "google-vision-safety",
    }

    @staticmethod
    def get_model_name(step_name: str) -> str:
        """Resolve a step name to its concrete model identifier."""
        return VisionModels.MODEL_MAP.get(step_name, "unknown-model")

    @staticmethod
    def normalize_response(raw_response: dict, step_name: str) -> dict:
        """Normalize responses from provider-specific schema to a unified internal shape."""
        if step_name == "detect_image_labels":
            # Expected: list of {description}, keep as is
            return {"labels": raw_response.get("labelAnnotations", [])}
        elif step_name in ["describe_image", "detect_image_text"]:
            # OCR/text returns a big string; split into lines
            text = raw_response.get("text", "")
            return {
                "text_lines": [
                    line.strip() for line in text.split("\n") if line.strip()
                ]
            }
        elif step_name == "score_image_safety":
            # SafeSearch response map to generic safety keys: adult, violent, medical, racy
            safe = raw_response.get("safeSearchAnnotation", {})
            return {
                "adult": safe.get("adult", "NONE"),
                "violent": safe.get("violent", "NONE"),
                "medical": safe.get("medical", "NONE"),
                "racy": safe.get("racy", "NONE"),
            }
        else:
            raise ValueError(f"Unrecognized step: {step_name}")
