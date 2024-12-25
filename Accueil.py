import os
import streamlit as st
import pandas as pd
#from fpdf import FPDF
from datetime import datetime, date

       
# Title of the Streamlit app
st.title("Liste des produits de la ferme Au Champ du Puits")

# Basic settings
root_dir = os.path.dirname(__file__)
products_file_path = os.path.join(root_dir, "products.xlsx")


# Get list of products
products_df = pd.read_excel(products_file_path, sheet_name="products")


st.dataframe(products_df)

st.table(products_df)
