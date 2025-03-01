import os
import streamlit as st
import pandas as pd
from streamlit_js_eval import streamlit_js_eval
# Custom
from pages.utils.helper import UpdateOrderFinal, GeneratePDF, ResetOrder
from pages.utils.helper import SendEmail


# Retrieve secrets
secrets_email = st.secrets["email"]
email_address = secrets_email["address"]
email_passkey = secrets_email["passkey"]


# Title of the Streamlit app
st.markdown("## Valider la commande")
st.markdown("""Vous pouvez télécharger le bon et nous l'envoyer à lechampdupuits@gmail.com.""")

try:
    order_df = st.session_state["order_df"]
    order_df["Quantité"] = order_df["Quantité"].apply(lambda x: str(float(x))) # -> does not show decimals
    #order_df["Quantité"] = order_df["Quantité"].astype(float) # -> 
    #xx = st.column_config.NumberColumn(
    #    "Quantité",
    #    help="Renseignez la quantité",
    #    format="%d",)

    show_dict = {"Nom":"Nom", "Prix":"Prix", "Catégorie":"Catégorie", "Quantité":"Quantité (en kg ou nombre d\'unités)", "Total":None}
    edited_order = st.data_editor(order_df, hide_index=True, disabled=[col for col in order_df if col != "Quantité"], column_config=show_dict)
    
    # Reset order button
    if st.button("Réinitialiser la commande"):
        ResetOrder()
    
    # Final preview before download
    st.markdown("#### Aperçu de la commande finale")
    edited_order["Quantité"] = edited_order["Quantité"].apply(lambda x: x.replace(",", "."))
    final_order = UpdateOrderFinal(edited_order)
    st.dataframe(final_order, hide_index=True, use_container_width=True)
    
    # Retrieve client's name
    client_name = st.text_input("Votre nom (appuyez sur entrée pour valider)", value="", placeholder="Veuillez entrer votre nom")
    note = st.text_input("Ajouter une remarque (appuyez sur entrée pour valider)", value="", placeholder="...")
    st.session_state["client_name"] = client_name
    
    # Generate PDF
    pdf_buffer = GeneratePDF(pd.DataFrame(final_order), client_name, note)

    # Embed PDF to display it:
    #base64_pdf = b64encode(gen_pdf()).decode("utf-8")
    #pdf_display = f'<embed src="data:application/pdf;base64,{base64_pdf}" width="700" height="400" type="application/pdf">'
    #st.markdown(pdf_display, unsafe_allow_html=True)

    # Download button
    if st.download_button(label="Télécharger le bon de commande",
                    type="primary",
                    data=pdf_buffer,
                    file_name="Commande_{}_{}.pdf".format(client_name.replace(" ", "_"), dt.now().strftime("%d%m%Y")),
                    mime="application/pdf"
                    ):
        pass
    
except Exception as e:
    if "st.session_state has no key \"order_df\"" in str(e):
        st.warning("Votre panier est vide")
    else:
        st.error("Error occured: {}".format(e))

    
