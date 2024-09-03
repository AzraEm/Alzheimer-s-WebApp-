import streamlit as st
from openai import OpenAI
import numpy as np
import pickle
import json
import requests

ROOT_NAME = "kalemvesilgi"
MODEL_NAME = "full_transcript_mlp_best_model3"
MAPPER = {"0": "Normal", "1": "Alzheimer's" }
CLIENT = openapi(api_key=st.secrets["OPEN_API_KEY"])

def save_feedbacks(data):
    url = "https://s5bcsbu84l.execute-api.us-east-1.amazonaws.com/Research/record-history"
    r = requests.post(url, data=json.dumps(data))
    response = getattr(r,'_content').decode("utf-8")
    response = json.loads(response)
    print(response)
    saved = response["data"]["saved"]
    return saved

def create_payload_to_record(user_id, user_context, label):
    payload = {"httpMethod": "POST", "body": 
            {"rootName": ROOT_NAME,
            "userId": user_id,
            "userText": user_context,
            "prediction": label}}

    return payload

