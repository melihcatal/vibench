import os
import json
from typing import Dict, Any
from document_models import NormalizedExpense, ValidationResult, DocumentValidation
from document_client import get_vertex_ai_model
from vertexai.generative_models import GenerationConfig

def validate_document_fields(
    normalized_expense: NormalizedExpense, confidence_scores: Dict[str, float], config: dict = None
) -> DocumentValidation:
    config = config or {}
    project_id = config.get("project_id", os.environ.get("GOOGLE_CLOUD_PROJECT"))
    location = config.get("location", "us-central1")

    if not project_id:
        raise ValueError("Google Cloud project_id must be provided.")

    model = get_vertex_ai_model(project_id, location, "gemini-1.5-flash-001")

    validation_rules = [
        ("vendor_name", normalized_expense.vendor_name is not None, "Vendor name is missing.", 0.7),
        ("transaction_date", normalized_expense.transaction_date is not None, "Transaction date is missing.", 0.8),
        ("total_amount", normalized_expense.total_amount is not None and normalized_expense.total_amount > 0, "Total amount is missing or invalid.", 0.85),
        # Add more rules as needed
    ]

    validation_results = []
    overall_valid = True

    for field_name, condition, reason, min_confidence in validation_rules:
        is_valid = condition
        if confidence_scores.get(field_name, 0.0) < min_confidence:
            is_valid = False
            reason += f" (Confidence too low: {confidence_scores.get(field_name, 0.0):.2f} < {min_confidence:.2f})"
        
        validation_results.append(ValidationResult(field_name=field_name, is_valid=is_valid, reason=reason))
        if not is_valid:
            overall_valid = False

    # Use LLM for more complex, contextual validation if necessary
    # For this example, we will just pass the structured validation through
    # The LLM can be prompted to review the validation_results and add more insights
    prompt_text = f"Review the following normalized expense data and validation results. Provide an overall assessment and any additional insights, especially for fields marked as invalid. \nNormalized Expense: {normalized_expense.dict()}\nValidation Results: {json.dumps([vr.dict() for vr in validation_results])}"
    
    # Simulating LLM response to confirm validation or add more context
    # In a real scenario, the LLM would analyze the prompt_text and return a more nuanced response.
    # For now, we are using the structured rules as the primary validation.
    # If the LLM were to override, its output would be parsed and used here.
    
    # This part can be uncommented and used if we want the LLM to actively validate
    # response = model.generate_content(
    #     [prompt_text],
    #     generation_config=GenerationConfig(temperature=0.1)
    # )
    # print(f"LLM Validation Insights: {response.text}") # For debugging

    return DocumentValidation(
        overall_valid=overall_valid,
        validation_results=validation_results,
        confidence_scores=confidence_scores
    )
