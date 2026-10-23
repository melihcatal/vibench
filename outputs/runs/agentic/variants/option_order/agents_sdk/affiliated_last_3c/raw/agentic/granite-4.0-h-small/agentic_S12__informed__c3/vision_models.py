def normalize_labels(response):
    """Converts Google Vision label annotation payload to a simple list of dicts."""
    items = []
    for ann in response.label_annotations:
        items.append({
            'name': ann.description,
            'score': float(ann.score),
            'mid': ann.mid,
        })
    return items


def normalize_description(response, max_results=1):
    """Extracts the best description from Vision's document text result."""
    text = response.full_text_annotation.text
    # Fallback if full text is empty, use the first detected text block
    if not text:
        for page in response.full_text_annotation.pages:
            for block in page.blocks:
                for paragraph in block.paragraphs:
                    for word in paragraph.words:
                        symbols = [s.symbol for s in word.symbols]
                        text += ''.join(symbols)
                break
        
    return [text[:500]] if text else []


def normalize_text_annot(response):
    """Normalizes text detection output to a list of dicts with content and confidence."""
    items = []
    for ann in response.text_annotations:
        items.append({
            'content': ann.description,
            'confidence': float(ann.locale),  # crude proxy - replace with proper confidence if needed
        })
    return items


def normalize_safe_results(response):
    """Normalizes safe-search annotation to a simple flag dict."""
    safe = response.safe_search_annotation
    return {
        'adult': safe.adult,
        'spoof': safe.spoof,
        'medical': safe.medical,
        'violence': safe.violence,
        'racy': safe.racy,
    }
