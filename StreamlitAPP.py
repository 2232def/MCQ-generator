import json
import traceback
import pandas as pd
from src.mcqgenerator.utils import read_file, get_table_data
import streamlit as st
from src.mcqgenerator.MCQgenerator import generate_evaluate_chain
from langchain_core.callbacks import StdOutCallbackHandler


handler = StdOutCallbackHandler()

with open(r'./Response.json','r') as file:
    RESPONSE_JSON = json.load(file)

st.write("Streamlit version:", st.__version__)

st.title("MCQ Generator Application with LangChain and Gemini")

with st.form("user_inputs"):

    uploaded_file = st.file_uploader("upload a PDF or txt file")

    mcq_count = st.number_input("No. of MCQs", min_value=3, max_value=50)

    subject = st.text_input("Insert Subject",  max_chars=20)

    tone = st.text_input("Complexity Level of Questions", max_chars=20, placeholder="Simple")

    button = st.form_submit_button("Generate MCQs") 

    if button and uploaded_file is not None and mcq_count and subject and tone:
        with st.spinner("Loading...."):
            try:
                text = read_file(uploaded_file)
                cb = StdOutCallbackHandler()
                response = generate_evaluate_chain({
                    "text":text,
                    "number":mcq_count,
                    "subject":subject,
                    "tone":tone,
                    "response_json":json.dumps(RESPONSE_JSON) 
                }, callbacks=[cb] ) 
                    
            except Exception as e:
                traceback.print_exception(type(e),e,e.__traceback__)
                st.error("error")

            else:
                # print(f"Total Tokens: {cb.total_tokens}")
                # print(f"Prompt Tokens: {cb.prompt_tokens}")
                # print(f"Completion Tokens: {cb.completion_tokens}")
                if isinstance(response, dict):
                    quiz = response.get("quiz" , None)
                    if quiz is not None:
                        table_data = get_table_data(quiz)
                        if table_data is not False:
                            df = pd.DataFrame(table_data)
                            df.index = df.index+1
                            st.table(df)
                            st.text_area(label="Review", value=response["review"])
                        else:
                            st.error("Error in the table data")
                    else:
                        st.error("Quiz is none")
                else:
                    st.write(response)

