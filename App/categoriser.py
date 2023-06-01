import pandas as pd
import streamlit as st
import base64
import matplotlib.pyplot as plt
from PIL import Image
from preprocessing import preprocessing
import plotly.express as px
from datetime import datetime
import plotly.graph_objects as go
from wordcloud import WordCloud
import matplotlib.pyplot as plt



# labels = {"Résiliation": ["resilié","résiliée","résiliation","resiliation","résilier"],
#           "ImageDeMarque" : ["opérateur", "catastrophe", "voleur","menteur","fuir", "arnaque", "concurrent","orange","free","cette entreprise","fuyez","Commerciaux","Publicité", "mensongère",'satisfait'],
#           "ServiceClient": [ "conseiller", "compétent","professionnalisme","chatbot","coup de fil","raccroché","raccroche","chat","messagerie","visuelle","vocale","répond","répondre","après vente","service après vente","rappeler","conseiller","incompétents","service clients","accueil","service client", "assistance", "hotline", "support", "aide", "conseiller", "conseil","sav","commercial","appelle","joindre","harcelement","Réception","service","Injoignable","rendez vous","client","Réception","reclame"],
#           "Forfait/Offre": ["abonnement","annonces" ,"publicitaires","forfait","promo","promotion", "offre", "rabais", "réduction", "avantage", "bon plan", "code promo","abonnement","remise","inscription"],
#           "Facturation": ["débitée","tarification","surfacturation","facturation","facture","débité", "paiement", "montant", "échéance", "remboursement","prélèvement", "tva","augmentation de prix",'Remboursez',"payer",'tarif',"facturé","remboursent"],
#           "Débit/Internet": ["fibre","fibre optique","internet","vitesse", "débit", "connexion", "lenteur", "ralentissement", "instabilité", "buffering","déconnecte"],
#           "Installation/ServiceTechnique": ["tech","rdv","rendez-vous","Service Technique","Technicien","installation", "paramétrage", "configuration", "réglage", "installation", "paramètre", "logiciel"],
#           "Contrat": ["contrat","engagement", "durée", "renouvellement", "engager", "souscrire", "clause","contrats"],
#           "Couverture/Réseau": ["coupure","couverture","réseau", "câble", "antenne", "télévision", "wifi", "téléphone", "signal"]}


import nltk
from nltk.corpus import stopwords

nltk.download('stopwords')
stop_words = set(stopwords.words('french'))  # Modify 'english' if you're using a different language

def remove_stop_words(text):
    tokens = text.split()
    filtered_tokens = [token for token in tokens if token.lower() not in stop_words]
    return " ".join(filtered_tokens)

# def get_categories(row):
#     text = row["Review"]
    
#     # Prétraitement de la review
#     processed_text = preprocess_customer_feedback(text)
    
#     category_votes = {}
#     for category, keywords in labels.items():
#         for keyword in keywords:
#             if keyword in processed_text:
#                 if category in category_votes:
#                     category_votes[category] += 1
#                 else:
#                     category_votes[category] = 1
    
#     categories = sorted(category_votes, key=category_votes.get, reverse=True)[:3]
#     categories = list(set(categories))
#     if len(categories) == 3 and category_votes[categories[2]] == category_votes[categories[1]]:
#         categories = categories[:2]
    
#     row["Processed Review"] = processed_text
#     row["Category1"] = categories[0] if len(categories) > 0 else ""
#     row["Category2"] = categories[1] if len(categories) > 1 else ""
#     row["Category3"] = categories[2] if len(categories) > 2 else ""
    
#     return row


def create_categories_dict(csv_file):
    # Lire le fichier CSV avec pandas
    df = pd.read_csv(csv_file, encoding='utf-8-sig', delimiter=';')

    # Créer un dictionnaire pour stocker les catégories et les phrases
    categories = {}

    # Boucler sur les colonnes du DataFrame
    for column in df.columns:
        # Boucler sur les lignes de chaque colonne
        categories[column] = df[column].dropna().tolist()

    return categories

def get_categories(row, labels):
    text = row["Review"]
    
    processed_text = preprocessing(text)
    
    category_votes = {}
    for category, keywords in labels.items():
        for keyword in keywords:
            if keyword in processed_text:
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
    
    return row




def run_categoriser(uploaded_file,categories):
    if uploaded_file is not None:
        try:
            # df = pd.read_csv(uploaded_file, encoding='utf-8-sig', delimiter=';', header=0)
            # df = df.apply(get_categories, axis=1)
            # df['Date'] = pd.to_datetime(df['Date'])
            df = pd.read_csv(uploaded_file, encoding='utf-8-sig', delimiter=';', header=0)
            df = df.apply(get_categories, args=(categories,), axis=1)
            df['Date'] = pd.to_datetime(df['Date'])

            # Créer un widget de sélection de date pour filtrer les données
            date_range = st.date_input("Sélectionnez une plage de dates", [df['Date'].min().date(), df['Date'].max().date()], key='date_categorizer')
            date_range = [datetime.combine(date, datetime.min.time()) for date in date_range]
            mask = (df['Date'] >= date_range[0]) & (df['Date'] <= date_range[1])
            df = df.loc[mask]

            # Créer un widget de sélection de rating pour filtrer les données
            min_rating, max_rating = st.slider("Filtrer par rating", float(df['Rating'].min()), float(df['Rating'].max()), (float(df['Rating'].min()), float(df['Rating'].max())))
            rating_mask = (df['Rating'] >= min_rating) & (df['Rating'] <= max_rating)
            df = df.loc[rating_mask]

            # Créer un widget de sélection de catégorie pour filtrer les données
            selected_categories = st.multiselect("Filtrer par catégorie", df['Category1'].unique())
            category_mask = df['Category1'].isin(selected_categories)
            df = df.loc[category_mask]

            # Vérifier si les données sont disponibles après le filtrage
            if df.empty:
                st.warning("Aucune donnée disponible pour les filtres sélectionnés.")
                return

            # Affichage des données catégorisées
            with st.expander("Quelques statistiques sur les catégories dominantes"):
                col1, col2 = st.columns(2)

                with col1 : 
                    category_counts = df["Category1"].value_counts().sort_values(ascending=False)
                    category_table = pd.DataFrame(category_counts).reset_index()
                    category_table.columns = ['Catégorie', 'Nombre de revues']
                    st.write(category_table.style.set_table_styles([{'selector': 'th', 'props': [('max-width', '500px')]}]))

                with col2 : 
                    # Preprocess the reviews and remove stop words
                    df["Processed Review"] = df["Review"].apply(preprocessing)
                    df["Processed Review"] = df["Processed Review"].apply(remove_stop_words)
                    
                    # Create a word cloud of the preprocessed reviews
                    all_reviews = " ".join(df["Processed Review"])
                    
                    # Set the background color for the word cloud
                    background_color = "#000000"  # Light gray
                    
                    # Create the word cloud with the specified background color
                    wordcloud = WordCloud(
                        width=1200,
                        height=600,
                        background_color=background_color
                    ).generate(all_reviews)
                    
                    # Display the word cloud in Streamlit
                    st.write("Nuage de mots de toutes les critiques de catégories choisies.")
                    st.image(wordcloud.to_array(), use_column_width=True)

            # Création d'un graphique en barres horizontales pour afficher le nombre de revues par catégorie
            col1, col2 = st.columns([1,5])


            with col1:
                st.write('')

            with col2:
                # Rééchantillonnage des données par mois
                df_time = df.resample('M', on='Date')['Rating'].mean()

                # Création d'un graphique en courbes pour afficher les moyennes des ratings par date
                fig2 = px.line(
                    x=df_time.index,
                    y=df_time.values,
                    labels={
                        'x': 'Date',
                        'y': 'Moyenne des ratings par date'
                
                },
                title='Moyenne des ratings par date'
                )
                fig2.update_xaxes(tickangle=45)
                st.plotly_chart(fig2)

                        # Création d'un graphique en barres horizontales pour afficher le nombre de revues par catégorie
            col3, col4 = st.columns([1,5])


            with col4:
                category_counts = df["Category1"].value_counts().sort_values(ascending=False)
                fig1 = px.bar(
                    y=category_counts.index,
                    x=category_counts.values,
                    orientation='h',
                    color=category_counts.index,
                    color_discrete_sequence=px.colors.qualitative.Pastel,
                    labels={
                        'y': 'Catégorie',
                        'x': 'Nombre de revues'
                    },
                    title='Nombre de revues par catégorie'
                )
                fig1.update_layout(xaxis={'categoryorder': 'total ascending'})
                st.plotly_chart(fig1,use_column_width=True)

            with col3:
                st.write('')
        

        except Exception as e:
            st.error(f"Une erreur s'est produite : {str(e)}")
        
    else:
        st.warning("Veuillez télécharger un fichier CSV pour commencer l'analyse.")


        
  # Téléchargement de l'output catégorisé au format CSV
    csv = df.to_csv(index=False, encoding='utf-8-sig', header=1, sep=";")
    b64 = base64.b64encode(csv.encode(encoding='utf-8-sig')).decode(encoding='utf-8-sig')
    href = f'<a href="data:file/csv;base64,{b64}" download="categorized_data.csv">Download CSV File</a>'
    if st.button("Télécharger les résultats", key='button_categorizer', use_container_width=True):
        st.markdown(f"<div style='text-align: center;'>{href}</div>", unsafe_allow_html=True)







