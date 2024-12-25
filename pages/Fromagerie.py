import os
import streamlit as st
import pandas as pd
from fpdf import FPDF
from datetime import datetime, date

# Title of the Streamlit app
st.title("Liste des produits laitiers")

# Basic settings
root_dir = os.path.dirname(os.path.dirname(__file__))
#root_root_dir = os.path.dirname(os.path.dirname(root_dir))
products_file_path = os.path.join(root_dir, "products.xlsx")


# Get list of products
products_df = pd.read_excel(products_file_path, sheet_name="fromagerie")

st.dataframe(products_df)