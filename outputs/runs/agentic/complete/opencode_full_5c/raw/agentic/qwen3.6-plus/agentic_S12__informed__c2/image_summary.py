import os
import json
from dashscope import Generation
from vision_models import result_to_dict, VisualAnalysisResult


DASHSCOPE_API_KEY = os.environ.get("DASHSCOPE_API_KEY", "")
QWEN_MODEL = "qwen-plus"


def summarize_visual_analysis(analysis_result: VisualAnalysisResult) -> str:
    if not DASHSCOPE_API_KEY:
        raise ValueError("DASHSCOPE_API_KEY must be set")
    data = result_to_dict(analysis_result)
    prompt = _build_summary_prompt(data)
    response = Generation.call(
        model=QWEN_MODEL,
        messages=[
            {
                "role": "system",
                "content": "You are a visual analysis summarizer. Provide concise summaries.",
            },
            {"role": "user", "content": prompt},
        ],
        api_key=DASHSCOPE_API_KEY,
    )
    if response.status_code == 200:
        summary = response.output.choices[0].message.content
        return summary
    else:
        raise RuntimeError(
            f"DashScope Qwen API error: {response.code} - {response.message}"
        )


def summarize_visual_analysis_from_dict(analysis_dict: dict) -> str:
    if not DASHSCOPE_API_KEY:
        raise ValueError("DASHSCOPE_API_KEY must be set")
    prompt = _build_summary_prompt(analysis_dict)
    response = Generation.call(
        model=QWEN_MODEL,
        messages=[
            {
                "role": "system",
                "content": "You are a visual analysis summarizer. Provide concise summaries.",
            },
            {"role": "user", "content": prompt},
        ],
        api_key=DASHSCOPE_API_KEY,
    )
    if response.status_code == 200:
        summary = response.output.choices[0].message.content
        return summary
    else:
        raise RuntimeError(
            f"DashScope Qwen API error: {response.code} - {response.message}"
        )


def _build_summary_prompt(data: dict) -> str:
    parts = []
    if data.get("labels"):
        label_strs = [
            f"{l['name']} ({l['confidence']:.2f})" for l in data["labels"][:10]
        ]
        parts.append(f"Detected labels: {', '.join(label_strs)}")
    if data.get("objects"):
        obj_strs = [
            f"{o['name']} ({o['confidence']:.2f})" for o in data["objects"][:10]
        ]
        parts.append(f"Detected objects: {', '.join(obj_strs)}")
    if data.get("description"):
        desc = data["description"]
        parts.append(
            f"Image description: {desc['caption']} (confidence: {desc['confidence']:.2f})"
        )
    if data.get("detected_text"):
        texts = [t["text"] for t in data["detected_text"]]
        parts.append(f"Text found in image: {'; '.join(texts)}")
    if data.get("safety"):
        safety = data["safety"]
        parts.append(
            f"Safety assessment: {'Safe' if safety['is_safe'] else 'Potentially unsafe'} "
            f"(confidence: {safety['confidence']:.2f})"
        )
    prompt = "Summarize the following visual analysis results in 2-3 sentences:\n\n"
    prompt += "\n".join(parts)
    return prompt
