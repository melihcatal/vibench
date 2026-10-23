from vision_client import call_vision_api, OPENAI_VISION_MODEL
from vision_models import ImageSummaryRequest, ImageSummaryResponse


def summarize_visual_analysis(
    request: ImageSummaryRequest, model: str | None = None
) -> ImageSummaryResponse:
    label_names = [label.name for label in request.labels if label.confidence > 0.5]
    text_segments = [t.text for t in request.detected_text]
    safety_status = "safe" if (request.safety and request.safety.is_safe) else "flagged"

    analysis_parts = []
    if request.description:
        analysis_parts.append(f"Description: {request.description}")
    if label_names:
        analysis_parts.append(f"Detected labels: {', '.join(label_names)}")
    if text_segments:
        analysis_parts.append(f"Text found in image: {'; '.join(text_segments)}")
    analysis_parts.append(f"Safety assessment: {safety_status}")

    combined = "\n".join(analysis_parts)

    system_prompt = (
        "You are a visual analysis summarizer. Create a concise summary of the image analysis results. "
        "Provide a one-paragraph summary followed by 3-5 key insights as bullet points."
    )
    user_prompt = (
        f"Summarize the following visual analysis results:\n\n{combined}\n\n"
        "Provide a brief summary paragraph and then list the key insights."
    )

    raw_output = call_vision_api(
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        model=model or OPENAI_VISION_MODEL,
        temperature=0.3,
        max_tokens=512,
    )

    summary_lines = raw_output.strip().split("\n")
    summary = ""
    key_insights = []
    capturing_insights = False
    for line in summary_lines:
        stripped = line.strip().lstrip("-*• ")
        if capturing_insights and stripped:
            key_insights.append(stripped)
        elif not stripped:
            capturing_insights = True
        elif not summary:
            summary = stripped

    if not summary and summary_lines:
        summary = summary_lines[0].strip()

    return ImageSummaryResponse(summary=summary, key_insights=key_insights)


def summarize_multiple_analyses(
    requests: list[ImageSummaryRequest], model: str | None = None
) -> list[ImageSummaryResponse]:
    results = []
    for req in requests:
        result = summarize_visual_analysis(req, model=model)
        results.append(result)
    return results
