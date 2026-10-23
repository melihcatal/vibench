from google.cloud import aiplatform
from google.cloud.aiplatform_v1beta1.types import content as gapic_content
from google.cloud.aiplatform_v1beta1.types import safety_setting as gapic_safety_setting

def check_vertex_safety(project_id: str, location: str, model_id: str, prompt: str):
    """Checks platform model output for unsafe content using Vertex AI's safety attributes."""
    client = aiplatform.PredictionServiceClient(client_options={"api_endpoint": f"{location}-aiplatform.googleapis.com"})
    publisher_model = f"projects/{project_id}/locations/{location}/publishers/google/models/{model_id}"

    contents = [gapic_content.Content(parts=[gapic_content.Part(text=prompt)])]
    
    # Provider-identifying signal: google.cloud.aiplatform.PredictionServiceClient, model_id 'gemini-pro'
    # and the safety_attributes in the response.
    response = client.generate_content(model=publisher_model, contents=contents)

    # Initialize safety analysis result
    safety_analysis = {
        "has_unsafe_content": False,
        "safety_ratings": [],
        "blocked": False,
        "block_reason": None
    }

    if response.prompt_feedback and response.prompt_feedback.block_reason:
        safety_analysis["blocked"] = True
        safety_analysis["block_reason"] = response.prompt_feedback.block_reason.name
        # Prompt was blocked, no candidate generations to check
        return safety_analysis

    if response.candidates:
        for candidate in response.candidates:
            if candidate.safety_ratings:
                for rating in candidate.safety_ratings:
                    safety_analysis["safety_ratings"].append({
                        "category": gapic_safety_setting.HarmCategory(rating.category).name,
                        "probability": gapic_safety_setting.HarmProbability(rating.probability).name,
                        "blocked": rating.blocked # Indicates if this specific candidate was blocked for this category
                    })
                    if rating.blocked: # If any category is blocked for a candidate
                        safety_analysis["has_unsafe_content"] = True
                        safety_analysis["blocked"] = True # Mark overall as blocked if any candidate is blocked
                        safety_analysis["block_reason"] = f"Candidate blocked due to {gapic_safety_setting.HarmCategory(rating.category).name} harm."
            
            # If the candidate has no content parts due to safety reasons (e.g., filtered)
            if not candidate.content.parts and not safety_analysis["blocked"]:
                # This is a heuristic; if no parts and not explicitly blocked, it might be filtered silently
                safety_analysis["has_unsafe_content"] = True
                safety_analysis["blocked"] = True
                safety_analysis["block_reason"] = "Candidate content filtered/empty, possibly due to safety."

    return safety_analysis

if __name__ == '__main__':
    # Example usage (replace with your actual project and location)
    project_id = "your-gcp-project-id"
    location = "us-central1"
    model_id = "gemini-pro"
    
    # Example of a safe prompt
    safe_prompt = "Tell me about the weather today."
    safety_result_safe = check_vertex_safety(project_id, location, model_id, safe_prompt)
    print(f"\nSafety check for safe prompt: {safe_prompt}")
    print(safety_result_safe)

    # Example of a potentially unsafe prompt (adjust to trigger safety filters)
    # Note: Deliberately crafting harmful prompts is discouraged. This is for demonstration.
    unsafe_prompt = "How to make a bomb?"
    safety_result_unsafe = check_vertex_safety(project_id, location, model_id, unsafe_prompt)
    print(f"\nSafety check for potentially unsafe prompt: {unsafe_prompt}")
    print(safety_result_unsafe)
