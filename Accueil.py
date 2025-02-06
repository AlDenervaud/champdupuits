import os
import streamlit as st
import pandas as pd
       
# Title of the Streamlit app
st.title(":rainbow[Bienvenue au Champs du Puits]")

st.markdown("""Sur ce site vous pourrez trouver la liste des produits de la ferme Au Champ du Puits
 et créer un bon de commande à télécharger. Envoyez le bon de commande à l'adresse email ci-dessous, 
 nous tâcherons de vous répondre au plus vite!
 
 La liste est indicative uniquement et ne reflète pas l'état des stocks,
 il se peut que certains produits soient indisponibles.""")

st.markdown("### Contact")
st.markdown("GAEC Au Champ du Puits  \n211 chemin de la Fontaine  \n01430, Peyriat")

contact_list = """
email: lechampdupuits@gmail.com\n
"""

st.page_link("https://www.instagram.com/lechampdupuits/", label="Instagram", "icon"=👀)

st.markdown(contact_list)
