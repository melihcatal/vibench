def normalize_job_id(job):
    if isinstance(job, dict):
        return job.get('job_id') or job.get('self') or job.get('id')
    return job


def normalize_transcript(data):
    if isinstance(data, dict):
        if 'combinedRecognizedPhrases' in data:
            return [item.get('display') or item.get('lexical') or '' for item in data.get('combinedRecognizedPhrases', [])]
        if 'results' in data:
            return [item.get('text') or item.get('display') or '' for item in data.get('results', [])]
        if 'transcript' in data:
            return data['transcript']
    return data


def extract_segments(data):
    if isinstance(data, dict):
        if 'combinedRecognizedPhrases' in data:
            return data.get('combinedRecognizedPhrases', [])
        if 'segments' in data:
            return data.get('segments', [])
        if 'results' in data:
            return data.get('results', [])
    return []


def extract_words(data):
    words = []
    for segment in extract_segments(data):
        for word in segment.get('words', []):
            words.append(word)
    return words
