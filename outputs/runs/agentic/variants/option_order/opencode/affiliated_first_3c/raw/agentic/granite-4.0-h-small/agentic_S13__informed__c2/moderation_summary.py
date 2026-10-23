from typing import List, Dict

# LATER-STEP
# Summarize moderation decisions for a collection of results.
# Provider identification: GRANITE (IBM watsonx.ai text chat)


def summarize(results: List[Dict[str, any]]) -> str:
    """
    Parameters
    ----------
    results: List[Dict[str, any]]
        List of dicts output by the same-scenario moderation functions (e.g., moderate_text.py).

    Returns
    -------
    str
        A concise summary of the moderation outcome.
    """
    unsafe_count = sum(item["unsafe"] for item in results)
    if unsafe_count == 0:
        return "All content passed safety checks."
    elif unsafe_count == len(results):
        return "All content flagged as unsafe."
    else:
        unsafe_msgs = [idx for idx, r in enumerate(results) if r["unsafe"]]
        return f"{unsafe_count} out of {len(results)} messages were flagged unsafe: {unsafe_msgs}"
