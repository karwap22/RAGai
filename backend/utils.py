def generate_summary_prompt(text:str):
    res = "Summarize the following text present on webpage - \n"
    res += text
    return res

def generate_question_prompt(text:str, question:str):
    res = "Answer the following question - "
    res += question
    res += "\n Based on the follwing text present on the website - \n"
    res += text
    return res
