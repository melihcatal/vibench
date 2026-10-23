import spacy


def extract_fields(text):
    nlp = spacy.load('en_core_web_sm')
    doc = nlp(text)
    fields = {
        'persons': [ent.text for ent in doc.ents if ent.label_ == 'PERSON'],
        'organizations': [ent.text for ent in doc.ents if ent.label_ == 'ORG'],
        'locations': [ent.text for ent in doc.ents if ent.label_ == 'GPE'],
    }
    return fields