import google.generativeai as genai
import os


def answer_with_context(question: str, context: str) -> str:
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(
        context + "\n\n" + question,
        generation_config=genai.GenerationConfig(
            temperature=0.2,
            max_output_tokens=512,
        ),
    )
    return response.text
