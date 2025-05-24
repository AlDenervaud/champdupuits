import streamlit as st
from PIL import Image
logo_path = r"C:\ALDE\Programs\Streamlit\InvestWatch\media\InvestWatch.ico"


def config_page(page_name="", page_icon=None):
    """  """
    page_name = " - {}".format(page_name) if page_name != "" else page_name
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