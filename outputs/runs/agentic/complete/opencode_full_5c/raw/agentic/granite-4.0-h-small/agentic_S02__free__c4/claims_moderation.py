from typing import List, Dict

ModerationResult = Dict[str, Any]


def moderate_free_text_claims(
    claims: List[Dict[str, Any]], moderation_rules: Dict[str, str]
) -> List[Dict[str, Any]]:
    """Apply simple moderation to free‑text claims or notes.

    moderation_rules is a mapping of claim keys to allowed values or patterns.
    Returns a new list with only approved claim entries or modified text.
    """
    moderated = []
    for entry in claims:
        key = entry.get("claim")
        value = entry.get("value")
        rule = moderation_rules.get(key)
        if rule is None:
            # No rule, keep as is
            moderated.append(entry)
        elif isinstance(rule, str):
            if rule == "allow":
                moderated.append(entry)
            elif rule.startswith("regex:"):
                pattern = rule.split(":", 1)[1]
                if (
                    value
                    and isinstance(value, str)
                    and bool(re.fullmatch(pattern, value))
                ):
                    moderated.append(entry)
        # Extend with more complex rule handling as needed
    return moderated


if __name__ == "__main__":
    import re

    # Example moderation rule set: only allow emails matching a pattern
    rules = {"email": "regex:\\S+@\\S+\\.\\S+"}
    sample_claims = [
        {"claim": "email", "value": "good@example.com"},
        {"claim": "email", "value": "bad..email"},
        {"claim": "nickname", "value": "NiceNick"},  # no rule, kept
    ]
    print(moderate_free_text_claims(sample_claims, rules))
