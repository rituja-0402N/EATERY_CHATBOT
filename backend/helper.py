def extract_session_id(session_str:str):
    import re
    session_regex = re.search(r"/sessions/(.*?)/contexts/",session_str)
    if session_regex:
        extracted_session_id = session_regex.group(1)
        return extracted_session_id
    return ""

def get_str_from_food_dict(food_dict:dict):
    return ", ".join([f"{int(value)} {key}" for key, value in food_dict.items()])
if __name__ =="__main__":
    print(extract_session_id("projects/mira-chatbot-sadm/agent/sessions/63c192e6-05ac-7c9e-2346-3a0d4e43c23c/contexts/ongoing-order"))