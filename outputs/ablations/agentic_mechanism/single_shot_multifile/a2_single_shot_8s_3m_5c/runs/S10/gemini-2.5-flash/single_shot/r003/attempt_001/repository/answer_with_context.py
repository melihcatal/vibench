import os
from google.cloud import aiplatform
from vertexai.generative_models import GenerativeModel, Part, HarmCategory, HarmBlockThreshold
from model_models import ContextAnswerRequest, LLMResponse
import logging

VERTEX_AI_PROJECT = os.environ.get("GOOGLE_CLOUD_PROJECT_ID")
VERTEX_AI_LOCATION = os.environ.get("GOOGLE_CLOUD_LOCATION", "us-central1")

if VERTEX_AI_PROJECT and VERTEX_AI_LOCATION:
    aiplatform.init(project=VERTEX_AI_PROJECT, location=VERTEX_AI_LOCATION)
else:
    logging.warning("GOOGLE_CLOUD_PROJECT_ID or GOOGLE_CLOUD_LOCATION not set. Vertex AI client might not initialize properly.")


def answer_with_context(request: ContextAnswerRequest) -> LLMResponse:

    model_id = request.model_id if request.model_id else "gemini-1.5-pro"
    model = GenerativeModel(model_id)

    safety_settings = {
        HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
        HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
        HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
        HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
    }

    full_prompt = (
        f"Context: {request.context}\n\n"
        f"Question: {request.prompt}\n\n"
        "Based on the provided context, answer the question comprehensively. "
        "If the answer cannot be found in the context, state that explicitly."
    )

    response = model.generate_content(
        contents=[Part.from_text(full_prompt)],
        generation_config={
            "max_output_tokens": request.max_tokens,
            "temperature": request.temperature,
            **request.kwargs
        },
        safety_settings=safety_settings
    )

    answer = response.text
    return LLMResponse(text=answer, model_id=model_id)