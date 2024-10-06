import streamlit as st
import json
import requests
from requests_oauthlib import OAuth2Session

from dem_tab import dementia_app
from history_tab import history_tab_ui


TITLE = "BrainLex Analyzer"
IMAGE_CAPTION = "Let's track Alzheimer's!"
CSS_STYLE = """
    <style>
        body {
            font-family: 'Poppins', sans-serif;
            background-color: #fef5e7;
        }
        .login-button {
            padding: 12px 18px;
            border-radius: 12px;
            background: linear-gradient(135deg, #c3aed6, #ffe3e3);
            color: white;
            border: none;
            font-size: 16px;
            transition: transform 0.2s ease, background-color 0.3s ease;
        }
        .login-button:hover {
            background-color: #a4ebf3;
            transform: translateY(-3px);
            box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.2);
        }
        h1, h2, h3 {
            font-family: 'Nunito', sans-serif;
            color: #3d3d3d;
        }
        h1 {
            font-size: 36px;
            animation: gradient-text 3s infinite ease;
        }
        .title-text {
            font-size: 30px;
            font-weight: bold;
            color: #5a5a5a;
        }
        .highlight {
            color: #ffe3e3;
        }
        .history-section {
            box-shadow: 0px 4px 15px rgba(0, 0, 0, 0.1);
            border-radius: 10px;
            padding: 20px;
            background-color: #ffffff;
        }

        @keyframes gradient-text {
            0% {
                background-position: 0% 50%;
            }
            100% {
                background-position: 100% 50%;
            }
        }
    </style>
"""
LOGO_PLACEHOLDER = "https://via.placeholder.com/150?text=Your+Logo+Here"
LOGIN_IMAGE = "https://kffhealthnews.org/wp-content/uploads/sites/2/2020/02/Dementia-resized.png?w=1024"
SIGNIN_IMAGE = "https://upload.wikimedia.org/wikipedia/commons/thumb/2/2f/Google_2015_logo.svg/2560px-Google_2015_logo.svg.png"
# you have to change with the deployment
LOGOUT_URL = "https://fxn4qbs5wygh8lzfmgfpuy.streamlit.app/"

# set css styles
st.markdown(CSS_STYLE, unsafe_allow_html=True)

# Google OAuth2 credentials
client_id = st.secrets["CLIENT_ID"]
client_secret = st.secrets["CLIENT_SECRET"]
# you have to change with the deployment
redirect_uri = "https://fxn4qbs5wygh8lzfmgfpuy.streamlit.app"

# OAuth endpoints
authorization_base_url = "https://accounts.google.com/o/oauth2/auth"
token_url = "https://oauth2.googleapis.com/token"

# Scopes
scope = [
    "https://www.googleapis.com/auth/userinfo.email",
    "https://www.googleapis.com/auth/userinfo.profile",
]


def exchange_code_for_token(code):
    token_url = "https://oauth2.googleapis.com/token"
    # Prepare the data for the token request
    data = {
        "code": code,
        "client_id": client_id,
        "client_secret": client_secret,
        "redirect_uri": redirect_uri,
        "grant_type": "authorization_code",
    }
    # Make a POST request to the token endpoint
    response = requests.post(token_url, data=data)
    response_data = response.json()
    # Handle possible errors
    if response.status_code != 200:
        raise Exception(
            "Failed to retrieve token: " + response_data.get("error_description", "")
        )
    return response_data["access_token"]


def get_user_info(access_token):
    user_info_url = "https://www.googleapis.com/oauth2/v3/userinfo"
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(user_info_url, headers=headers)
    user_info = response.json()
    # Handle possible errors
    if response.status_code != 200:
        raise Exception(
            "Failed to retrieve user info: " + user_info.get("error_description", "")
        )
    return user_info


if "oauth_state" not in st.session_state:
    st.session_state.oauth_state = None

if "oauth_token" not in st.session_state:
    st.session_state.oauth_token = None

if "user_id" not in st.session_state:
    st.session_state.user_id = None

if "user_name" not in st.session_state:
    st.session_state.user_name = None


if st.session_state.oauth_token:
    with st.sidebar:
        st.title("Log Out")
        st.image(SIGNIN_IMAGE, caption="Log Out")
        if st.button("Log Out"):
            st.session_state.oauth_token = None
            # set login button
            st.write(
                f"""
            <a target="_self" href="{LOGOUT_URL}">
                <button class = 'login-button'>
                    Confirm
                </button>
            </a>
            """,
                unsafe_allow_html=True,
            )

    # set title and image
    st.title(TITLE)
    st.image(LOGIN_IMAGE, caption=IMAGE_CAPTION)

    dementia_app_tracker, history = st.tabs(["Text Analyzer", "History"])

    with dementia_app_tracker:
        dementia_app()

    with history:
        history_tab_ui()

else:
    oauth2_session = OAuth2Session(client_id, redirect_uri=redirect_uri, scope=scope)
    authorization_url, state = oauth2_session.authorization_url(
        authorization_base_url, access_type="offline"
    )

    if st.session_state.oauth_state is None:
        st.session_state.oauth_state = state

    # set the sign in page
    st.title(TITLE)
    st.image(LOGIN_IMAGE, caption = "Let's Track Dementia")
    st.markdown("""Alzheimer’s Disease is a progressive brain disorder that causes cognitive decline, such as 
memory loss and the inability complete simply daily tasks, that results in a decline in quality of life. According to 
the Alzheimer’s Association, nearly 7 million people are affected in the U.S., and many more will be effected in the future 
as the aging population increases worldwide. Alzheimer’s Disease has no cure; however, with early intervention, it is possible
 to alleviate the side effects and better manage symptoms. Unfortunately, it is rarely diagnosed early on because the symptoms 
are mild at the beginning and so, are usually attributed to other factors, like stress. BrainLex Analyzer introduces a novel 
way to detect Alzheimer’s Disease using Natural Language Processing techniques based on provided text input by *you*.""")
    
    # sign in
    st.subheader("Please Sign In with Google to Continue 📲")
    with st.sidebar:
        st.subheader("Please Sign In")
        st.image(SIGNIN_IMAGE, caption = "")
        st.write(
            f"""
        <a target="_blank" href="{authorization_url}">
            <button class = 'login-button'>
                Sign In
            </button>
        </a>
        """,
            unsafe_allow_html=True,
        )

    authorization_response = st.query_params

    if "code" in authorization_response:
        st.session_state.oauth_token = exchange_code_for_token(
            authorization_response["code"]
        )
        user_info = get_user_info(st.session_state.oauth_token)
        # set session states
        st.session_state.user_id = user_info["sub"]
        st.session_state.user_name = user_info["name"]

        # ui
        with st.sidebar:
            st.subheader("Hi! {} 👋".format(user_info["name"]))
            st.subheader("Welcome to BrainLex Analyzer!")
            st.write("**Name**: {}".format(user_info["name"]))
            st.write("**Email**: {}".format(user_info["email"]))

            st.subheader("Login Successful! Please Click on Continue")
            if st.button("Continue"):
                st.toast("Login Successfull!")
