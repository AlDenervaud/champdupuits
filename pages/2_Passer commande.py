import os
import streamlit as st
import pandas as pd
from datetime import datetime as dt
from streamlit_js_eval import streamlit_js_eval
# Report
from io import BytesIO
from fpdf import FPDF
# Custom
from utils.helper import test


def UpdateOrderFinal(order):
    # Reset Total column
    if "Total" in order.columns:
        order.drop("Total", axis=1, inplace=True)
    # Remove row with grand total
    order = order[order["Nom"].str.strip() != ""]
    
    # Updates total price based on price and quantity
    order["price_temp"] = order["Prix"].apply(lambda x: float(x.split(" ")[0].replace(",", ".")))
    order["Quantité"] = pd.to_numeric(order["Quantité"], errors='coerce')
    order["Total"] = order["price_temp"] * order["Quantité"]
    
    # Remove items with 0 quantity
    order = order[order["Quantité"] != 0]
    
    # Add grand total
    order = order._append({"Nom":"", "Prix":"", "Catégorie":"", "Quantité":"", "Total":order["Total"].sum()}, ignore_index=True)
    order["Total"] = order["Total"].apply(lambda x: "{:.2f} €".format(x))

    # Cleaning
    final_order = order[['Nom', 'Prix', 'Catégorie', 'Quantité', 'Total']]

    return final_order

def ResetOrder():
    """Empties the order dataframe"""
    try:
        st.session_state["order_df"] = None
        st.toast("Commande effacée avec succès")
    except Exception as e:
        st.error("Erreur dans la suppression de la commande: {}".format(e))
    streamlit_js_eval(js_expressions="parent.window.location.reload()")
    return


def GeneratePDF(df, client_name, note):
    # https://stackoverflow.com/questions/35668219/how-to-set-up-a-custom-font-with-custom-path-to-matplotlib-global-font/43647344#43647344
    
    # Create a PDF
    pdf = FPDF()
    pdf.add_page()

    uni_font = True
    if uni_font:
        font_path = "data/fonts/Arial Unicode MS Regular.ttf"
        pdf.add_font("Arial_unicode", '', font_path, uni=True)
        font = "Arial_unicode"
    else:
        font = "Arial"
    
    # PDF settings
    pdf.set_left_margin(20)
    pdf.set_right_margin(30)
    pdf.set_top_margin(30)
    linebreak_height = 10
    # Table
    cell_height = 10
    product_width = 70
    price_width = 30
    category_width = 25
    quantity_width = 25
    total_width = 30
    
    # Add title
    pdf.set_font(font, "", size=20)
    pdf.cell(170, 10, txt="Bon de commande", ln=True, align="C")
    pdf.cell(170, 10, txt="GAEC Champ du Puits", ln=True, align="C")
    pdf.ln(30)
    pdf.set_font(font, size=12)
    
    # Add details
    pdf.cell(200, linebreak_height, txt="Client: {}".format(client_name), ln=True, align="L")
    pdf.cell(200, linebreak_height, txt="Date de création: {}".format(dt.now().strftime("%d/%m/%Y %H:%M")), ln=True, align="L")
    
    # Add table header
    pdf.ln(20)
    #pdf.set_fill_color(200, 220, 255)
    pdf.set_fill_color(224, 224, 224)
    pdf.cell(product_width, cell_height, txt="Produit", border=1, align="C", fill=True)
    pdf.cell(price_width, cell_height, txt="Prix unitaire", border=1, align="C", fill=True)
    #pdf.cell(category_width, cell_height, txt="Catégorie", border=1, align="C", fill=True)
    pdf.cell(quantity_width, cell_height, txt="Quantité", border=1, align="C", fill=True)
    pdf.cell(total_width, cell_height, txt="Prix total", border=1, align="C", fill=True)
    pdf.set_fill_color(255, 255, 255)
    pdf.ln()
    
    # Add table rows
    def add_table_rows(df):
        for index, row in df.iterrows():
            if row["Nom"] == "":
                pdf.cell(product_width+price_width+quantity_width, cell_height, txt="", border=0)
                pdf.cell(total_width, cell_height, txt=row["Total"], border=1, align="C", fill=False)
            else:
                pdf.cell(product_width, cell_height, txt=row["Nom"], border=1, align="C", fill=True)
                pdf.cell(price_width, cell_height, txt=str(row["Prix"]), border=1, align="C", fill=False)
                #pdf.cell(category_width, cell_height, txt=str(row["Categorie"]), border=1, align="C", fill=True)
                pdf.cell(quantity_width, cell_height, txt=str(row["Quantité"]), border=1, align="C", fill=False)
                pdf.cell(total_width, cell_height, txt=row["Total"], border=1, align="C", fill=False)
            pdf.ln()
    
    # Get unique categories
    categories = df["Catégorie"].unique()
    for category in categories:
        
        sub_df = df[df["Catégorie"]==category]
        if category.lower() == "apiculture":
            pdf.set_fill_color(255, 255, 204)
        elif category.lower() == "fromagerie":
            pdf.set_fill_color(255, 255, 255)
        elif category.lower() == "viande":
            pdf.set_fill_color(255, 204, 229)
        else:
            pdf.set_fill_color(255, 255, 255)
        pdf.cell(200, linebreak_height, txt="{}".format(category), ln=True, align="L", fill=False)
        add_table_rows(sub_df)

    # Add note
    pdf.cell(200, linebreak_height, txt="Remarque", ln=True, align="L", fill=False)
    pdf.cell(200, linebreak_height, txt=note, ln=True, align="L", fill=False)

    if False: # works locally only
        pdf_output = BytesIO()
        pdf.output(pdf_output)
        pdf_output.seek(0)
        return pdf_output
    else:
        pdf_output = pdf.output(dest='S').encode('latin1')
        return pdf_output

import smtplib
import ssl
from email.message import EmailMessage

# Function to send an email with an attachment
def send_email(receiver, subject, body, pdf_path):
    msg = EmailMessage()
    msg.set_content(body)
    msg["Subject"] = subject
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = receiver

    # Attach PDF file
    with open(pdf_path, "rb") as f:
        pdf_data = f.read()
        msg.add_attachment(pdf_data, maintype="application", subtype="pdf", filename="attachment.pdf")

    # Send email using SMTP
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=ssl.create_default_context()) as server:
            server.login(EMAIL_ADDRESS, EMAIL_PASSKEY)
            server.send_message(msg)
        st.success(f"Email sent successfully to {receiver}!")
    except Exception as e:
        st.error(f"Error sending email: {e}")
    


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

    
