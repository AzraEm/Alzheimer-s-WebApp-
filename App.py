import streamlit as st
import json
import requests
from requests_oauthlib import OAuth2Session
from dem_tab import alzheimers_app
from history_tab import history_tab_ui

TITLE = "Alzheimer's App"
IMAGE_CAPTION = "Let's track Alzheimer's!"
CSS_STYLE = """ 
<style>
.login-button {
            padding: 10px;
            border-radius: 5px;
            background-color: blue;
            color: white;
            border: none;
            margin-bottom: 20px;
   }

.login-button: hover {
            color: black;
        }
</style>
"""

LOGIN_IMAGE = "https://kffhealthnews.org/wp-content/uploads/sites/2/2020/02/Dementia-resized.png?w=1024"
SIGN_IN_IMAGE = "https://beconnected.esafety.gov.au/pluginfile.php/82020/mod_resource/content/1/t35_c4_a2_p1.png"
LOG_OUT_URL = "https://adhdhistory-u2cko4dyvncvkr7whryxg8.streamlit.app/"

st.markdown(CSS_STYLE, unsafe_allow_html=True)








