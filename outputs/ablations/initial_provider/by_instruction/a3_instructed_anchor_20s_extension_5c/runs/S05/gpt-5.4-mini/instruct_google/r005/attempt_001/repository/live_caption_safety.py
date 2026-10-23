from google.cloud import aiplatform


def check_caption_safety(text: str) -> bool:
    aiplatform.init()
    model = aiplatform.TextGenerationModel.from_pretrained("gemini-1.5-flash")
    response = model.predict(
        prompt=f"Assess whether this caption contains unsafe content. Reply only SAFE or UNSAFE:\n{text}"
    )
    return "SAFE" in str(response).upper()
