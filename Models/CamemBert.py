from sentence_transformers import SentenceTransformer, util
from Utils import Glossaire_CamemBert
from torch.nn.functional import cosine_similarity
from transformers import AutoTokenizer
## for data
import pandas as pd
import numpy as np
## for processing
import re
import nltk
## for w2v
import gensim
import gensim.downloader as gensim_api
from Utils import preprocess_text


from tqdm.autonotebook import tqdm
import re
import string
import nltk
from nltk.corpus import stopwords
import warnings
warnings.filterwarnings('ignore')



<<<<<<< HEAD
=======
def preprocess_text(text):
    text = text.lower()
    text = re.sub(r'\W', ' ', text)
    text = re.sub(r':[a-z_]+:', ' ', text)
    text = text.translate(str.maketrans('', '', string.punctuation))

    tokens = text.split()

    stop_words = set(stopwords.words('french'))
    tokens = [token for token in tokens if token not in stop_words]

    return ' '.join(tokens) 


max_length=1024
# Encoder les phrases de chaque catégorie
embeddings = {}
for category, sentences in categories.items():
    embeddings[category] = model.encode(sentences, convert_to_tensor=True,batch_size=1)



>>>>>>> abda6cd398796dcc296bc611c2f01de1d2fd847a
def CamemBertClassifier(input_file,model,tokenizer) : 

    max_length=1024
    # Encoder les phrases de chaque catégorie
    embeddings = {}
    for category, sentences in Glossaire_CamemBert.categories.items():
        embeddings[category] = model.encode(sentences, convert_to_tensor=True,batch_size=1)

    input_file = pd.read_csv(input_file, encoding='utf-8-sig', delimiter=';', header=0)
    input_file['Review_cleaned'] = input_file['Review'].apply(preprocess_text)


    for index, row in input_file.iterrows():
        review = row['Review_cleaned']

        # Tokenisation et limitation de la longueur
        tokens = tokenizer.tokenize(review)
        if len(tokens) > max_length:
            tokens = tokens[:max_length]

        review = tokenizer.convert_tokens_to_string(tokens)

        # Encoder la revue
        try:
            review_embedding = model.encode([review], convert_to_tensor=True)
        except Exception as e:
            print(f"Error at row {index}: {e}")
            continue

        max_similarity = -1  # Initialisez à une valeur très faible
        max_category = None

        # Parcourez chaque catégorie et chaque phrase dans chaque catégorie :
        for category, phrase_embeddings in embeddings.items():
            for phrase_embedding in phrase_embeddings:
                # Calculez la similarité cosinus entre l'embedding de la revue et l'embedding de la phrase :
                similarity = cosine_similarity(review_embedding, phrase_embedding)

                # Si cette similarité est plus grande que la similarité maximale actuelle, mettez à jour la similarité maximale et la catégorie maximale :
                if similarity > max_similarity:
                    max_similarity = similarity
                    max_category = category

        # À ce stade, max_category est la catégorie de la phrase avec la plus grande similarité à la revue.
        # Vous pouvez maintenant attribuer cette catégorie à la revue dans votre dataframe :
        input_file.at[index, 'Category'] = max_category

    input_file.to_csv("ClassifiedWith_CamemBert.csv", encoding='utf-8-sig',header=1,sep=';')
