from __future__ import annotations

from vision_client import get_openai_client
from vision_models import VisualAnalysisBundle, build_visual_summary_payload


def image_summary(bundle: VisualAnalysisBundle) -> str:
    client = get_openai_client()
    response = client.responses.create(
        model="gpt-4.1-mini",
        input=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "input_text",
                        "text": "Summarize these visual analysis results in 2 concise sentences: "
                        + str(build_visual_summary_payload(bundle)),
                    }
                ],
            }
        ],
    )
    return response.output_text.strip()
