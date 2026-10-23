import os
import json
from document_client import get_anthropic_client
from document_models import NormalizedExpense, ValidationResult
from typing import List

def validate_document_fields(expense: NormalizedExpense, required_fields: List[str], min_confidence: float) -> ValidationResult:
    client = get_anthropic_client()
    
    reasons = []
    required_fields_pass = True
    confidence_score_pass = True

    for field in required_fields:
        if getattr(expense, field) is None:
            reasons.append(f"Missing required field: {field}")
            required_fields_pass = False
    
    if expense.confidence_score is None or expense.confidence_score < min_confidence:
        reasons.append(f"Overall confidence score {expense.confidence_score:.2f} is below minimum required {min_confidence:.2f}")
        confidence_score_pass = False

    system_message = """You are an expert document validation system. Your task is to review extracted expense data and identify any potential inconsistencies, errors, or anomalies that might indicate incorrect extraction.
    Focus on logical consistency (e.g., total amount vs. sum of line items, realistic dates/amounts).
    Provide a concise list of observations or potential issues. If everything looks correct, state 'No issues found.'
    Output should be a JSON array of strings, where each string is an observation or issue."""

    user_message = f"""Review the following normalized expense data for consistency and potential errors:
    {expense.model_dump_json(indent=2)}
    """

    try:
        response = client.messages.create(
            model=os.environ.get("ANTHROPIC_VALIDATION_MODEL", "claude-3-haiku-20240307"),
            max_tokens=500,
            messages=[
                {"role": "user", "content": user_message},
                {"role": "assistant", "content": "<result>"}
            ],
        )
        
        llm_validation_output = response.content[0].text.strip()
        if llm_validation_output and llm_validation_output != "No issues found.":
            try:
                llm_issues = json.loads(llm_validation_output)
                if isinstance(llm_issues, list):
                    reasons.extend(llm_issues)
                else:
                    reasons.append(f"LLM observation: {llm_validation_output}")
            except json.JSONDecodeError:
                reasons.append(f"LLM observation: {llm_validation_output}")
        
    except Exception as e:
        reasons.append(f"LLM validation failed: {e}")

    is_valid = required_fields_pass and confidence_score_pass and not reasons
    if "No issues found." in reasons:
        reasons.remove("No issues found.")

    return ValidationResult(
        is_valid=is_valid,
        reasons=reasons,
        confidence_score_pass=confidence_score_pass,
        required_fields_pass=required_fields_pass,
    )