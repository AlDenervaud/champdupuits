import os
import streamlit as st
import pandas as pd
#from fpdf import FPDF
from datetime import datetime, date

       
# Title of the Streamlit app
st.title("# :rainbow[Bienvenue au Champs du Puits]")

st.write("Sur ce site vous pourrez trouver la liste des produits de la ferme Au Champ du Puits, organisés par catégorie")
st.write("Les différentes catégories sont disponibles dans le menu à gauche")


image_url = "https://github.com/AlDenervaud/champdupuits/blob/main/data/images/pain_epices.jpg"
st.image(image_url, caption="test 1")

image_url = "data/images/pain_epices.jpg"
st.image(image_url, caption="test 2")

#from PIL import Image
#image_1=Image.open('online_education.jpg')
#st.image(image_1)
