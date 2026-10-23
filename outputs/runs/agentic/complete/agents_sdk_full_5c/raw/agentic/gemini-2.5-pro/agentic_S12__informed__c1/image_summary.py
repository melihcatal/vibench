import os
from openai import OpenAI
from vision_models import VisionResult


def summarize_vision_result(vision_result: VisionResult) -> str:
    """Summarizes the results of a vision analysis using OpenAI GPT."""
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

    prompt_parts = []
    if vision_result.description:
        prompt_parts.append(f"The image is described as: '{vision_result.description}'.")
    if vision_result.labels:
        labels_str = ", ".join([label.name for label in vision_result.labels[:5]])
        prompt_parts.append(f"It contains objects and concepts like: {labels_str}.")
    if vision_result.texts:
        text_str = " ".join([text.text for text in vision_result.texts])
        prompt_parts.append(f"The following text was detected: '{text_str}'.")

    if not prompt_parts:
        return "Not enough information to generate a summary."

    full_prompt = " ".join(prompt_parts)
    system_prompt = "You are an expert at summarizing image analysis results into a concise, human-readable paragraph."
    user_prompt = f"Please summarize the following image analysis:\n\n{full_prompt}"

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.5,
        max_tokens=150,
    )
    return response.choices[0].message.content
