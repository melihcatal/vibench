
from google.cloud import aiplatform
from google.protobuf import json_format
import os
from document_client import GoogleVertexAIManager
from document_models import ExpenseRecord

def moderate_vendor_notes(expense_record: ExpenseRecord) -> dict:
    """
    Moderates vendor notes or memo fields using Google Cloud Vertex AI's safety attributes.
    """
    project_id = os.getenv("GCP_PROJECT_ID")
    location = os.getenv("GCP_LOCATION", "us-central1")

    if not project_id:
        raise ValueError("GCP_PROJECT_ID environment variable not set.")
    if not expense_record.notes:
        return {"safety_attributes": {"moderation_skipped": True, "reason": "No notes to moderate."}}

    vertex_manager = GoogleVertexAIManager(project_id, location)
    prediction_client = vertex_manager.get_prediction_client()

    # The model used for safety attributes is typically a foundational model capable of text analysis.
    # For safety, we can use a generative model and examine its safety output.
    # Using `gemini-pro` for text generation and safety attributes.
    model_id = "gemini-pro"
    endpoint = (
        f"projects/{project_id}/locations/{location}/publishers/google/models/{model_id}"
    )

    # For safety, we call the model with the text and inspect the safety ratings in the response.
    # The actual prompt here is less important than the model's inherent safety detection.
    # We are essentially asking the model to process the text, and its response will include safety attributes.
    # Note: Direct safety API for arbitrary text (not as part of a generation) might be different,
    # but using a generative model and checking its safety attributes is a common pattern.
    input_content = expense_record.notes

    # For Gemini, the request structure for text input in `generate_content` is different.
    # We will use the `predict` method of the client, assuming a text generation model.
    # This might require the raw API structure.
    # A more direct approach for text safety without generation might involve a different API or model.
    # For simplicity, we'll try to use a generic text model and look for safety attributes in the response.

    # Gemini API uses `GenerateContentRequest` not `predict` for this.
    # Let's adjust for Vertex AI SDK for generative models, which has a specific way for safety.
    # The aiplatform library has `GenerativeModel` for this.

    try:
        model = aiplatform.preview.generative_models.GenerativeModel(model_id=model_id)
        response = model.generate_content(
            input_content,
            safety_settings=[], # Empty to get raw safety scores if model supports it without blocking
            # The safety settings would typically be used to block unsafe content.
            # Here we want to retrieve the scores *of* the content.
        )

        safety_data = {}
        if response.prompt_feedback and response.prompt_feedback.safety_ratings:
            safety_data["prompt_safety_ratings"] = [
                {"category": rating.category.name, "probability": rating.probability.name}
                for rating in response.prompt_feedback.safety_ratings
            ]
        
        # If there's a generated candidate, check its safety too (though not relevant for mere moderation of input)
        if response.candidates:
            first_candidate = response.candidates[0]
            if first_candidate.safety_ratings:
                 safety_data["candidate_safety_ratings"] = [
                    {"category": rating.category.name, "probability": rating.probability.name}
                    for rating in first_candidate.safety_ratings
                ]

        return {"safety_attributes": safety_data}

    except Exception as e:
        print(f"Error moderating text with Vertex AI Gemini: {e}")
        return {"safety_attributes": {"moderation_failed": True, "error": str(e)}}

if __name__ == '__main__':
    # Example usage
    expense_with_notes = ExpenseRecord(
        document_type="invoice",
        vendor_name="Contoso Ltd",
        transaction_date="2023-01-01",
        total_amount=100.0,
        notes="This is a perfectly normal note about the invoice.",
        line_items=[]
    )

    expense_with_potentially_unsafe_notes = ExpenseRecord(
        document_type="invoice",
        vendor_name="Bad Co.",
        transaction_date="2023-01-02",
        total_amount=200.0,
        notes="I hate this vendor and their terrible service!", # Example of negative sentiment
        line_items=[]
    )

    # Ensure GCP_PROJECT_ID and GCP_LOCATION are set as environment variables
    # print("Moderating safe notes:")
    # print(moderate_vendor_notes(expense_with_notes))

    # print("
Moderating potentially unsafe notes:")
    # print(moderate_vendor_notes(expense_with_potentially_unsafe_notes))
    pass
