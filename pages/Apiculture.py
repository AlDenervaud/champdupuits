import os
import streamlit as st
import pandas as pd
#from fpdf import FPDF
#from datetime import datetime, date

# Title of the Streamlit app
st.title("Liste des produits laitiers")

# Basic settings
root_dir = os.path.dirname(os.path.dirname(__file__))
#root_root_dir = os.path.dirname(os.path.dirname(root_dir))
products_file_path = os.path.join(root_dir, "products.xlsx")


# Get list of products
products_df = pd.read_excel(products_file_path, sheet_name="apiculture")

st.dataframe(products_df)




# Function to convert image paths into HTML <img> tags
def path_to_image_html(path):
    return f'<img src="{path}" width="60">'

# Apply the HTML formatting
products_df['Image'] = products_df['Image_Path'].apply(lambda x: f'<img src="{x}" width="100">')
st.table(products_df)

# Render HTML
st.write(products_df.to_html(escape=False), unsafe_allow_html=True)


if False:
    # Loop through the DataFrame to display images with corresponding names
    for index, row in products_df.iterrows():
        st.write(f"**Nom:** {row['Nom']}")
        st.image(row['Image_Path'], caption=row['Nom'], use_column_width=True)
