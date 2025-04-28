from setuptools import find_packages, setup

setup(
    name='mcqgenerator',
    version='0.0.1',
    author='Dev Kumar Singh',
    author_email='dev07072004@gmail.com',
    install_requires=["langchain-google-genai","langchain", "streamlit", "python-dotenv", "PyPDF2"],
    packages=find_packages(),
)