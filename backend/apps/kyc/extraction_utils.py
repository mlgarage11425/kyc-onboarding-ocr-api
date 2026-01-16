import re
from datetime import datetime

def extract_aadhaar(text):
    match = re.search(r'\b\d{4}\s\d{4}\s\d{4}\b|\b\d{12}\b', text)
    return match.group().replace(" ", "") if match else None

def extract_pan(text):
    match = re.search(r'\b[A-Z]{5}[0-9]{4}[A-Z]\b', text)
    return match.group() if match else None

def extract_dob(text):
    match = re.search(r'\b\d{2}/\d{2}/\d{4}\b', text)
    if match:
        return datetime.strptime(match.group(), "%d/%m/%Y").date()
    return None

def extract_name(text):
    lines = text.split("\n")
    for line in lines:
        if line.isupper() and len(line.split()) <= 4:
            return line.strip()
    return None

def extract_address(text):
    keywords = ['ADDRESS', 'Addr', 'Add']
    lines = text.split("\n")
    capture = False
    address_lines = []

    for line in lines:
        if any(k.lower() in line.lower() for k in keywords):
            capture = True
            continue
        if capture:
            if line.strip() == "":
                break
            address_lines.append(line.strip())

    return " ".join(address_lines) if address_lines else None
