import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder, DataReturnMode
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

# Sample DataFrame
data = {
    "Name": ["Alice", "Bob", "Charlie", "David"],
    "Age": [24, 27, 22, 32],
    "Occupation": ["Engineer", "Doctor", "Artist", "Teacher"]
}
df = pd.DataFrame(data)

# Streamlit app
st.title("Row Selection with AgGrid and PDF Export")

# Display dataframe with AgGrid
options_builder = GridOptionsBuilder.from_dataframe(df)
options_builder.configure_selection('multiple', use_checkbox=True)
grid_options = options_builder.build()

grid_response = AgGrid(
    df,
    gridOptions=grid_options,
    data_return_mode=DataReturnMode.FILTERED_AND_SORTED,
    update_mode='SELECTION_CHANGED',
    allow_unsafe_jscode=True,
)

selected_rows = grid_response['selected_rows']

# Display selected rows as a new dataframe
#st.write(type(selected_rows))
try:
    if selected_rows:
        pass
    else:
        st.write("Select rows to display them here.")
except:
    selected_df = pd.DataFrame(selected_rows)  # Properly create DataFrame from list of dicts
    selected_df["quantity"] = [1 for i in range(selected_df.shape[0])]
    st.write("Selected Rows:")
    command = st.data_editor(selected_df)


# PDF generation function
def generate_pdf(dataframe):
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    c.drawString(100, 750, "Selected Rows Data")
    
    # Add dataframe content to PDF
    y_position = 720
    for _, row in dataframe.iterrows():
        line = " | ".join(f"{col}: {row[col]}" for col in dataframe.columns)
        c.drawString(100, y_position, line)
        y_position -= 20
        if y_position < 40:  # Simple page break logic
            c.showPage()
            y_position = 750
    c.save()
    
    buffer.seek(0)
    return buffer

# Button to generate and download PDF
if st.button("Validater la sélection"):
    try:
        if command is not None:
            st.write(command)
            pdf_buffer = generate_pdf(pd.DataFrame(command))
            st.download_button(
                label="Télécharger le bon de commande",
                data=pdf_buffer,
                file_name="Commande.pdf",
                mime="application/pdf"
            )
        else:
            st.error("La sélection est vide!")
    except ValueError as va:
        st.fail("Error: {}".format(va))


# Retrieve data from session state
if "command_df" in st.session_state:
    saved_df = st.session_state["command_df"]
    st.write("Data retrieved from session state:")
    st.dataframe(saved_df)
else:
    st.write("No data found in session state.")