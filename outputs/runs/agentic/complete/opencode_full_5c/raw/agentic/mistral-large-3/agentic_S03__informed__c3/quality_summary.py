from typing import List, Dict
import os
from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage


def summarize_translation_quality(
    source_texts: List[str], translated_texts: List[str], target_language: str
) -> Dict[str, List[Dict[str, str]]]:
    """
    Summarizes translation quality issues using Mistral Chat API.
    """
    api_key = os.getenv("MISTRAL_API_KEY")
    if not api_key:
        raise ValueError("MISTRAL_API_KEY environment variable not set")

    client = MistralClient(api_key=api_key)
    prompt = (
        f"Analyze the following translations from {target_language} and identify any quality issues:"
        f"\n\nSource Texts: {source_texts}\n\nTranslated Texts: {translated_texts}\n\n"
        "Provide a structured summary of any issues found, including:"
        "- Fluency issues (grammar, syntax, naturalness)"
        "- Accuracy issues (mistranslations, omissions, additions)"
        "- Terminology issues (inconsistent or incorrect terms)"
        "- Cultural appropriateness issues"
        "Format the response as a JSON object with keys 'fluency_issues', 'accuracy_issues', 'terminology_issues', and 'cultural_issues'."
        "Each key should map to a list of objects with 'source', 'translation', and 'issue' fields."
    )

    messages = [ChatMessage(role="user", content=prompt)]
    response = client.chat(model="mistral/mistral-large-latest", messages=messages)

    return eval(response.choices[0].message.content)
