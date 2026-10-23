# secret_label_safety.py
import os
from safety_utils import check_unsafe_text, UnsafeCategory
from security_client import get_secret_meta
from security_models import FetchSecretRequest


def check_secret_labels(queries: List[FetchSecretRequest]) -> List[Dict]:
    """Inspect each secret's metadata for unsafe language in labels or notes.
    Returns a list of dicts with secret name and safety result.
    """
    results = []
    for req in queries:
        meta = get_secret_meta(req["secret_name"])
        labels = meta.get("labels", [])
        notes = meta.get("notes", "")
        unsafe = check_unsafe_text("\n".join(labels) + "\\n" + notes)
        results.append(
            {
                "secret_name": meta.get("name"),
                "unsafe": unsafe == UnsafeCategory.UNSAFE,
                "issues_found": unsafe.value,
            }
        )
    return results


# Example usage
if __name__ == "__main__":
    sample_queries = [
        {"secret_name": "sample-secret"},
    ]
    safety = check_secret_labels(sample_queries)
    print(safety)
