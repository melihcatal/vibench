import json
from typing import List, Dict

def image_summary(results: Dict[str, any]) -> str:
    """Summarize visual analysis results (labels, description, text, safety) into a concise report."""
    summary_lines = []
    if "labels" in results:
        summary_lines.append("Detected labels/tags:")
        summary_lines.extend([f" - {tag}" for tag in results["labels"]) if isinstance(results["labels"], list) else [] )
    if "description" in results:
        summary_lines.append("Image description:")
        summary_lines.append(f" - {results['description']}" if results["description"] else " - (no description)")
    if "text" in results:
        summary_lines.append("Detected text in image:")
        summary_lines.extend([f" - Line {i+1}: {line}" for i, line in enumerate(results["text"])])
    if "safety" in results:
        summary_lines.append("Safety check:")
        unsafe = results["safety"].get("detected", [])
        if unsafe:
            summary_lines.append(f" - Unsafe content detected: {', '.join(unsafe)}")
        else:
            summary_lines.append(" - No unsafe content detected")
    return "\\n".join(summary_lines)
