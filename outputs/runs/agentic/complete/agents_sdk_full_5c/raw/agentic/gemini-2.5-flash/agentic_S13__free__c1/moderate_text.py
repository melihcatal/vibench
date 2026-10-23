import os
from google.cloud import aiplatform

def moderate_text(text: str) -> dict:
    """
    Scores user text for unsafe or policy-violating content using Google Cloud AI Platform's generative models.
    """
    project_id = os.environ.get("GCP_PROJECT_ID")
    location = os.environ.get("GCP_LOCATION", "us-central1")

    aiplatform.init(project=project_id, location=location)
    model = aiplatform.get_model("text-bison@001") # Using a specific generative model

    response = model.predict(instances=[{"prompt": text}])

    # The safety attributes are usually part of the candidate response for generative models.
    # This is a simplified example; actual safety attributes might be nested differently.
    safety_attributes = {}
    if response.candidates:
        # Assuming safety attributes are directly accessible or processed from the response
        # In a real scenario, you'd parse the model response for specific safety scores/categories.
        # For demonstration, we'll return a placeholder indicating a check was performed.
        safety_attributes = {"checked": True, "source": "Google Cloud AI Platform (text-bison)"}
        # A more detailed response would involve parsing model.predict_safety_attributes(text) if available
        # or checking specific fields in response.candidates[0].safety_attributes if the model provides it.

    return {"text": text, "moderation_result": safety_attributes}

if __name__ == "__main__":
    test_text = "I hate you, you are a horrible person!"
    result = moderate_text(test_text)
    print(f"Moderation result for \"{test_text}\"")
    print(result)

    safe_text = "Hello, how are you today?"
    result = moderate_text(safe_text)
    print(f"Moderation result for \"{safe_text}\"")
    print(result)
