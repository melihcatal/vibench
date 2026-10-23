from typing import Dict, Any
from vertexai.preview.language_models import TextGenerationModel
from vertexai.preview.language_models import HarmCategory, HarmSeverity

from model_client import get_palm_model

def check_text_safety(text: str) -> Dict[str, Any]:
    model = get_palm_model()
    # Using a simple prompt to get a response that includes safety attributes
    # In a real scenario, you'd likely check the *actual* generation prompt/response.
    # For demonstration, we'll just run a prediction to get safety info.
    response = model.predict(
        text,
        temperature=0.0,
        max_output_tokens=1,
    )

    safety_attributes = {
        "categories": [],
        "scores": [],
        "blocked": False
    }

    if response.safety_attributes:
        safety_attributes["categories"] = response.safety_attributes.categories
        safety_attributes["scores"] = response.safety_attributes.scores
        if response.safety_attributes.blocked:
            safety_attributes["blocked"] = True

    return safety_attributes

def check_prompt_and_output_safety(prompt: str, generated_output: str) -> Dict[str, Any]:
    # In a more complete system, you'd check both independently or during generation.
    # For this example, we'll run a check on the generated_output as it's typically what needs guarding.
    # Vertex AI's TextGenerationModel implicitly checks prompt safety during predict calls.
    return check_text_safety(generated_output)
