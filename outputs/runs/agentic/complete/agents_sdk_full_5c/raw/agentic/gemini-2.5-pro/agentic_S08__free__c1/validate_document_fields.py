import json
from document_client import get_openai_client
from document_models import ValidationResult, NormalizedExpense


def validate_document_fields(expense: NormalizedExpense) -> ValidationResult:
    """
    Validates normalized expense fields using OpenAI's GPT model as a rules engine.
    """
    client = get_openai_client()
    expense_json = expense.model_dump_json(indent=2)

    prompt = f"""
    You are a data validation engine. Given the following JSON object representing an
    expense, please validate it against these rules:
    1. The 'vendor' field must not be null or empty.
    2. The 'transaction_date' must be a valid date.
    3. The 'total' must be a positive number greater than zero.
    4. The 'currency' field must be a valid 3-letter ISO currency code (e.g., "USD").
    5. 'line_items', if present, must be a list.

    Here is the expense object:
    {expense_json}

    Return a JSON object with two keys:
    - "is_valid": a boolean indicating if all rules passed.
    - "errors": a list of strings, where each string describes a validation rule that failed.
               If validation is successful, return an empty list.

    Respond with only the validation JSON object, without any additional explanation.
    """

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a data validation assistant that only responds in JSON."},
            {"role": "user", "content": prompt}
        ],
        response_format={"type": "json_object"},
        temperature=0.0,
    )

    try:
        validation_output = json.loads(response.choices[0].message.content)
        return ValidationResult(**validation_output)
    except (json.JSONDecodeError, TypeError):
        return ValidationResult(
            is_valid=False,
            errors=["Failed to parse validation response from the AI model."]
        )
