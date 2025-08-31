import spacy
import importlib
import emoji

nlp = spacy.load('en_core_web_sm')

def clean_text(text: str) -> str:
    text = emoji.replace_emoji(text, replace='')
    doc = nlp(str(text).lower())
    return ' '.join([token.lemma_ for token in doc if not token.is_stop and token.is_alpha])
