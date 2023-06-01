import re
from nltk.corpus import stopwords
import string

def preprocess_text(text):
    text = text.lower()
    text = re.sub(r'\W', ' ', text)
    text = re.sub(r':[a-z_]+:', ' ', text)
    text = text.translate(str.maketrans('', '', string.punctuation))

    tokens = text.split()

    stop_words = set(stopwords.words('french'))
    tokens = [token for token in tokens if token not in stop_words]

    return ' '.join(tokens)