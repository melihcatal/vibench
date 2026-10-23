from google.cloud import aiplatform

def summarize_transcript(text_content, project_id, location="us-central1"):
    aiplatform.init(project=project_id, location=location)

    # Using the text-bison model for summarization
    # https://cloud.google.com/vertex-ai/docs/generative-ai/model-reference/text
    parameters = {
        "temperature": 0.2,
        "max_output_tokens": 256,
        "top_p": 0.95,
        "top_k": 40,
    }
    
    model = aiplatform.TextGenerationModel.from_pretrained("text-bison")
    response = model.predict(f"Summarize the following text:\n\n{text_content}", **parameters)
    
    return response.text
