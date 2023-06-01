import pandas as pd
import streamlit as st
import base64
import matplotlib.pyplot as plt
from PIL import Image
# from preprocessing import preprocess_customer_feedback
import plotly.express as px
from datetime import datetime
import plotly.graph_objects as go
from Utils import preprocess_text






labels = {"Résiliation": ["resilié","résiliée","résiliation","resiliation","résilier"],
          "ImageDeMarque" : ["opérateur", "catastrophe", "voleur","menteur","fuir", "arnaque", "concurrent","orange","free","cette entreprise","fuyez","Commerciaux","Publicité", "mensongère",'satisfait'],
          "ServiceClient": [ "conseiller", "compétent","professionnalisme","chatbot","coup de fil","raccroché","raccroche","chat","messagerie","visuelle","vocale","répond","répondre","après vente","service après vente","rappeler","conseiller","incompétents","service clients","accueil","service client", "assistance", "hotline", "support", "aide", "conseiller", "conseil","sav","commercial","appelle","joindre","harcelement","Réception","service","Injoignable","rendez vous","client","Réception","reclame"],
          "Forfait/Offre": ["abonnement","annonces" ,"publicitaires","forfait","promo","promotion", "offre", "rabais", "réduction", "avantage", "bon plan", "code promo","abonnement","remise","inscription"],
          "Facturation": ["débitée","tarification","surfacturation","facturation","facture","débité", "paiement", "montant", "échéance", "remboursement","prélèvement", "tva","augmentation de prix",'Remboursez',"payer",'tarif',"facturé","remboursent"],
          "Débit/Internet": ["fibre","fibre optique","internet","vitesse", "débit", "connexion", "lenteur", "ralentissement", "instabilité", "buffering","déconnecte"],
          "Installation/ServiceTechnique": ["tech","rdv","rendez-vous","Service Technique","Technicien","installation", "paramétrage", "configuration", "réglage", "installation", "paramètre", "logiciel"],
          "Contrat": ["contrat","engagement", "durée", "renouvellement", "engager", "souscrire", "clause","contrats"],
          "Couverture/Réseau": ["coupure","couverture","réseau", "câble", "antenne", "télévision", "wifi", "téléphone", "signal"]}



def get_categories(row):
    text = row["Review"]
    
    # Prétraitement de la review
    processed_text = preprocess_text(text)
    
    category_votes = {}
    for category, keywords in labels.items():
        for keyword in keywords:
            if keyword in processed_text.lower():
                if category in category_votes:
                    category_votes[category] += 1
                else:
                    category_votes[category] = 1
    
    categories = sorted(category_votes, key=category_votes.get, reverse=True)[:3]
    categories = list(set(categories))
    if len(categories) == 3 and category_votes[categories[2]] == category_votes[categories[1]]:
        categories = categories[:2]
    
    row["Processed Review"] = processed_text
    row["Category1"] = categories[0] if len(categories) > 0 else ""
    row["Category2"] = categories[1] if len(categories) > 1 else ""
    row["Category3"] = categories[2] if len(categories) > 2 else ""
    
     # Téléchargement de l'output catégorisé au format CSV
    return row.to_csv(index=False, encoding='utf-8-sig', header=1, sep=";")








