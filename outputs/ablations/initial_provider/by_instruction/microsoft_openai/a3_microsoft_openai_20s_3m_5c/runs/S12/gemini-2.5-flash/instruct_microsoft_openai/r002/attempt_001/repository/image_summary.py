
import os
from vision_client import VisionClient
from vision_models import ImageAnalysisRequest

def summarize_image_analysis(analysis_results_text: str) -> str:
    client = VisionClient().get_openai_client()

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "user",
                "content": f"Summarize the following image analysis results:

{analysis_results_text}"
            }
        ],
        max_tokens=500,
    )

    summary = response.choices[0].message.content
    return summary
