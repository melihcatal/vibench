from google.cloud import aiplatform

def archive_summary(text, project_id, location="us-central1"):
    aiplatform.init(project=project_id, location=location)
    
    # Using a text-bison model for summarization
    # Model ID: "text-bison@001" or similar
    # Note: Specific model versions might change, this is an example.
    parameters = {
        "temperature": 0.2,
        "max_output_tokens": 256,
        "top_p": 0.95,
        "top_k": 40,
    }
    
    model = aiplatform.TextGenerationModel.from_pretrained("text-bison")

    prompt = f"Summarize the following transcript:

{text}

Summary:"

    response = model.predict(prompt, **parameters)

    return {"summary": response.text}
