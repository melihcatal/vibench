import json


def normalize_transcript(output):
    """Convert Transcribe JSON output to a plain text transcript.

    Parameters
    ----------
    output : dict
        Transcribe 'results' structure.

    Returns
    -------
    str
        Cleaned transcript string.
    """
    lines = []
    for result in output["results"]:
        items = result.get("items", [])
        for item in items:
            # Keep only alphabetic content, strip punctuation if desired
            word = item.get("alternatives", [{}])[0].get("content", "")
            lines.append(word)
    return " ".join(lines)


def parse_timestamps(output):
    """Extract word-level timestamps from Transcribe output.

    Parameters
    ----------
    output : dict
        Transcribe 'results' structure.

    Returns
    -------
    list[dict]
        Each dict contains 'start_time', 'end_time', 'content'.
    """
    timestamps = []
    for result in output["results"]:
        items = result.get("items", [])
        for item in items:
            alt = item.get("alternatives", [{}])[0]
            word = alt.get("content", "")
            start = alt.get("start_time")
            end = alt.get("end_time")
            timestamps.append({"word": word, "start": start, "end": end})
    return timestamps
