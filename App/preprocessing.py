import re
import re
import string
import nltk
from nltk.corpus import stopwords


def preprocessing(text):
    # Convertir en minuscules
    text = text.lower()

    # Supprimer les caractères spéciaux et les emojis
#     text = emoji.demojize(text)
    text = re.sub(r'\W', ' ', text)
    text = re.sub(r':[a-z_]+:', ' ', text)

    # Supprimer la ponctuation
    text = text.translate(str.maketrans('', '', string.punctuation))

    # Tokenisation
    tokens = text.split()

    # Supprimer les stopwords
    stop_words = set(stopwords.words('french'))
    tokens = [token for token in tokens if token not in stop_words]

    return ' '.join(tokens)