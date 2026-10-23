import vertexai
from vertexai.language_models import TextGenerationModel

def document_field_extraction(text: str, project_id: str, location: str):
    vertexai.init(project=project_id, location=location)
    model = TextGenerationModel.from_pretrained("text-bison@001")

    prompt = f"""
    Extract the following fields from the text below:
    - Name
    - Date
    - Amount

    Text: {text}

    Format the output as a JSON object.
    """
    
    response = model.predict(
        prompt,
        temperature=0.2,
        max_output_tokens=1024,
        top_p=0.8,
        top_k=40,
    )
    
    # In a real scenario, you would parse the JSON output from the model.
    # For this example, we return the raw text response.
    return {"extracted_fields_raw_response": response.text}
