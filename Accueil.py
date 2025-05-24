import os
import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime as dt
# Grid display
#Grid view
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode, DataReturnMode
from st_aggrid.shared import JsCode, ColumnsAutoSizeMode

from bin import utils
from pages.utils.helper import UpdateOrderFinal, ResetOrder
from pages.utils.helper import GeneratePDF, SendEmail

# Retrieve secrets
secrets_email = st.secrets["email"]
email_address = secrets_email["address"]
email_passkey = secrets_email["passkey"]
email_receiver = secrets_email["receiver"]


utils.config_page(page_name="🐮")
utils.customize_css()
       
# Title of the Streamlit app
st.title(":rainbow[Bienvenue au Champ du Puits]")

st.markdown("""Sur ce site vous pourrez trouver la liste des produits de la ferme Au Champ du Puits
 et créer un bon de commande à télécharger. Envoyez le bon de commande à l'adresse email ci-dessous, 
 nous tâcherons de vous répondre au plus vite!
 
 La liste est indicative uniquement et ne reflète pas l'état des stocks,
 il se peut que certains produits soient indisponibles.""")
 
st.info("""Dans le tableau ci-dessous, cochez les produits que vous souhaitez commander et
    indiquez les quantités voulues en nombre d'unités ou en poids (kg).""",
    icon="✍️")
 
###############################################################################

# Basic settings
root_dir = os.path.dirname(__file__)
products_file_path = os.path.join(root_dir, "products.xlsx")

# Get list of products
df = pd.read_excel(products_file_path, sheet_name="products")
df["price"] = df.apply(lambda row: "{} {}".format(row["price"], row["units"]), axis=1)
df.insert(0, "quantity", "0")
df.insert(0, "select", False)


# Column configs
image_conf = st.column_config.ImageColumn(label="Photo", width="medium", help="Photo non contractuelle")
select_conf = st.column_config.CheckboxColumn(label="Commander")
# Choose which column are editable
active_cols = ["select", "quantity"]
disabled_cols = [col for col in df.columns if col not in active_cols]

selected_rows = st.data_editor(
                                df,
                                column_config={
                                                "name":"Nom",
                                                "price":"Prix",
                                                "units":None,
                                                "select":select_conf,
                                                "quantity":"Quantité",
                                                "category":None,
                                                "image_path":image_conf,
                                                },
                                hide_index = True,
                                disabled = disabled_cols,
                                row_height=100,
                            )


# Extract selected rows from grid
order = selected_rows[selected_rows["select"]]

# Proceed only if at least one row selected
if order.shape[0]>0:

    # Update prices
    final_order = UpdateOrderFinal(order)
    
    # Preview
    st.markdown("""#### Aperçu""")
    st.data_editor(
                    final_order,
                    column_config={
                                    "name":"Nom",
                                    "price":"Prix",
                                    "category":None,
                                    "quantity":"Quantité",
                                    "total":"Total",
                                    },
                    hide_index = True,
                    disabled = final_order.columns,
                )
    
    # Retrieve client's name
    client_name = st.text_input("Votre nom (appuyez sur entrée pour valider)", value="", placeholder="Veuillez entrer votre nom")
    note = st.text_input("Optionnel: ajouter une remarque (appuyez sur entrée pour valider)", value="", placeholder="...")
    st.session_state["client_name"] = client_name
    
    c1, c2 = st.columns([1,2])
    # Reset order button
    if c1.button("Réinitialiser la commande"):
        ResetOrder()
        
    # Proceed to PDF generation / download only if a name has been provided
    if client_name != "":
        # Generate PDF
        pdf_buffer = GeneratePDF(pd.DataFrame(final_order), client_name, note)
        
        # Download button - PDF need to be generated before
        if c2.download_button(label="Télécharger le bon de commande",
                        type="primary",
                        data=pdf_buffer,
                        file_name="Commande_{}_{}.pdf".format(client_name.replace(" ", "_"), dt.now().strftime("%d%m%Y")),
                        mime="application/pdf"
                        ):
            pass
    else:
        st.warning("Veuillez entrer votre nom avant de pouvoir télécharger le bon de commande")
    
    if client_name == "admin":
        if st.button("Send Email"):
            #receiver = #"lechampdupuits@gmail.com"
            receiver = email_receiver
            subject = "Commande de la part de {}".format(client_name)
            body = "Test"
            if receiver and subject and body and pdf_buffer:
                SendEmail(receiver, subject, body)
            else:
                st.warning("Please fill in all fields.")
    



###############################################################################

st.markdown("### Contact")
st.markdown("GAEC Au Champ du Puits  \n211 chemin de la Fontaine  \n01430, Peyriat")

st.markdown('<a href="mailto:lechampdupuits@gmail.com">lechampdupuits@gmail.com</a>', unsafe_allow_html=True)
st.page_link("https://www.instagram.com/lechampdupuits/", label="-> Instagram <-")

