import streamlit as st
import pandas as pd
import numpy as np
from st_aggrid import AgGrid, GridOptionsBuilder, JsCode
#from streamlit.components.v1 import html
import streamlit as st
import streamlit.components.v1 as components
components.html("PASID")
def nav_page(page_name, timeout_secs=1000):
    """
    From https://github.com/streamlit/streamlit/issues/4832, on Jan 4, 2023

    """
    nav_script = """
        <script type="text/javascript">
            function attempt_nav_page(page_name, start_time, timeout_secs) {
                var links = window.parent.document.getElementsByTagName("a");
                for (var i = 0; i < links.length; i++) {
                    if (links[i].href.endsWith("/" + page_name)) {
                        links[i].click();
                        return;
                    }
                }
                var elasped = new Date() - start_time;
                if (elasped < timeout_secs * 1000) {
                    setTimeout(attempt_nav_page, 100, page_name, start_time, timeout_secs);
                } else {
                    alert("Unable to navigate to page '" + page_name + "' after " + timeout_secs + " second(s).");
                }
            }
            window.addEventListener("load", function() {
                attempt_nav_page("%s", new Date(), %d);
            });
        </script>
    """ % (page_name, timeout_secs)
    st._main._html(nav_script)

# st.set_page_config(
#     page_title="PASID",
#     page_icon="🧬",
#     layout="centered",
#     initial_sidebar_state="expanded")

title = '''
<p style="font-family: sans-serif; text-align: center; color:#5E2750; font-size: 40px;">
    Welcome to PASID:<br>
    <strong>P</strong>seudomonas <strong>A</strong>eruginosa<br>
    <strong>S</strong>tructural <strong>I</strong>nformation <strong>D</strong>atabase
</p>
'''


st.markdown(title, unsafe_allow_html=True)

st.text("")
st.text("")
st.text("")


col1, col2 = st.columns(2)
with col1:
    if st.button("PPInt for Pseudomonas Aeruginosa", key="ppint_button"):
        nav_page("PPInt_for_Pseudomonas_Aeruginosa")
    m = st.markdown("""
    <style>
    .stButton > button {
        background-color: #77216F;
        border-radius: 20px;
        border: 1px solid #772953;
        height: 5rem;
        width: 100%; /* Use relative width to adjust with the layout */
        font-size: 20px; /* Adjust font size to fit within the button */
        cursor: pointer;
        color: white;
        font-family: sans-serif;
        font-weight: bold;
        text-align: center;
        display: flex; /* Use flexbox for centering content */
        align-items: center;
        justify-content: center;
    }
    </style>
""", unsafe_allow_html=True)

with col2:
    if st.button("Mimicry for Pseudomonas Aeruginosa", key="mimicry_button"):
        nav_page("Mimicry_for_Pseudomonas_Aeruginosa")

    m = st.markdown("""
    <style>
    .stButton > button {
        background-color: #77216F;
        border-radius: 20px;
        border: 1px solid #772953;
        height: 5rem;
        width: 100%; /* Use relative width to adjust with the layout */
        font-size: 20px; /* Adjust font size to fit within the button */
        cursor: pointer;
        color: white;
        font-family: sans-serif;
        font-weight: bold;
        text-align: center;
        display: flex; /* Use flexbox for centering content */
        align-items: center;
        justify-content: center;
    }
    </style>
""", unsafe_allow_html=True)


welcome_text = '<p style="font-family: sans-serif; text-align: justify; color:#2C001E; font-size: 15px;">' \
            'Welcome to our website, where we provide comprehensive insights into both the structural ' \
            'interfaces of biofilm-related proteins of Pseudomonas aeruginosa and their mimicry of human proteins. ' \
            'Our platform features two dedicated modules: the first explores the detailed protein structure interfaces ' \
            'associated with these biofilm proteins, while the second investigates the mechanisms by which these proteins ' \
            'mimic human proteins. We aim to advance your understanding of these complex biological systems and invite you ' \
            'to delve into our resources for a deeper appreciation of these interactions. </p>'



st.markdown(welcome_text, unsafe_allow_html=True)

info_text = '<p style="font-family: sans-serif; text-align: center; color:#77216F; font-size: 12px;">For more information about how to use this website, please visit User Guide Page in the navigation panel.</p>'
st.markdown(info_text, unsafe_allow_html=True)