import json
from typing import List, Mapping, Any

# Later-step scored file: claims_moderation.py
# Moderate free-text claims or notes coming from federated providers

def moderate_claim(claim_text: str, policy: Mapping[str, Any]) -> Mapping[str, Any]:
    """
    policy example:
    {
        "max_length": 200,
        "allowed_keywords": ["subject", "topic"],
        "disallowed_keywords": ["confidential", "secret"]
    }
    """
    moderated = {
        "original": claim_text,
        "is_allowed": True,
        "reason": None,
        "cleaned": claim_text.strip()
    }
    if len(moderated["cleaned"]) > policy.get("max_length", 1000):
        moderated.update({
            "is_allowed": False,
            "reason": "exceeds max length",
            "cleaned": claim_text[:policy["max_length"]].strip()
        })
        return moderated
    for kw in policy.get("disallowed_keywords", []):
        if kw.lower() in moderated["cleaned"].lower():
            moderated.update({
                "is_allowed": False,
                "reason": f"contains disallowed keyword '{kw}'",
                "cleaned": None
            })
            return moderated
    for kw in policy.get("allowed_keywords", []):
        if kw.lower() in moderated["cleaned"].lower():
            break
    else:
        moderated.update({
            "is_allowed": False,
            "reason": "missing required keyword",
            "cleaned": None
        })
        return moderated
    return moderated

# Batch moderation helper
@staticmethod
    def moderate_batch(claims_list: List[Mapping[str, Any]], policy: Mapping[str, Any]) -> List[Mapping[str, Any]]:
        return [moderate_claim(c["text"], policy) for c in claims_list]

# Example usage (CLI)
if __name__ == "__main__":
    import sys
    policy = json.loads(sys.argv[1])
    claim = {"text": sys.argv[2]}
    result = moderate_claim(claim["text"], policy)
    print(json.dumps(result, indent=2))
