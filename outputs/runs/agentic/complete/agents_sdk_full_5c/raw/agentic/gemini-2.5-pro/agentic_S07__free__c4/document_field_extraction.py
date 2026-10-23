import os
import json
import anthropic

def extract_fields_with_anthropic(document_text: str, fields: dict) -> dict:
    """
    Extracts structured fields from document text using Anthropic's Claude.

    Args:
        document_text: The unstructured text from an OCR process.
        fields: A dictionary describing the fields to extract,
                e.g., {"invoice_number": "string", "total_amount": "float"}

    Returns:
        A dictionary containing the extracted data.
    """
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY environment variable not set.")

    client = anthropic.Anthropic(api_key=api_key)

    prompt = f"""
        Given the following document text, extract the specified fields into a valid JSON object.
        The required JSON schema is: {json.dumps(fields)}

        Here is the document text:
        ---
        {document_text}
        ---

        Please provide only the JSON object as the output.
    """

    try:
        message = client.messages.create(
            model="claude-3-sonnet-20240229",
            max_tokens=1024,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        response_text = message.content[0].text
        return json.loads(response_text)

    except (anthropic.APIError, json.JSONDecodeError) as e:
        print(f"An error occurred: {e}")
        return {"error": str(e)}

