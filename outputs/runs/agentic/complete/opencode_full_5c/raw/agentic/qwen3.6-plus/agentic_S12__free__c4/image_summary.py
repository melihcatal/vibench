import os
from openai import OpenAI
from vision_models import (
    VisionAnalysisResult,
    ImageLabel,
    ImageDescription,
    DetectedText,
    SafetyScore,
)

SUMMARY_MODEL = "gpt-4o"


def get_summary_client():
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is required")
    client = OpenAI(
        api_key=api_key,
        base_url="https://api.openai.com/v1",
    )
    return client


def summarize_labels(labels: list[ImageLabel]) -> str:
    if not labels:
        return "No labels detected."
    top = sorted(labels, key=lambda l: l.confidence, reverse=True)[:5]
    names = [l.name for l in top]
    return "Primary elements: " + ", ".join(names)


def summarize_description(desc: ImageDescription) -> str:
    if not desc:
        return "No description available."
    return desc.description


def summarize_texts(texts: list[DetectedText]) -> str:
    if not texts:
        return "No text detected."
    combined = " ".join(t.text for t in texts[:10])
    return f"Text found: {combined}"


def summarize_safety(safety: SafetyScore) -> str:
    if not safety:
        return "No safety analysis available."
    if safety.is_safe:
        return "Image passed safety checks."
    flagged = ", ".join(safety.flagged_categories)
    return f"Safety concerns detected in: {flagged}"


def summarize_visual_analysis(
    labels: list[ImageLabel] = None,
    description: ImageDescription = None,
    texts: list[DetectedText] = None,
    safety: SafetyScore = None,
) -> dict:
    summary_parts = []
    summary_parts.append(summarize_labels(labels or []))
    summary_parts.append(summarize_description(description))
    summary_parts.append(summarize_texts(texts or []))
    summary_parts.append(summarize_safety(safety))

    return {
        "label_summary": summarize_labels(labels or []),
        "description_summary": summarize_description(description),
        "text_summary": summarize_texts(texts or []),
        "safety_summary": summarize_safety(safety),
        "combined_summary": " | ".join(summary_parts),
    }


def summarize_from_result(result: VisionAnalysisResult) -> dict:
    return summarize_visual_analysis(
        labels=result.labels,
        description=result.description,
        texts=result.detected_texts,
        safety=result.safety,
    )


def generate_ai_summary(result: VisionAnalysisResult) -> str:
    client = get_summary_client()
    input_text = f"Labels: {[l.name for l in result.labels]}\nDescription: {result.description.description if result.description else 'N/A'}\nText: {[t.text for t in result.detected_texts]}\nSafety: {'Safe' if result.safety and result.safety.is_safe else 'Flagged'}"
    response = client.chat.completions.create(
        model=SUMMARY_MODEL,
        messages=[
            {
                "role": "system",
                "content": "You are a visual analysis summarizer. Produce a concise 2-3 sentence summary of the image analysis results.",
            },
            {"role": "user", "content": input_text},
        ],
        max_tokens=256,
    )
    return response.choices[0].message.content.strip()


if __name__ == "__main__":
    import json

    sample = VisionAnalysisResult(
        labels=[ImageLabel("cat", 0.95, "animal"), ImageLabel("grass", 0.88, "nature")],
        description=ImageDescription(
            description="A cat sitting on green grass in daylight."
        ),
        detected_texts=[DetectedText(text="No text found")],
        safety=SafetyScore(is_safe=True, overall_score=0.98),
    )
    summary = summarize_from_result(sample)
    print(json.dumps(summary, indent=2))
