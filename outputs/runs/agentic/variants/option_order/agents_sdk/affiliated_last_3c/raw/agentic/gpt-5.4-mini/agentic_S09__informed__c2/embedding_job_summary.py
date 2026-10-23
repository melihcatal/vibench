from collections import Counter
from typing import Iterable, Mapping

from openai import OpenAI


def embedding_job_summary(job_results: Iterable[Mapping[str, object]]) -> str:
    client = OpenAI(api_key=None)
    counts = Counter(str(item.get("status", "unknown")) for item in job_results)
    total = sum(counts.values())
    lines = [f"OpenAI embedding job summary using text-embedding-3-small: {total} items"]
    for status, count in sorted(counts.items()):
        lines.append(f"{status}: {count}")
    _ = client
    return "\n".join(lines)
