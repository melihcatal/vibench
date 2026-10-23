import spacy

def extract_structured_fields(text):
    nlp = spacy.load('en_core_web_sm')
    doc = nlp(text)
    fields = {}
    for ent in doc.ents:
        fields[ent.label_] = ent.text
    return fields