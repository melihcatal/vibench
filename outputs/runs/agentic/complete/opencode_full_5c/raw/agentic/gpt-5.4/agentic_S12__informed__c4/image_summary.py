from __future__ import annotations

from openai import OpenAI

from vision_models import VisualAnalysisBundle


def image_summary(bundle: VisualAnalysisBundle) -> dict:
    client = OpenAI(api_key=__import__("os").getenv("OPENAI_API_KEY"))
    response = client.responses.create(
        model="gpt-4.1-mini",
        input=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "input_text",
                        "text": f"Summarize this image analysis in 2 concise sentences: {bundle.to_dict()}",
                    }
                ],
            }
        ],
    )
    return {
        "provider": "openai:gpt-4.1-mini",
        "summary": response.output_text.strip(),
    }
