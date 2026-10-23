def check_unsafe_words(texts, unsafe_terms=None):
    '''Simple keyword check on OCR or generated label texts for unsafe content.
    texts: list of strings
    unsafe_terms: optional list of prohibited words; defaults to a small built‑in list
    Returns a list of any matching terms found.
    '''
    if unsafe_terms is None:
        # Minimal hard‑coded list; in production this could be loaded from env or DB
        unsafe_terms = ['nudity', 'violence', 'drugs', 'hate', 'porn']
    found = []
    lower_texts = [txt.lower() for txt in texts]
    for term in unsafe_terms:
        if any(term in txt for txt in lower_texts):
            found.append(term)
    return found
