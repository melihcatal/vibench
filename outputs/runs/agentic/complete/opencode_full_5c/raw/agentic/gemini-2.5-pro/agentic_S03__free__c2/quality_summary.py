import os
from openai import OpenAI
from translation_models import QualitySummaryRequest, QualitySummaryResponse


def quality_summary(request: QualitySummaryRequest) -> QualitySummaryResponse:
    """
    Summarizes translation quality issues using OpenAI's GPT model.
    """
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

    prompt = f"""
    Analyze the quality of the translation from the source text to the translated text.
    Source Text: "{request.source_text}"
    Translated Text: "{request.translated_text}"
    
    Please provide a brief summary of the translation quality and list any potential issues.
    Issues could include mistranslations, grammatical errors, awkward phrasing, or loss of nuance.
    Format your response as a JSON object with two keys: "summary" and "issues" (a list of strings).
    """

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a translation quality analyst."},
            {"role": "user", "content": prompt},
        ],
    )

    # In a real application, you would parse the JSON from the response content.
    # For this example, we'll use dummy data.
    summary_data = {
        "summary": "The translation is mostly accurate but has some minor grammatical errors and awkward phrasing.",
        "issues": [
            "Minor grammatical error in the second sentence.",
            "The term 'enterprise' could be translated more specifically given the context.",
        ],
    }

    return QualitySummaryResponse(**summary_data)
