import os

import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader

with open(os.path.join(os.path.dirname(__file__), "config.yaml")) as f:
    config = yaml.load(f, Loader=SafeLoader)


def get_authenticator():
    return stauth.Authenticate(
        credentials=config["credentials"],
        cookie_name=config["cookie"]["name"],
        key=config["cookie"]["key"],
        cookie_expiry_days=config["cookie"]["expiry_days"],
    )
