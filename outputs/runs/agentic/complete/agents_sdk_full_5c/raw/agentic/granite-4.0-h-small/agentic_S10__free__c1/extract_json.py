import openai
import model_client
import model_models

def extract_json(text: str, schema: dict, model: str = "gpt-4o-mini") -> dict:
    """Extracts structured JSON from text using the hosted LLM.
    Args:
        text (str): Unstructured input text.
        schema (dict): JSON Schema describing the desired output fields.
        model (str): LLM model (default: gpt-4o-mini).
    Returns:
        dict: Normalized JSON matching the provided schema.
    """
    safe_prompt = model_client.check_prompt(text)
    # Build prompt with schema inline for clarity
    prompt = f"Given the following unstructured text:\n\n{text}\n\nPlease extract the information and return it as JSON that conforms to this schema. The JSON must be the ONLY output, no explanation.\n\nSchema:\n{model_models.json_schema_to_string(schema)}\n"
    response = openai.ChatCompletion.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
    )
    raw = response.choices[0].message.content.strip()
    # Parse and validate the JSON response against the schema
    return model_models.parse_and_validate_json(raw, schema)
