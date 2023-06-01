import pandas as pd
import streamlit as st
import analyser
import categoriser

import pandas as pd
import streamlit as st
import base64
import matplotlib.pyplot as plt
from PIL import Image
from preprocessing import preprocessing

import streamlit as st
from categoriser import run_categoriser
from analyser import run_analyser
import plotly.graph_objects as go
from categoriser import create_categories_dict



st.set_page_config(page_title="RED by SFR", layout="wide")




st.markdown(
    """
    <style>
    .stRadio > label {
        background-color: #40494b;
        color: white;
        border-radius: 10px;
        margin-right: 10px;
        margin-bottom: 10px;
        padding: 10px;
        text-align: center;
        cursor: pointer;
    }
    .stRadio > label:hover {
        background-color: #1a1a1a;
    }
    .stRadio > label.stSelected {
        background-color: #ff0000;
        font-weight: bold;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


st.markdown(
    """
    <style>
    [data-testid="stSidebar"][aria-expanded="true"] > div:first-child {
        background-color: #00e094	;
        border-top-right-radius: 30px;
        border-bottom-right-radius: 30px;
   
    }
    [data-testid="stSidebar"][aria-expanded="true"] > div:first-child > div {
        background-color: #00e094	;
        border-top-right-radius: 30px;
        border-bottom-right-radius: 30px;

    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.sidebar.markdown(
    """
    <style>
    .sidebar .sidebar-content {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
    }
    .sidebar .sidebar-content .stSelectbox {
        width: 100%;
        margin-bottom: 1rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)



# logo = Image.open("C:/Users/hp/Desktop/app/Customer.png")
# st.sidebar.image(logo, use_column_width=False)
st.sidebar.title("""Menu des opérations : """)


col1 , col2 = st.columns([1,3.1])
with col1 : 
    st.write('', unsafe_allow_html=True)
with col2 : 
    logo1 = Image.open("ANALYTICA (2).png")
    st.image(logo1, use_column_width=False)
    st.write('')
    st.write('')

col8 , col9, col10 = st.columns([1,7,1])
with col9 : 
    st.subheader("Bienvenue dans ANALYTICA ! \n \n  l'analyseur des avis clients de RED by SFR, une plateforme développée par E-Voluciona by intelcia.Cette plateforme a pour but de vous aider à mieux comprendre les avis et les retours de vos clients, en effectuant une catégorisation de leurs commentaires ainsi qu'une analyse de leurs sentiments.\n \n Grâce à notre technologie de pointe, nous sommes en mesure de catégoriser automatiquement les commentaires de vos clients en fonction de leur contenu et de leur contexte. Vous pouvez ainsi découvrir rapidement les sujets qui préoccupent le plus vos clients et prendre des mesures pour améliorer leur expérience.\n \n Nous sommes également capables de détecter les sentiments exprimés par vos clients dans leurs commentaires, en analysant non seulement leur texte, mais aussi leur note. Vous pouvez ainsi savoir si vos clients sont satisfaits, mécontents ou neutres vis-à-vis de votre entreprise, et agir en conséquence. \n \n Nous espérons que notre plateforme vous sera utile pour améliorer votre relation client et vous permettre de mieux répondre aux attentes de vos clients.")


# Define the expander for the 'Catégorisation des avis clients' mode
glossaire_expander = st.sidebar.expander("Glossaire référence des catégories", expanded=False)

# Agrandir le texte à l'aide de CSS
glossaire_expander.markdown("<h3 style='font-size: 30px;'>Glossaire :</h3>", unsafe_allow_html=True)
with glossaire_expander:
    st.write("Utilisez le bouton ci-dessous pour télécharger le fichier CSV contenant le glossaire.")
    uploaded_file3 = st.file_uploader("Chargez un fichier CSV", type="csv", key='input3')
    if uploaded_file3    is not None:
        st.header("Glossaire importé avec succès ! ")
        categories = create_categories_dict(uploaded_file3)





# Define the expander for the 'Catégorisation des avis clients' mode
categorisation_expander = st.sidebar.expander("Catégorisation des avis clients", expanded=False)

# Agrandir le texte à l'aide de CSS
categorisation_expander.markdown("<h3 style='font-size: 30px;'>Catégorisation des avis clients</h3>", unsafe_allow_html=True)
with categorisation_expander:
    st.write("Utilisez le bouton ci-dessous pour télécharger le fichier CSV contenant les avis clients à catégoriser.")
    uploaded_file1 = st.file_uploader("Chargez un fichier CSV", type="csv", key='input1')
if uploaded_file1 is not None:
    st.write('')
    st.write('')
    st.write('')
    st.header("Résultat de l'étiquetage des données :")
    run_categoriser(uploaded_file1 , categories)




# Define the expander for the 'Analyse des sentiments' mode
analyse_expander = st.sidebar.expander("Analyse des sentiments", expanded=False)

# Agrandir le texte en utilisant la fonction write avec une taille de police spécifiée
analyse_expander.write("<h3 style='font-size: 30px;'>Analyse des sentiments des avis clients</h3>", unsafe_allow_html=True)
with analyse_expander:
    st.subheader("Utilisez le bouton ci-dessous pour télécharger le fichier CSV contenant les avis clients à analyser.")
    uploaded_file2 = st.file_uploader("Chargez un fichier CSV", type="csv", key='input2')
if uploaded_file2 is not None:
    st.header("Résultat de l'analyse des sentiments des avis client :")
    run_analyser(uploaded_file2)






    




st.write("")
st.write("")
st.write("")
st.write("")
st.write("")
st.write("")
st.write("")
st.write("")
st.write("")
st.write("")
st.write("")
st.write("")
st.write("")
st.write("")
col1, col2, col3 = st.columns([5, 1, 5])
col2.image("evoluciona.png", width=3, use_column_width=True)
col1.write("")
col2.write("")
st.markdown(
                """
                <style>
                .footer {
                    text-align: right;
                }
                </style>
                """,
                unsafe_allow_html=True,
            )
st.write('<center>© 2023 RED by SFR. Tous droits réservés.<center>', unsafe_allow_html=True)





