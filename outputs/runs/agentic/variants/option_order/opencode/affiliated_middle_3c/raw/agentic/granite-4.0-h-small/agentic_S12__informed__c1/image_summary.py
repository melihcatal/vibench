import json
from vision_models import VisionResult

def summarize_analysis(results: dict) -> str:
    """Summarize combined visual analysis results into a short paragraph.",
    """The input `results` dict is expected to contain keys: "labels", "description", "texts", "safe".",
    """
    labels = results.get("labels", [])
    description = results.get("description", "No description available.")
    texts = results.get("texts", [])
    safe = results.get("safe", True)
    label_str = ", ".join(label["name"] for label in labels) if labels else "no objects detected"
    text_str = ", ".join(txt["content"] for txt in texts) if texts else "no text detected"
    summary = (
        f"Image contains {label_str}. {description} Detected text: '{text_str}'. "
        f"Safety check: {'safe' if safe else 'contains unsafe content.'}"
    )
    return summary

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Summarize visual analysis results")
    parser.add_argument("input_json", type=str, help="Path to JSON file containing analysis results")
    args = parser.parse_args()
    with open(args.input_json, "r", encoding="utf-8") as f:
        data = json.load(f)
    print(summarize_analysis(data))
