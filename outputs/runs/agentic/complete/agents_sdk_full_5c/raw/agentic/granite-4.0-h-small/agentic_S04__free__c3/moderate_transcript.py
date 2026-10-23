import re
from typing import Dict, Any, List
from speech_models import BatchTranscriptionResult
import json

def moderate_transcript(transcript: BatchTranscriptionResult) -> Dict[str, Any]:
    """Simple moderation: filter out profanity and replace with asterisks.

    Args:
        transcript (BatchTranscriptionResult): JSON returned from Azure Batch Speech-to-Text.

    Returns:
        dict: A modified transcript with moderated segment text.
    """
    # Define a basic profanity list (extend as needed)
    profanity_list = {"damn", "hell", "ass", "bitch", "bastard", "slut", "dick", "fuck", "cunt"}
    # Compile a regex pattern for word boundaries (case insensitive)
    pattern = re.compile(r"\b(" + "|".join(map(re.escape, profanity_list)) + r")\b", re.IGNORECASE)

    def replace_profanity(text: str) -> str:
        def repl(m):
            return "*" * len(m.group(0))
        return pattern.sub(repl, text)

    # Navigate the result structure; Azure returns results -> items -> items (segment) -> content
    results = transcript.get("results", [])
    moderated = []
    for result in results:
        item = result.get("items", [])
        moderated_item = []
        for segment in item:
            seg = segment.copy()
            content = seg.get("content", "")
            moderated_content = replace_profanity(content)
            seg["content"] = moderated_content
            moderated_item.append(seg)
        result["items"] = moderated_item
        moderated.append(result)
    transcript["results"] = moderated
    return transcript

# CLI entrypoint for quick testing
if __name__ == "__main__":
    import sys, json
    if len(sys.argv) != 2:
        print("Usage: python moderate_transcript.py <result_json_file>")
        sys.exit(1)
    file_path = sys.argv[1]
    with open(file_path, "r", encoding="utf-8") as f:
        raw = json.load(f)
    moderated = moderate_transcript(raw)
    print(json.dumps(moderated, ensure_ascii=False, indent=2))
