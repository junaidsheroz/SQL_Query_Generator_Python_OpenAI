from turtle import onclick
from matplotlib.pyplot import get
import streamlit as st
import pymysql
import pandas as pd
import numpy as np
import re
import openai
import pyperclip


def getNameFromEmail(email):
    df = pd.read_csv('data.csv')
    name = df.loc[df.email == str(email), 'name']
    return name


if "load_state" not in st.session_state:
    st.session_state.load_state = False


def get_response(txt):
    openai.api_key = "<OPENAI API KEY>"
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt="{}".format(txt),
        temperature=0.3,
        max_tokens=60,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0
    )
    text = response.choices[-1].to_dict()['text']
    res = re.sub('\n', '', text)
    return res


email_entered = st.text_input('Enter your Email to continue')
hello = getNameFromEmail(email_entered)
if hello.empty == True:
    st.error('Please Enter Valid Email ID')

else:
    text_input = st.text_area('Enter the prompt')
    input_button = st.button('Submit')
    if input_button or st.session_state.load_state:
        st.session_state.load_state = True
        if text_input != '':
            txt = st.text_area(label='Query', value=get_response(text_input))
            copy_button = st.button("Copy Query")
            if copy_button or st.session_state.load_state:
                st.session_state.load_state = True
                pyperclip.copy(txt)
