from __future__ import annotations

import os
from typing import Iterable

from perspective import PerspectiveAPI


PERSPECTIVE_ATTRIBUTES = {"TOXICITY": {}, "INSULT": {}, "THREAT": {}}


def visual_safety_text(text_fragments: Iterable[str]) -> dict:
    client = PerspectiveAPI(api_key=os.getenv("PERSPECTIVE_API_KEY", ""))
    combined = ", ".join(fragment.strip() for fragment in text_fragments if fragment.strip())
    response = client.score(text=combined, attributes=PERSPECTIVE_ATTRIBUTES, languages=["en"])
    scores = response["attributeScores"]
    return {
        "provider": "commentanalyzer.googleapis.com",
        "toxicity": scores["TOXICITY"]["summaryScore"]["value"],
        "insult": scores["INSULT"]["summaryScore"]["value"],
        "threat": scores["THREAT"]["summaryScore"]["value"],
    }
