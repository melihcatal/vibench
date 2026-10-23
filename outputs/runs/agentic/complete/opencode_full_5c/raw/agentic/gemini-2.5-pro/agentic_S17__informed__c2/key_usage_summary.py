import os
from openai import OpenAI
from security_models import SummaryRequest


def generate_key_usage_summary(request: SummaryRequest) -> str:
    """
    Generates a human-readable summary of key usage from audit notes.

    Args:
        request: A SummaryRequest object containing the audit notes and model.

    Returns:
        A string containing the summary.
    """
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set.")

    client = OpenAI(api_key=api_key)

    prompt = f"""
    Based on the following crypto audit notes, please provide a concise summary
    of key usage and any potential security observations.

    Audit Notes:
    {request.audit_notes}

    Summary:
    """

    try:
        response = client.chat.completions.create(
            model=request.model,
            messages=[
                {"role": "system", "content": "You are a security analyst assistant."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.5,
            max_tokens=250,
        )
        if response.choices:
            return response.choices[0].message.content.strip()
        return "Could not generate summary."
    except Exception as e:
        print(f"An error occurred with the OpenAI API: {e}")
        raise
