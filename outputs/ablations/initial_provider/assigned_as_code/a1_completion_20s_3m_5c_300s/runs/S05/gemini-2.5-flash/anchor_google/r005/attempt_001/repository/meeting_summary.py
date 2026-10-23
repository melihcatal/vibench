import vertexai
from vertexai.language_models import TextGenerationModel

def summarize_meeting_chunk(text, project_id, location="us-central1"):
    vertexai.init(project=project_id, location=location)
    model = TextGenerationModel.from_pretrained("text-bison")

    prompt = f"Summarize the following meeting transcript chunk: {text}"

    response = model.predict(
        prompt,
        temperature=0.2,
        max_output_tokens=256,
        top_p=0.8,
        top_k=40,
    )
    return response.text
