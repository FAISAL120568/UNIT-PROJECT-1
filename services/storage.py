import json
import os

DATA_FILE = "cyber_cases.json"

def load_cases():
    if not os.path.exists(DATA_FILE):
        return []
    
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except Exception:
        return []

def save_cases(cases_list):
    try:
        with open(DATA_FILE, "w", encoding="utf-8") as file:
            json.dump(cases_list, file, ensure_ascii=False, indent=4)
        return True
    except Exception:
        return False