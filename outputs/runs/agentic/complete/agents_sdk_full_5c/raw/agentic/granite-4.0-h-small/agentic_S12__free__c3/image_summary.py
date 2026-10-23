import json

def summarize_analysis(image_path, analyses):
    """Summarize the results of multiple image analyses into a concise report.
    analyses is a dict mapping analysis names to their result dicts.
    Returns a text summary.
    """
    summary_lines = [f"=== Analysis Summary for {image_path} ==="]
    result_counts = {}
    for name, result in analyses.items():
        result_counts[name] = len(result) if isinstance(result, list) else 1
        if name == "labels":
            top = result[:5]
            summary_lines.append(f"Top {len(top)} detected labels:")
            for lbl in top:
                summary_lines.append(f"  - {lbl['description']} (confidence {lbl['score']:.2f})")
        elif name == "extracted_text":
            summary_lines.append(f"Extracted text ({len(result)} pieces):")
            for line in result[:3]:
                summary_lines.append(f"  - {line}")
        elif name == "safe_search":
            ss = result
            summary_lines.append(f"Safety flags: adult={ss['isAdult']}, violent={ss['isViolent']}, racy={ss['isRacy']}" )
        else:
            summary_lines.append(f"{name} result: {result}")
    # Add overall count
    summary_lines.append(f"Counts: labels={result_counts.get('labels',0)}, text={result_counts.get('extracted_text',0)}, safety={result_counts.get('safe_search',0)}")
    return "\\n".join(summary_lines)
