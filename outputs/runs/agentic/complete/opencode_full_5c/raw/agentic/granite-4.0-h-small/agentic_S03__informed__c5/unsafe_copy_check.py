import os
from google.genai import ContentReference, HarmType, HarmSeverity
from google.genai import HarmBlockThreshold

# Use Gemini for toxicity / unsafe content detection
model = "gemini-1.5-flash"


def check_unsafe(localized_copy):
    """Check a list of translated strings for unsafe content.

    Args:
        localized_copy (list[str]): translated texts.

    Returns:
        dict: mapping index->list of detected issues (or empty list if clean).
    """
    # Build a prompt listing all strings for the model to evaluate
    text_bodies = "\\n".join(f"{i + 1}: {t}" for i, t in enumerate(localized_copy))
    prompt = (
        "For each string in the list below, identify any unsafe content such as:\\n"
        "- hate speech\\n- self‑harm\\n- sexual content\\n- misinformation\\n"
        'Return a JSON‑like mapping: {"index": ["issue1", "issue2"]} where index starts at 1.\\n'
        "If a string is safe, do not include its index.\\n" + text_bodies
    )

    response = model.generate_content(
        prompt,
        generation_config={"temperature": 0.0, "max_output_tokens": 500},
        safety_settings={
            HarmType.HARMS_CATEGORY_TOXICITY: HarmSeverity.BLOCK_ALL,
            HarmType.HARMS_CATEGORY_SELF_HARM: HarmSeverity.BLOCK_ALL,
            HarmType.HARMS_CATEGORY_SEXUAL: HarmSeverity.BLOCK_ALL,
        },
    )
    content = response.text.strip()
    # Very simple parsing: each line like \"3: hate speech, self-harm\" → {3: [...]}
    issues = {}
    for line in content.splitlines():
        parts = line.split(":")
        if len(parts) != 2:
            continue
        idx_str, rest = parts
        idx = idx_str.strip()
        if not idx.isdigit():
            continue
        indices = int(idx) - 1  # convert to 0‑based
        # Split issues, ignore empty
        issues[indices] = [i.strip() for i in rest.split(",") if i.strip()]
    return issues
