import google.generativeai as genai
from model_client import get_google_genai_client
from model_models import normalize_response

def answer_with_context(question: str, context: str) -> str:
    genai = get_google_genai_client()
    model_id = "gemini-1.5-pro"
    model = genai.GenerativeModel(model_id)

    prompt = (
        f"Based on the following context, answer the question comprehensively. "
        f"If the answer cannot be found in the context, state that.\n\n"
        f"Context:\n{context}\n\n"
        f"Question: {question}\n\n"
        f"Answer:"
    )

    response = model.generate_content(
        prompt,
        generation_config=genai.types.GenerationConfig(temperature=0.1, max_output_tokens=500)
    )
    normalized = normalize_response(response, "google")
    return normalized.get("text", "")