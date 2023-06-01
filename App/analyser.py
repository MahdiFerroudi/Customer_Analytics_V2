import pandas as pd
import streamlit as st
import base64
import matplotlib.pyplot as plt
from PIL import Image
from preprocessing import preprocessing
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime



sentiment_keywords = {
            "positif": [
                "heureux","excellent", "rapide", "bon", "super", "efficace", "convivial", "aimé", "recommande", "parfait", "bonne qualité", "bon service", "prix abordable",
                "satisfait", "meilleur", "bonne couverture", "bonne connexion", "bonne assistance", "support réactif", "service clientèle compétent", "service fiable","stable","remarquable","content","aimable","fiable","flexibilité","impressionnante","impressionné","agréablement","formidable","merci","compétent","facile","soulagement","transparente","transparence","transparent"
            ],
            "négatif": [
                "incompétent","autre opérateur","Orange","voleurs","mal poli","chantage","mal","galère","pitoyable","ne recommande","désagréable","lamentable","mauvaise","insatisfaite","Déconseille","déficient","incompétent","Incapable","mépris","dégoutée","incompétent","fuyez","malhonnete","galères","honte","catastrophe","fuir","pire","mécontent","déçu", "mauvais", "lent", "cher", "coûteux", "horrible", "désagréable", "incompétent", "service médiocre", "mauvaise qualité", "mauvaise couverture",
                "a fuire","nul","mauvaise connexion", "mauvaise assistance", "service clientèle inutile", "problème", "erreur", "difficulté", "détesté", "arnaque"
                ,"sans prévenir","aucune réponse","éviter","insupportables","injoignables","injoignable","inexacte","médiocre","aucun service","malheureusement"
                ,"dommage ","effronté","sans consentement","mensonge","malhonnêteté","injoignable","escroquerie","raccroche","incompetent","lamentable","sans accord"
                ,"scandaleux","escrocs","sans consentement","inacceptable","emmerdes","surfacturation","inacceptable","désastreux","imbecile","mensonge","mensonges"
                ,"regretté","chaotique","incapables","incapable","inadmissible","minable","bye","inadmissible","consentement","surfacturation","injustifiée","déconseille"
                ,"forcée","bandits","retardé","fraudes","fraude","agressé","agression","horreur","difficile","incompétence","impossible","absurde","trompeuse","mensongère","absente"
            ]
        }


def preprocess_labels(labels_dict):
    preprocessed_labels = {}
    for key, value_list in labels_dict.items():
        preprocessed_values = [preprocessing(value) for value in value_list]
        preprocessed_labels[key] = preprocessed_values
    return preprocessed_labels

labels = preprocess_labels(sentiment_keywords)



def get_sentiments(row):
    text = row["Review"]
    # Prétraitement de la review
    processed_text = preprocessing(text)
    rating = row["Rating"]
    
    sentiment_votes = {}
    for sentiment, keywords in sentiment_keywords.items():
        for keyword in keywords:
            if keyword in processed_text.lower():
                if sentiment in sentiment_votes:
                    sentiment_votes[sentiment] += 1
                else:
                    sentiment_votes[sentiment] = 1
    
    if sentiment_votes:
        sentiment = max(sentiment_votes, key=sentiment_votes.get)
    else:
        sentiment = "Neutre"

    if sentiment == "Positif" or rating in [4, 5]:
        return "Positif"
    elif sentiment == "Négatif" and rating in [1, 2]:
        return "Négatif"
    elif rating == 3:
        return "Neutre"
    else:
        return "Négatif"
    



    


# def run_analyser(file):

#     # Chargement du fichier CSV
#     df = pd.read_csv(file, encoding='utf-8-sig', delimiter=';', header=0)

#     # Application de la fonction get_sentiments à chaque ligne du fichier
#     df['Sentiment'] = df.apply(get_sentiments, axis=1)

#     # Conversion de la colonne "Date" en format datetime
#     df["Date"] = pd.to_datetime(df["Date"])

#     # Création d'une nouvelle colonne "year" qui contient l'année correspondante
#     df["year"] = df["Date"].dt.year

#     # Créez un widget de sélection de date pour filtrer les données
#     date_range = st.date_input("Sélectionnez une plage de dates", [df['Date'].min().date(), df['Date'].max().date()], key='date_analyser')

#     # Convert the date objects to datetime objects
#     date_range = [datetime.combine(date, datetime.min.time()) for date in date_range]

#     # Filtrer les données en fonction de la plage de dates sélectionnée
#     mask = (df['Date'] >= date_range[0]) & (df['Date'] <= date_range[1])
#     df = df.loc[mask]

#     sentiments_per_year = df.groupby(['year', 'Sentiment'])['Sentiment'].count().unstack().fillna(0)
#     # Calcul de la moyenne des ratings pour chaque catégorie
#     mean_ratings = df.groupby("Category1")["Rating"].mean()

#     # Calcul de la moyenne des ratings pour chaque catégorie
#     mean_ratings = df.groupby("Category1")["Rating"].mean()
#     mean_ratings = mean_ratings.reset_index()


#     # Create a 2x2 layout
#     col5, col6 = st.columns(2)
#     col1, col2 = st.columns(2)
#     col3, col4 = st.columns(2)

#     # First chart
#     with col5:
#         grouped_df = df.groupby('Sentiment')

#         positif_df = grouped_df.get_group('Positif').head(2)
#         negatif_df = grouped_df.get_group('Négatif').head(2)
#         neutre_df = grouped_df.get_group('Neutre').head(2)

#         positif_df=positif_df[['Review', 'Rating','Sentiment']]
#         negatif_df=negatif_df[['Review', 'Rating', 'Sentiment']]
#         neutre_df=neutre_df[['Review', 'Rating', 'Sentiment']]

#         st.write('Avis positifs :')
#         st.write(positif_df)
#         st.write('Avis négatifs :')
#         st.write(negatif_df)
#         st.write('Avis neutres :')
#         st.write(neutre_df)



#         sentiment_counts = df['Sentiment'].value_counts(normalize=True)
#         st.write(sentiment_counts , use_container_width=1)

#     # Second chart
#     with col6:
#         fig2 = px.pie(
#         names=sentiment_counts.index,
#         values=sentiment_counts.values,
#         hole=0.5,
#         color_discrete_sequence=px.colors.qualitative.Set2,
#         labels={"Sentiment": "Proportion"}
#         )
#         st.plotly_chart(fig2)


#     # First chart
#     with col1:
#         fig1 = px.line(mean_ratings, x="Category1", y="Rating", title="Moyenne des ratings par catégorie")
#         fig1.update_layout(xaxis_tickangle=-45)
#         st.plotly_chart(fig1)

#     # Second chart
#     with col2:
#         # Calculer la moyenne des notes par sentiment
#         avg_rating_by_sentiment = df.groupby("Sentiment")["Rating"].mean()

#         # Créer le graphique en nuage de points
#         fig = go.Figure()

#         fig.add_trace(
#             go.Scatter(
#                 x=avg_rating_by_sentiment.index,
#                 y=avg_rating_by_sentiment.values,
#                 mode="markers",
#                 marker=dict(size=10),
#             )
#         )

#         # Mise en forme du graphique
#         fig.update_layout(
#             title="Moyenne des notes par sentiment",
#             xaxis_title="Sentiments",
#             yaxis_title="Moyenne des notes",
#         )

#         # Affichage du graphique
#         st.plotly_chart(fig)

#     # Third chart
#     with col3:

#         # Assurez-vous que 'Date' est de type datetime
#         df['Date'] = pd.to_datetime(df['Date'])

#         # Group by date and sentiment, then unstack to get a column for each sentiment
#         sentiment_counts = df.groupby(['Date', 'Sentiment']).size().unstack(fill_value=0)

#         # Assurez-vous que votre DataFrame est trié par date
#         sentiment_counts.sort_index(inplace=True)

#         # Créez un graphique avec Plotly
#         fig = go.Figure()

#         # Ajoutez une trace pour chaque sentiment
#         for sentiment in sentiment_counts.columns:
#             fig.add_trace(
#                 go.Scatter(
#                     x=sentiment_counts.index,
#                     y=sentiment_counts[sentiment],
#                     mode='lines',
#                     name=sentiment
#                 )
#             )

#         fig.update_layout(
#             title='Fréquence des sentiments en fonction du temps',
#             xaxis_title='Date',
#             yaxis_title='Nombre de revues',
#         )

#         # Affichez le graphique avec Streamlit
#         st.plotly_chart(fig)




#     # Fourth chart (Replace with your fourth chart)
#     with col4:
#         # Grouper les données par catégorie et par sentiment
#         sentiments_by_category = df.groupby(["Category1", "Sentiment"])["Sentiment"].count().unstack().fillna(0)

#         # Créer le graphique à barres empilées
#         fig = go.Figure()

#         for sentiment in sentiments_by_category.columns:
#             fig.add_trace(
#                 go.Bar(
#                     y=sentiments_by_category.index,
#                     x=sentiments_by_category[sentiment],
#                     name=sentiment,
#                     orientation="h",
#                 )
#             )

#         # Mise en forme du graphique
#         fig.update_layout(
#             title="Nombre de revues par catégorie et par sentiment",
#             xaxis_title="Nombre de revues",
#             yaxis_title="Catégories",
#             barmode="stack",
#         )

#         # Affichage du graphique
#         st.plotly_chart(fig)
#         pass


#     # Téléchargement de l'output catégorisé au format CSV
#     csv = df.to_csv(index=False,encoding='utf-8-sig', header=1,sep=";")
#     b64 = base64.b64encode(csv.encode(encoding='utf-8-sig')).decode(encoding='utf-8-sig')
#     href = f'<a href="data:file/csv;base64,{b64}" download="categorized_data.csv">Download CSV File</a>'
#     if st.button("Télécharger les résultats", key='button_analyser' , use_container_width=1):
#         st.markdown(f"<div style='text-align: center;'>{href}</div>", unsafe_allow_html=True)


def run_analyser(file):
    
    if file is not None:
        try:
        # Chargement du fichier CSV
            df = pd.read_csv(file, encoding='utf-8-sig', delimiter=';', header=0)
            df['Sentiment'] = df.apply(get_sentiments, axis=1)
            df['Date'] = pd.to_datetime(df['Date'])
            df["year"] = df["Date"].dt.year

            # Créer un widget de sélection de date pour filtrer les données
            date_range = st.date_input("Sélectionnez une plage de dates", [df['Date'].min().date(), df['Date'].max().date()], key='date_analyser')
            date_range = [datetime.combine(date, datetime.min.time()) for date in date_range]

            # Filtrer les données en fonction de la plage de dates sélectionnée
            mask = (df['Date'] >= date_range[0]) & (df['Date'] <= date_range[1])
            df = df.loc[mask]

            # Créer un widget de sélection de rating pour filtrer les données
            min_rating, max_rating = st.slider("Filtrer par rating", float(df['Rating'].min()), float(df['Rating'].max()), (float(df['Rating'].min()), float(df['Rating'].max())), key='slider1')
            rating_mask = (df['Rating'] >= min_rating) & (df['Rating'] <= max_rating)
            df = df.loc[rating_mask]

            # Créer un widget de sélection de catégorie pour filtrer les données
            selected_categories = st.multiselect("Filtrer par catégorie", df['Category1'].unique())
            category_mask = df['Category1'].isin(selected_categories)
            df = df.loc[category_mask]

            # First chart
            # First chart

            # First chart
            col1, col2 = st.columns(2)
            with col1:
                grouped_df = df.groupby('Sentiment')
                
                sentiment_labels = ['Positif', 'Négatif', 'Neutre']
                
                for sentiment_label in sentiment_labels:
                    if sentiment_label in grouped_df.groups:
                        st.write(f'Avis {sentiment_label}s:')
                        sentiment_df = grouped_df.get_group(sentiment_label).head(2)
                        st.write(sentiment_df[['Review', 'Category1']])
                    else:
                        st.write(f'Aucun avis {sentiment_label} trouvé.')
                
                sentiment_counts = df['Sentiment'].value_counts(normalize=True)
                st.write(sentiment_counts, use_container_width=True)

            # Second chart
            with col2:
                fig2 = px.pie(
                    names=sentiment_counts.index,
                    values=sentiment_counts.values,
                    hole=0.5,
                    color_discrete_sequence=px.colors.qualitative.Set2,
                    labels={"Sentiment": "Proportion"}
                )
                st.plotly_chart(fig2)


            # Third chart
            col3, col4 = st.columns(2)
            with col3:
                mean_ratings = df.groupby("Category1")["Rating"].mean()
                fig1 = px.line(mean_ratings, x=mean_ratings.index, y=mean_ratings.values,labels={
                    "x": "Catégorie",
                    "y": "Moyenne des ratings"
                }, title="Moyenne des ratings par catégorie")
                fig1.update_layout(xaxis_tickangle=-45)

                # Set y-axis range
                fig1.update_layout(yaxis_range=[mean_ratings.min(), mean_ratings.max()])

                st.plotly_chart(fig1)


            # Fourth chart
            with col4:
                avg_rating_by_sentiment = df.groupby("Sentiment")["Rating"].mean()
                fig = go.Figure()
                fig.add_trace(
                    go.Scatter(
                        x=avg_rating_by_sentiment.index,
                        y=avg_rating_by_sentiment.values,
                        mode="markers",
                        marker=dict(size=10),
                    )
                )
                fig.update_layout(
                    title="Moyenne des notes par sentiment",
                    xaxis_title="Sentiments",
                    yaxis_title="Moyenne des notes",
                )
                st.plotly_chart(fig)

            # Fifth chart
            col5, col6 = st.columns(2)
            with col5:
                sentiment_counts = df.groupby(['Date', 'Sentiment']).size().unstack(fill_value=0)
                sentiment_counts.sort_index(inplace=True)
                fig = go.Figure()
                for sentiment in sentiment_counts.columns:
                    fig.add_trace(
                        go.Scatter(
                            x=sentiment_counts.index,
                            y=sentiment_counts[sentiment],
                            mode='lines',
                            name=sentiment
                        )
                    )
                fig.update_layout(
                    title='Fréquence des sentiments en fonction du temps',
                    xaxis_title='Date',
                    yaxis_title='Nombre de revues',
                )
                st.plotly_chart(fig)

            # Sixth chart
            with col6:
                sentiments_by_category = df.groupby(["Category1", "Sentiment"])["Sentiment"].count().unstack().fillna(0)
                fig = go.Figure()
                for sentiment in sentiments_by_category.columns:
                    fig.add_trace(
                        go.Bar(
                            x=sentiments_by_category[sentiment],
                            y=sentiments_by_category.index,
                            name=sentiment,
                            orientation="h",
                        )
                    )
                fig.update_layout(
                    title="Nombre de revues par catégorie et par sentiment",
                    xaxis_title="Nombre de revues",
                    yaxis_title="Catégories",
                    barmode="stack",
                )
                st.plotly_chart(fig)
            

        except Exception as e:
            st.error(f"Une erreur s'est produite : {str(e)}")
            


    # Téléchargement de l'output catégorisé au format CSV
    csv = df.to_csv(index=False, encoding='utf-8-sig', header=1, sep=";")
    b64 = base64.b64encode(csv.encode(encoding='utf-8-sig')).decode(encoding='utf-8-sig')
    href = f'<a href="data:file/csv;base64,{b64}" download="categorized_data.csv">Download CSV File</a>'
    if st.button("Télécharger les résultats", key='button_analyser', use_container_width=True):
        st.markdown(f"<div style='text-align: center;'>{href}</div>", unsafe_allow_html=True)










