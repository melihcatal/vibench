import os
from openai import AzureOpenAI

def extract_structured_fields(document_text: str, schema: dict) -> dict:
    # Azure OpenAI API configuration
    azure_endpoint = os.environ.get("AZURE_OPENAI_ENDPOINT")
    api_key = os.environ.get("AZURE_OPENAI_KEY")
    api_version = os.environ.get("AZURE_OPENAI_API_VERSION", "2024-02-01") # e.g., "2024-02-01"
    deployment_name = os.environ.get("AZURE_OPENAI_DEPLOYMENT_NAME") # e.g., "gpt-4o"

    if not azure_endpoint or not api_key or not deployment_name:
        raise ValueError("AZURE_OPENAI_ENDPOINT, AZURE_OPENAI_KEY, and AZURE_OPENAI_DEPLOYMENT_NAME environment variables must be set.")

    client = AzureOpenAI(
        azure_endpoint=azure_endpoint,
        api_key=api_key,
        api_version=api_version
    )

    # The prompt will instruct the model to extract information based on the provided schema.
    # For robust extraction, consider using Azure OpenAI's Function Calling capabilities.
    prompt = f"""You are an AI assistant designed to extract structured information from documents.
    Extract the following fields from the document text provided, according to the JSON schema below.
    Return the extracted data as a JSON object.

    Document Text:
    '''{document_text}'''

    JSON Schema:
    '''{schema}'''

    Extracted JSON:
    """

    try:
        response = client.chat.completions.create(
            model=deployment_name, # Use your deployment name
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"} # Request JSON output
        )
        extracted_data_str = response.choices[0].message.content
        import json
        return json.loads(extracted_data_str)
    except Exception as e:
        print(f"Error during field extraction: {e}")
        return {}
