def image_summary(results):
    """Summarizes visual analysis results (labels, description, detected text) into a concise report."""
    lines = ['--- Image Analysis Summary ---']
    for labels in results.get('labels', []):
        lines.append(f'  Label: {labels.get("name")} (score {labels.get("score"):.2f})')
    if results.get('description'):
        lines.append(f'  Description: {results.get("description")[0]}')
    if results.get('text'):
        lines.extend([f'  OCR Text: {t.get("content")}' for t in results.get('text')])
    if results.get('safety'):
        safety = results['safety']
        lines.append('  Safety Flags:')
        lines.append(f'    Adult:      {safety.get("adult")}')
        lines.append(f'    Spoof:      {safety.get("spoof")}')
        lines.append(f'    Medical:    {safety.get("medical")}')
        lines.append(f'    Violence:   {safety.get("violence")}')
        lines.append(f'    Racy:       {safety.get("racy")}')
    return '\n'.join(lines)
