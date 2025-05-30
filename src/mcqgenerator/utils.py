import os
import PyPDF2
import json
import traceback


def read_file(file):
    if file.name.endswith(".pdf"):
        try:
            pdf_reader = PyPDF2.PdfReader(file)
            text=""
            for page in pdf_reader.pages:
                text+=page.extract_text()
            return text

        except Exception as e:
            raise Exception("error reading the PDF file")

    elif file.name.endswith(".txt"):
        return file.read().decode("utf-8")

    else:
        raise Exception(
            "unsupported file format only pdf and text file supported"
        ) 
    
def get_table_data(quiz_str):
    try:
        import re
        json_match = re.search(r'```(?:json)?\s*([\s\S]*?)\s*```', quiz_str)
        if json_match:
            quiz_str = json_match.group(1)

        quiz_dict=json.loads(quiz_str)
        quiz_table_data=[]

        for key, value in quiz_dict.items():
            mcq=value["mcq"]
            correct=value["correct"]
            option = value["options"]

            quiz_table_data.append({
                "QUESTIONS" : mcq, 
                "Option A" :  f"a) {option.get("a","")}",
                "Option B" :  f"b) {option.get("b","")}",
                "Option C" :  f"c) {option.get("c","")}",
                "Option D" :  f"d) {option.get("d","")}",
                "Correct": correct 
            })

        return quiz_table_data
    
    except Exception as e:
        traceback.print_exception(type(e), e, e.__traceback__)
        return False
