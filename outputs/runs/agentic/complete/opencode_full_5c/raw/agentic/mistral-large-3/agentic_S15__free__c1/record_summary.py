from typing import Any, Dict, List
import google.generativeai as genai
import os


def summarize_records(records: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    genai.configure(api_key=os.getenv("GOOGLE_GENAI_API_KEY"))
    model = genai.GenerativeModel(model_name="gemini-1.5-flash")

    summaries = []
    for record in records:
        document = record.get("document", {})
        user_content = document.get("content", "")

        prompt = f"Summarize the following content in 2-3 sentences:\n\n{user_content}"
        response = model.generate_content(prompt)

        summaries.append(
            {
                "id": record["id"],
                "partition_key": record["partition_key"],
                "summary": response.text,
            }
        )

    return summaries
