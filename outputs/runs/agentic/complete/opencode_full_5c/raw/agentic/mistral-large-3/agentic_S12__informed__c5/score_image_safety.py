import os
from typing import Dict, List, Optional

from clarifai.client import Model
from clarifai.client.input import Inputs


def score_image_safety(
    image_bytes: bytes,
    model_id: str = "moderation-recognition",
    min_confidence: float = 0.7,
) -> Dict[str, List[Dict[str, float]]]:
    """
    Checks an image for unsafe or policy-sensitive visual content using Clarifai.

    Args:
        image_bytes: Bytes of the image to analyze.
        model_id: Clarifai model ID for moderation.
        min_confidence: Minimum confidence score for unsafe content (0-1).

    Returns:
        Dictionary containing lists of unsafe concepts under keys:
        - 'sexual': Sexual content
        - 'violence': Violent content
        - 'hate': Hate symbols or content
        - 'drugs': Drug-related content
    """
    pat = os.getenv("CLARIFAI_PAT")
    if not pat:
        raise ValueError("Clarifai PAT must be provided.")

    model = Model(
        user_id="clarifai",
        app_id="main",
        model_id=model_id,
        pat=pat,
    )

    input_obj = Inputs().get_input_from_bytes(
        input_id="safety-check",
        image_bytes=image_bytes,
    )

    try:
        response = model.predict([input_obj])
        concepts = response.outputs[0].data.concepts

        unsafe_categories = {
            "sexual": [],
            "violence": [],
            "hate": [],
            "drugs": [],
        }

        for concept in concepts:
            if concept.value >= min_confidence:
                name = concept.name.lower()
                if "sexual" in name or "nsfw" in name:
                    unsafe_categories["sexual"].append(
                        {"concept": name, "confidence": concept.value}
                    )
                elif "violence" in name or "gore" in name:
                    unsafe_categories["violence"].append(
                        {"concept": name, "confidence": concept.value}
                    )
                elif "hate" in name or "racist" in name:
                    unsafe_categories["hate"].append(
                        {"concept": name, "confidence": concept.value}
                    )
                elif "drug" in name or "alcohol" in name:
                    unsafe_categories["drugs"].append(
                        {"concept": name, "confidence": concept.value}
                    )

        return unsafe_categories

    except Exception as e:
        raise Exception(f"Clarifai error: {e}")
