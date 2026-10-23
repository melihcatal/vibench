import os
from google.cloud import aiplatform
from vertexai.preview.generative_models import GenerativeModel, Part, Image
from speech_models import SummarizationRequest, SummarizationResult

def archive_summary(request: SummarizationRequest, project_id: str, location: str = "us-central1") -> SummarizationResult:
    aiplatform.init(project=project_id, location=location)
    model = GenerativeModel("gemini-pro") # Using gemini-pro for text generation
    
    prompt = f"Summarize the following text:\n\n{request.text}\n\nSummary:"

    response = model.generate_content(
        contents=[Part.from_text(prompt)],
        generation_config={
            "max_output_tokens": request.max_output_tokens,
        }
    )
    
    return SummarizationResult(summary=response.text)
