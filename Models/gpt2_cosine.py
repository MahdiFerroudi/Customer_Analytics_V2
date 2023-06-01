import re
import string
import nltk
from nltk.corpus import stopwords
import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from transformers import AutoTokenizer, TFAutoModel
import transformers as trf
import torch
import gc
from Utils import Glossaire_gpt2





# Charger le modèle GPT-2 pré-entraîné
tokenizer = AutoTokenizer.from_pretrained("DohaData/gpt2-base-french-finetuned")
model = TFAutoModel.from_pretrained("DohaData/gpt2-base-french-finetuned",from_pt=True)

def preprocess_text(text):
    text = text.lower()
    text = re.sub(r'\W', ' ', text)
    text = re.sub(r':[a-z_]+:', ' ', text)
    text = text.translate(str.maketrans('', '', string.punctuation))

    tokens = text.split()

    stop_words = set(stopwords.words('french'))
    tokens = [token for token in tokens if token not in stop_words]

    return ' '.join(tokens)

def gpt2_embedding(txt):
    idx = tokenizer.encode(txt, max_length=1024, truncation=True)
    if len(idx) >= 1024:
        return None
    idx = np.array(idx)[None, :]

    emb = model(torch.tensor(idx))[0]
    hidden = np.array(emb[0])

    sent_emb = hidden.mean(0)
    return sent_emb


from tqdm.autonotebook import tqdm


def preproc_calculate_cosine_similarity(input_data):

    input_embeddings = np.array([gpt2_embedding(text) for text in tqdm(input_data['Review_cleaned'][0:300])] , dtype=object)
    IMAGE_MARQUE = [preprocess_text(text) for text in Glossaire_gpt2.image_de_marque]
    SERVICE_CLI = [preprocess_text(text) for text in Glossaire_gpt2.service_client]
    FORFAIT_OFFRE = [preprocess_text(text) for text in Glossaire_gpt2.forfait_offre]
    FACTURATION = [preprocess_text(text) for text in Glossaire_gpt2.facturation]
    DEBIT_INTERNET = [preprocess_text(text) for text in Glossaire_gpt2.debit_internet]
    INSTALLATION_SERVICE_TECHNIQUE = [preprocess_text(text) for text in Glossaire_gpt2.installation_service_technique]
    CONTRAT = [preprocess_text(text) for text in Glossaire_gpt2.contrat]
    COUVERTURE_RESEAU = [preprocess_text(text) for text in Glossaire_gpt2.couverture_reseau]

    import numpy as np

    IMAGE_MARQUE = np.array([gpt2_embedding(text) for text in Glossaire_gpt2.image_de_marque])
    SERVICE_CLI = np.array([gpt2_embedding(text) for text in Glossaire_gpt2.service_client])
    FORFAIT_OFFRE = np.array([gpt2_embedding(text) for text in Glossaire_gpt2.forfait_offre])
    FACTURATION = np.array([gpt2_embedding(text) for text in Glossaire_gpt2.facturation])
    DEBIT_INTERNET = np.array([gpt2_embedding(text) for text in Glossaire_gpt2.debit_internet])
    INSTALLATION_SERVICE_TECHNIQUE = np.array([gpt2_embedding(text) for text in Glossaire_gpt2.installation_service_technique])
    CONTRAT = np.array([gpt2_embedding(text) for text in Glossaire_gpt2.contrat])
    COUVERTURE_RESEAU = np.array([gpt2_embedding(text) for text in Glossaire_gpt2.ouverture_reseau])

    input_embeddings = np.array([gpt2_embedding(text) for text in tqdm(input_data['Review_cleaned'][0:300])] , dtype=object)
    from sklearn.metrics.pairwise import cosine_similarity
    import pandas as pd

    # Calcul des scores de similarité cosinus pour chaque catégorie
    IMAGE_MARQUE_MEAN = IMAGE_MARQUE.mean(0)[None,:]
    SERVICE_CLI_MEAN = SERVICE_CLI.mean(0)[None,:]
    FORFAIT_OFFRE_MEAN = FORFAIT_OFFRE.mean(0)[None,:]
    FACTURATION_MEAN = FACTURATION.mean(0)[None,:]
    DEBIT_INTERNET_MEAN = DEBIT_INTERNET.mean(0)[None,:]
    INSTALLATION_SERVICE_TECHNIQUE_MEAN = INSTALLATION_SERVICE_TECHNIQUE.mean(0)[None,:]
    CONTRAT_MEAN = CONTRAT.mean(0)[None,:]
    COUVERTURE_RESEAU_MEAN = COUVERTURE_RESEAU.mean(0)[None,:]

    # Création du DataFrame pour stocker les scores de similarité
    cosine_score = pd.DataFrame()
    cosine_score['id'] = range(len(input_embeddings))
    cosine_score['Image de marque'] = cosine_similarity(input_embeddings, IMAGE_MARQUE_MEAN)
    cosine_score['Service client'] = cosine_similarity(input_embeddings, SERVICE_CLI_MEAN)
    cosine_score['Forfait/Offre'] = cosine_similarity(input_embeddings, FORFAIT_OFFRE_MEAN)
    cosine_score['Facturation'] = cosine_similarity(input_embeddings, FACTURATION_MEAN)
    cosine_score['Débit/Internet'] = cosine_similarity(input_embeddings, DEBIT_INTERNET_MEAN)
    cosine_score['Installation/Service technique'] = cosine_similarity(input_embeddings, INSTALLATION_SERVICE_TECHNIQUE_MEAN)
    cosine_score['Contrat'] = cosine_similarity(input_embeddings, CONTRAT_MEAN)
    cosine_score['Couverture/Réseau'] = cosine_similarity(input_embeddings, COUVERTURE_RESEAU_MEAN)

    # Trouver les trois catégories les plus similaires pour chaque phrase
    top3_categories = cosine_score[['Image de marque', 'Service client', 'Forfait/Offre', 'Facturation', 'Débit/Internet', 'Installation/Service technique', 'Contrat', 'Couverture/Réseau']].apply(lambda x: x.nlargest(3).index.tolist(), axis=1)

    # Ajouter les colonnes au DataFrame
    cosine_score['Category'] = top3_categories.apply(lambda x: x[0])
    cosine_score['Category2'] = top3_categories.apply(lambda x: x[1] if len(x)>1 else None)
    cosine_score['Category3'] = top3_categories.apply(lambda x: x[2] if len(x)>2 else None)

    df = cosine_score
    del cosine_score #deleting as we dont need this df anymore
    gc.collect()
    df['Review'] = input_data['Review'][0:300] #Earlier we have defined num_sentences
    df.drop(['Image de marque', 'Service client', 'Forfait/Offre', 'Facturation', 'Débit/Internet', 'Installation/Service technique', 'Contrat', 'Couverture/Réseau'],axis=1,inplace =True) 
    df1 = df[['id','Review','Category','Category2','Category3']]

    return df1



def preproc_calculate_cosine_similarity(input_df):

    # Prétraitement de l'entrée
    input_df['Review_cleaned'] = input_df['Review'].apply(preprocess_text)

    # Calcul de similarité cosinus
    similarity_scores = preproc_calculate_cosine_similarity(input_df)

    # Enregistrer les résultats dans un fichier CSV
    similarity_scores.to_csv('Resultats_GPT2_COSINE.csv', index=False, encoding='utf-8-sig',header=1,sep=';')



