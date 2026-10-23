import os
from google.cloud import aiplatform

def moderate_batch(texts: list[str]) -> list[dict]:
    """
    Moderates a batch of user messages and returns per-message decisions
    using Google Cloud AI Platform's generative models.
    """
    project_id = os.environ.get("GCP_PROJECT_ID")
    location = os.environ.get("GCP_LOCATION", "us-central1")

    aiplatform.init(project=project_id, location=location)
    model = aiplatform.get_model("text-bison@001") # Using a specific generative model

    results = []
    for text in texts:
        response = model.predict(instances=[{"prompt": text}])
        safety_attributes = {}
        if response.candidates:
            safety_attributes = {"checked": True, "source": "Google Cloud AI Platform (text-bison)"}
        results.append({"text": text, "moderation_result": safety_attributes})

    return results

if __name__ == "__main__":
    test_texts = [
        "This is a perfectly safe message.",
        "I will destroy you and everything you love!",
        "Let's discuss the weather.",
        "You are so stupid, I can't believe it."
    ]
    batch_results = moderate_batch(test_texts)
    for result in batch_results:
        print(f"Batch moderation result for \"{result['text']}\"")
        print(result)
