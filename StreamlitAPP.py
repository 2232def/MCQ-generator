import os
import json
import traceback
import pandas as pd
from dotenv import load_dotenv
from src.mcqgenerator.utils import read_file, get_table_data
import streamlit as st
from src.mcqgenerator.logger import logging
from src.mcqgenerator.MCQgenerator import generate_evaluate_chain

with open('D:\Users\Lenovo\Downloads\mcqgen\Response.json','r') as file:
    RESPONSE_JSON = json.load(file)

st.write("Streamlit version:", st.__version__)

st.title("MCQ Generator Application with LangChain and Gemini")

with st.form("user_inputs"):

    uploaded_file = st.file_uploader("upload a PDF or txt file")