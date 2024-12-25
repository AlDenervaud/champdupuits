import os
import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode
from st_aggrid.shared import JsCode

# Title of the Streamlit app
st.title("Liste des produits laitiers")

# Basic settings
root_dir = os.path.dirname(os.path.dirname(__file__))
#root_root_dir = os.path.dirname(os.path.dirname(root_dir))
products_file_path = os.path.join(root_dir, "products.xlsx")


# Get list of products
df = pd.read_excel(products_file_path, sheet_name="apiculture")

st.dataframe(df)

if False:
    # Function to convert image paths into HTML <img> tags
    def path_to_image_html(path):
        return f'<img src="{path}" width="60">'
    
    # Apply the HTML formatting
    products_df['Image'] = products_df['Image_Path'].apply(lambda x: f'<img src="{x}" width="100">')
    st.table(products_df)
    
    # Render HTML
    st.write(products_df.to_html(escape=False), unsafe_allow_html=True)


### Solution 2.0
gb = GridOptionsBuilder.from_dataframe(df, editable=True)

cell_renderer =  JsCode("""
                        function(params) {return `<a href=${params.value} target="_blank">${params.value}</a>`}
                        """)

thumbnail_renderer = JsCode("""
        class ThumbnailRenderer {
            init(params) {

            this.eGui = document.createElement('img');
            this.eGui.setAttribute('src', params.value);
            this.eGui.setAttribute('width', '100');
            this.eGui.setAttribute('height', 'auto');
            }
                getGui() {
                console.log(this.eGui);

                return this.eGui;
            }
        }
    """)

gb.configure_column(
    "Image",
    headerName="Image_Path",
    width=100,
    cellRenderer=thumbnail_renderer
)



#grid = AgGrid(df,
#            gridOptions=gb.build(),
#            updateMode=GridUpdateMode.VALUE_CHANGED,
#            allow_unsafe_jscode=True)

vgo = gb.build()
AgGrid(df, gridOptions=vgo, theme='streamlit', height=150, allow_unsafe_jscode=True )


if False:
    # Loop through the DataFrame to display images with corresponding names
    for index, row in products_df.iterrows():
        nom = row["Nom"]
        st.write(nom)
        st.write(row["Prix"])
        #st.image(row['Image_Path'], caption=nom)
        st.image("data/images/apiculture/pain_epices.jpg", caption="default")
