import os
from dotenv import load_dotenv

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_classic.chains import LLMChain, SequentialChain

load_dotenv()

key = os.getenv("GOOGLE_API_KEY")

llm = ChatGoogleGenerativeAI(
    api_key=key,
    model="gemini-2.0-flash",
    temperature=0.7
)

template="""
Text:{text}
You are an expert MCQ maker. Given the above text, it is your job to \
create a quiz  of {number} multiple choice questions for {subject} students in {tone} tone. 
Make sure the questions are not repeated and check all the questions to be conforming the text as well.
Make sure to format your response like  RESPONSE_JSON below  and use it as a guide. \
Ensure to make {number} MCQs
### RESPONSE_JSON
{response_json}
"""

quiz_generation_prompt = PromptTemplate(
    input_variables=["text","number", "subject","tone","response_json"],
    template=template)

quiz_chain = LLMChain(llm=llm, prompt=quiz_generation_prompt, output_key="quiz" ,verbose=True)


template2="""
You are an expert english grammarian and writer. Given a Multiple Choice Quiz for {subject} students.\
You need to evaluate the complexity of the question and give a complete analysis of the quiz. Only use at max 50 words for complexity analysis. 
if the quiz is not at per with the cognitive and analytical abilities of the students,\
update the quiz questions which needs to be changed and change the tone such that it perfectly fits the student abilities
Quiz_MCQs:
{quiz}

Check from an expert English Writer of the above quiz:
"""

quiz_evaluation_prompt = PromptTemplate(input_variables=["subject","quiz"], template=template2)

review_chain = LLMChain(llm=llm , prompt=quiz_evaluation_prompt, output_key="review", verbose=True)

generate_evaluate_chain = SequentialChain(chains=[quiz_chain, review_chain], input_variables=["text","number","subject","tone","response_json"], output_variables=["quiz","review"],verbose=True,) 