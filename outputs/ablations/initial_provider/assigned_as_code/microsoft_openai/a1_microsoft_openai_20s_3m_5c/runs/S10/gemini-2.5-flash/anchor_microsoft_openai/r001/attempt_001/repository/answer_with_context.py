import os
from model_client import get_vertex_ai_model_client
from model_models import TextGenerationRequest, TextGenerationResponse
from typing import Dict, Any

def answer_with_context(payload: Dict[str, Any], config: Dict[str, Any] = None) -> Dict[str, Any]:
    config = config or {}
    project_id = config.get("project_id") or os.environ.get("GOOGLE_CLOUD_PROJECT")
    location = config.get("location") or os.environ.get("GOOGLE_CLOUD_LOCATION")
    model_id = config.get("model_id") or "gemini-1.5-flash-001"

    vertex_ai = get_vertex_ai_model_client(project_id, location)

    question = payload.get("question", "")
    context = payload.get("context", "")

    prompt = f"""Answer the following question based on the provided context only.
    If the answer is not in the context, say "I cannot answer based on the provided context."

    Context: {context}

    Question: {question}
    Answer:
    """

    request = TextGenerationRequest(prompt=prompt, model_id=model_id)
    
    model = vertex_ai.preview.generative_models.GenerativeModel(model_id)
    response = model.generate_content(
        contents=[{"role": "user", "parts": [{"text": request.prompt}]}]
    )

    generated_text = ""
    if response.candidates and response.candidates[0].content.parts:
        generated_text = response.candidates[0].content.parts[0].text

    return TextGenerationResponse(text=generated_text).text
