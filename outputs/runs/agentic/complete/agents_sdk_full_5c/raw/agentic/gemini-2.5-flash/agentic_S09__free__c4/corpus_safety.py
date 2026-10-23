import os
from google.cloud import aiplatform
from typing import List, Dict, Any

def check_text_for_safety(
    project_id: str, 
    location: str, 
    text_content: str
) -> Dict[str, Any]:
    """
    Checks a given text for safety using Google Cloud Vertex AI Generative AI safety features.
    This uses the 'gemini-pro' model for content moderation, which integrates safety attributes.
    """
    aiplatform.init(project=project_id, location=location)

    # Using a generative model with built-in safety filters
    # The `gemini-pro` model can be used for content analysis and safety checks.
    # It returns safety attributes in the response.
    model = aiplatform.get_model_registry().get_model_version("gemini-pro").model

    safety_check_prompt = (
        "Analyze the following text for potential harmful content (hate speech, sexual content, "
        "violence, harassment, dangerous content). Just respond with 'SAFE' or 'UNSAFE' "
        "and if unsafe, briefly state why, without repeating the text. "
        "Strictly adhere to this format: 'SAFE' or 'UNSAFE: [reason]'.\n\n"
        f"Text: """{text_content}""""
    )

    response = model.predict(
        instances=[{"prompt": safety_check_prompt}],
        parameters={
            "temperature": 0.0,
            "max_output_tokens": 100,
            "top_p": 0.8,
            "top_k": 40
        }
    )
    
    safety_results = {"decision": "UNKNOWN", "reasons": []}
    
    if response and response.predictions:
        # Check the safety attributes provided by the model itself
        # This is where the actual Vertex AI safety signal comes from, not just the prompt output.
        # The structure can vary, but generally, it's in the 'safety_attributes' or similar.
        # For gemini-pro, safety ratings are part of the 'candidates' structure.
        
        # Access safety ratings from the candidate (generated content)
        if response.candidates and hasattr(response.candidates[0], 'safety_ratings'):
            for rating in response.candidates[0].safety_ratings:
                category = rating.category.name.replace("HARM_CATEGORY_", "")
                if rating.probability_score >= 0.8 or rating.severity_score >= 0.8: # High probability/severity
                    safety_results["decision"] = "UNSAFE"
                    safety_results["reasons"].append(f"High risk in category: {category} (Probability: {rating.probability_score:.2f}, Severity: {rating.severity_score:.2f})")
        
        # Also check the direct text output from the prompt, as a secondary signal
        generated_text = response.predictions[0].get('content', '').strip() if response.predictions[0] else ''
        if "UNSAFE" in generated_text.upper():
            safety_results["decision"] = "UNSAFE"
            if "reasons" not in safety_results or not safety_results["reasons"]:
                safety_results["reasons"].append(f"Model output indicated unsafety: {generated_text}")
        elif "SAFE" in generated_text.upper() and safety_results["decision"] == "UNKNOWN":
            safety_results["decision"] = "SAFE"
            safety_results["reasons"].append("Model output indicated safety.")

    if not safety_results["reasons"] and safety_results["decision"] == "UNKNOWN":
        safety_results["decision"] = "SAFE" # Default to safe if no specific unsafe signal and no direct model output indicated unsafety.
        safety_results["reasons"].append("No explicit safety concerns detected by the model's safety attributes or direct output.")
            
    return safety_results

if __name__ == "__main__":
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    location = os.environ.get("GOOGLE_CLOUD_LOCATION", "us-central1")

    if not project_id:
        print("Please set the GOOGLE_CLOUD_PROJECT environment variable.")
    else:
        safe_text = "This is a perfectly normal sentence about cloud computing."
        unsafe_text_violence = "I will hit them with a baseball bat."
        unsafe_text_hate = "I hate all people from that group."

        print(f"Checking safety for: '{safe_text}'")
        safe_result = check_text_for_safety(project_id, location, safe_text)
        print(f"Safety Result: {safe_result}\n")

        print(f"Checking safety for: '{unsafe_text_violence}'")
        violence_result = check_text_for_safety(project_id, location, unsafe_text_violence)
        print(f"Safety Result: {violence_result}\n")

        print(f"Checking safety for: '{unsafe_text_hate}'")
        hate_result = check_text_for_safety(project_id, location, unsafe_text_hate)
        print(f"Safety Result: {hate_result}\n")