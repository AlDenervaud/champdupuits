import math
import pandas as pd
from PIL import Image
from datetime import datetime as dt
from streamlit_js_eval import streamlit_js_eval
# Specific to PDF
from io import BytesIO
from fpdf import FPDF
# Specific to email
import smtplib
import ssl
import streamlit as st
from email.message import EmailMessage

# Retrieve secrets
secrets_email = st.secrets["email"]
email_address = secrets_email["address"]
email_passkey = secrets_email["passkey"]

def config_page(page_name="", page_icon=None):
    """ Sets the app page name """
    if page_icon:
        image = Image.open(page_icon)
    else:
        image = None
    PAGE_CONFIG = {"page_title":page_name, 
                   "page_icon":image,
                   "layout":"wide",#"centered", 
                   "initial_sidebar_state":"auto"}
    st.set_page_config(**PAGE_CONFIG)


def customize_css():
    """
    Injects custom CSS to enable full screen width
    """    
    st.markdown("""
        <style>
        /* Center content horizontally and align to the top */
        .main .block-container {
            max-width: 2500px;  /* Adjust width as needed */
            margin: 50 auto;    /* Center horizontally */
            padding-top: 50px; /* Adjust top padding for spacing */
            text-align: center; /* Center text */
        }
        .subtitle {
            font-size: 1.1rem;  /* matches Streamlit's H4 */
            font-weight: 600;
            color: #264653; /* #2c3e50 #264653 */
            background-color: #a8dadc;
            border-radius: 12px;
            padding: 10px;
        }
        .forecast {
            font-size: 1.1rem;  /* matches Streamlit's H4 */
            font-weight: 600;
            color: #912F2F;
            color: #912F2F;
            background-color: #f4cccc;
            border-radius: 12px;
            padding: 10px;
        }
        .blurred-text {
            color: transparent;
            text-shadow: 0 0 8px rgba(0, 0, 0, 0.5);
            user-select: none;
            filter: blur(3px);
            transition: filter 0.1s ease;
        }
        </style>
    """, unsafe_allow_html=True)


def SendEmail(receiver, subject, body):
    msg = EmailMessage()
    msg.set_content(body)
    msg["Subject"] = subject
    msg["From"] = email_address
    msg["To"] = receiver

    # Send email using SMTP
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=ssl.create_default_context()) as server:
            server.login(email_address, email_passkey)
            server.send_message(msg)
        st.success(f"Email sent successfully to {receiver}!")
    except Exception as e:
        st.error(f"Error sending email: {e}")
        
        
# Function to send an email with an attachment
def SendEmailPDF(receiver, subject, body, pdf_path):
    msg = EmailMessage()
    msg.set_content(body)
    msg["Subject"] = subject
    msg["From"] = email_address
    msg["To"] = receiver

    # Attach PDF file
    with open(pdf_path, "rb") as f:
        pdf_data = f.read()
        msg.add_attachment(pdf_data, maintype="application", subtype="pdf", filename="attachment.pdf")

    # Send email using SMTP
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=ssl.create_default_context()) as server:
            server.login(email_address, email_passkey)
            server.send_message(msg)
        st.success(f"Email sent successfully to {receiver}!")
    except Exception as e:
        st.error(f"Error sending email: {e}")


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
            if row["name"] == "":
                pdf.cell(product_width+price_width+quantity_width, cell_height, txt="", border=0)
                pdf.cell(total_width, cell_height, txt=row["total"], border=1, align="C", fill=False)
            else:
                pdf.cell(product_width, cell_height, txt=row["name"], border=1, align="C", fill=True)
                pdf.cell(price_width, cell_height, txt=str(row["price"]), border=1, align="C", fill=False)
                #pdf.cell(category_width, cell_height, txt=str(row["Categorie"]), border=1, align="C", fill=True)
                pdf.cell(quantity_width, cell_height, txt=str(row["quantity"]), border=1, align="C", fill=False)
                pdf.cell(total_width, cell_height, txt=row["total"], border=1, align="C", fill=False)
            pdf.ln()
    
    # Get unique categories
    categories = df["category"].unique()
    for category in categories:
        
        sub_df = df[df["category"]==category]
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
    if note != "":
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

def ResetOrder():
    """reloads the page to empty selection"""
    streamlit_js_eval(js_expressions="parent.window.location.reload()")
    return


def UpdateOrderFinal(order):
    # Reset Total column
    if "total" in order.columns:
        order.drop("total", axis=1, inplace=True)
    # Remove row with grand total
    order = order[order["name"].str.strip() != ""]
    
    # Updates total price based on price and quantity (round quantity)
    order["price_temp"] = order["price"].apply(lambda x: float(x.split(" ")[0].replace(",", ".")))
    order["quantity"] = order["quantity"].apply(lambda x: x.replace(",", "."))
    order["quantity"] = pd.to_numeric(order["quantity"], errors='coerce')
    order["quantity"] = order.apply(lambda row: math.floor(row["quantity"]) if row["units"]=="€" else round(row["quantity"], 1), axis=1)
    order["total"] = order["price_temp"] * order["quantity"]
    
    # Remove items with 0 quantity
    order = order[order["quantity"] != 0]
    
    # Add grand total
    order = order._append({"name":"", "price":"", "category":"", "quantity":"", "total":order["total"].sum()}, ignore_index=True)
    order["total"] = order["total"].apply(lambda x: "{:.2f} €".format(x))

    # Cleaning
    final_order = order[['name', 'price', 'category', 'quantity', 'total']]

    return final_order
