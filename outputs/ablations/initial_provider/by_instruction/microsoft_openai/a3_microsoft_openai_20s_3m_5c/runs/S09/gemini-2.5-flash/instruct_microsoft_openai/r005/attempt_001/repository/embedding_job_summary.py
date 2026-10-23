import os
from typing import List, Dict, Any
from google.cloud import language_v1

def summarize_embedding_job_results(job_results: List[Dict[str, Any]]) -> str:
    """Summarizes embedding job results using Google Cloud Language API.

    Args:
        job_results: A list of dictionaries, where each dictionary represents
                     a job result (e.g., {'text': '...', 'embedding': [...]}).

    Returns:
        A summarized text of the job results.
    """
    # Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set
    # os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/path/to/your/key.json"

    client = language_v1.LanguageServiceClient()

    full_text_to_summarize = "".join([result.get('text', '') for result in job_results if 'text' in result])

    if not full_text_to_summarize:
        return "No text found in job results to summarize."

    document = language_v1.Document(
        content=full_text_to_summarize,
        type_=language_v1.Document.Type.PLAIN_TEXT
    )

    # Currently, the Language API does not have a direct 'summarize' method exposed for general text.
    # A common approach for summarization with NLM API is to extract entities or analyze sentiment
    # to get a high-level understanding, or use specific models (e.g., Vertex AI for true summarization).
    # For the purpose of demonstration using language_v1, we will do entity analysis
    # as a form of 'summary' of key topics.

    # As a proxy for summarization, we'll extract key entities.
    response = client.analyze_entities(document=document)

    summary_parts = []
    if response.entities:
        summary_parts.append("Key entities identified:")
        for entity in response.entities:
            summary_parts.append(f"- {entity.name} (Type: {language_v1.Entity.Type(entity.type_).name})")
    else:
        summary_parts.append("No significant entities found.")

    return "\n".join(summary_parts)
