from observability_client import get_generative_model_client, configure_generative_model
import google.generativeai as genai
import os

def check_annotation_safety(annotation_text: str, api_key: str, model_name: str = "gemini-pro") -> dict:
    configure_generative_model(api_key)
    model = get_generative_model_client(model_name)

    # Use safety settings to check for unsafe content
    # The generative model itself provides safety attributes in its response.
    # We'll formulate a query and check the response's prompt_feedback.
    # Note: Direct safety classification without content generation often involves specific safety APIs or careful prompt engineering.
    # For this task, we'll rely on the built-in safety features during a dummy generation attempt.

    response = model.generate_content(
        annotation_text,
        safety_settings={
            genai.types.HarmCategory.HARM_CATEGORY_HARASSMENT: genai.types.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
            genai.types.HarmCategory.HARM_CATEGORY_HATE_SPEECH: genai.types.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
            genai.types.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: genai.types.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
            genai.types.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: genai.types.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
        }
    )

    # The safety attributes are usually on the response object, even if no text is generated due to blocking.
    # If the response is blocked, response.text might be empty.
    # We'll check response.prompt_feedback.safety_ratings

    safety_verdict = {"is_safe": True, "categories": []}
    if response._chunks and response._chunks[0].safety_ratings:
        for rating in response._chunks[0].safety_ratings:
            if rating.probability > genai.types.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE:
                safety_verdict["is_safe"] = False
                safety_verdict["categories"].append({"category": rating.category.name, "probability": rating.probability.name})
    elif not response._chunks:
        # If no chunks, it might be due to blocking before content generation
        # In current genai library, if content is blocked, prompt_feedback contains the info.
        if response.prompt_feedback and response.prompt_feedback.safety_ratings:
            for rating in response.prompt_feedback.safety_ratings:
                if rating.blocked: # Check if the content was blocked for this category
                    safety_verdict["is_safe"] = False
                    safety_verdict["categories"].append({"category": rating.category.name, "probability": rating.probability.name, "blocked": rating.blocked})


    return safety_verdict
