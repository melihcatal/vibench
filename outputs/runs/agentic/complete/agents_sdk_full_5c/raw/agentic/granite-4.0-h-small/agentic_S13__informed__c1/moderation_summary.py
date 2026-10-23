# moderation_summary.py
import json
from safety_models import ModerationResponse

def summarize_moderation(responses: List[ModerationResponse]) -> dict:
    """Produce a concise summary of moderation decisions.

    Provider agnostic – works with any moderation response (here we use Amazon
    Comprehend Toxicity responses).
    """
    summary = {
        "total": len(responses),
        "allowed": 0,
        "rejected": 0,
        "details": []
    }
    for resp in responses:
        summary["details"].append({
            "text": resp.text[:50],
            "decision": resp.decision,
            "toxicity_score": resp.scores.get("toxicity", 0.0)
        })
        if resp.decision == "ALLOW":
            summary["allowed"] += 1
        else:
            summary["rejected"] += 1
    return summary

if __name__ == "__main__":
    # Demo using dummy ModerationResponse objects.
    from safety_models import ModerationResponse
    demo = [
        ModerationResponse(text="Nice post!", decision="ALLOW", scores={"toxicity": 0.1}),
        ModerationResponse(text="You suck.", decision="REJECT", scores={"toxicity": 0.9})
    ]
    print(json.dumps(summarize_moderation(demo), indent=2))
