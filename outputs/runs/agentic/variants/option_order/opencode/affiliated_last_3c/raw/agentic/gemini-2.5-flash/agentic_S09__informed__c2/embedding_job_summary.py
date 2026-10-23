import os
import google.generativeai as genai
from embeddings_models import SummaryRequest, SummaryResponse


def summarize_embedding_job_results(request: SummaryRequest) -> SummaryResponse:
    """
    Summarizes embedding job results using Google Gemini API.
    """
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
    model = genai.GenerativeModel("gemini-pro")  # Using a general LLM for summarization
    prompt = f"Please summarize the following text: {request.text_to_summarize}"
    response = model.generate_content(prompt)
    return SummaryResponse(summary=response.text)
