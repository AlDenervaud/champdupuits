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