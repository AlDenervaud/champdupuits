import os
import streamlit as st
import pandas as pd
#from fpdf import FPDF
from datetime import datetime, date

       
# Title of the Streamlit app
st.title(":rainbow[Bienvenue au Champs du Puits]")

st.write("Sur ce site vous pourrez trouver la liste des produits de la ferme Au Champ du Puits, organisés par catégorie")
st.write("Les différentes catégories sont disponibles dans le menu à gauche")


st.markdown("## Contact")
st.markdown("This is line 1.  \nThis is line 2.  \nThis is line 3.")
st.write("""<div>GAEC Au Champ du Puits<br>
211 chemin de la Fontaine<br>
01430, Peyriat</div>""")
contact_list = """
email: ...\n
Instagram: ...
"""
st.markdown(contact_list)

