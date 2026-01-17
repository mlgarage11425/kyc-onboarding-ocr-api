import re
from datetime import datetime

def clean_name(name):
    if not name:
        return None

    name = re.sub(r'[^A-Za-z ]', '', name)
    name = re.sub(r'\s+', ' ', name).strip()

    return name.title()


def extract_aadhaar(text):
    match = re.search(r'\b\d{4}\s?\d{4}\s?\d{4}\b', text)
    return match.group().replace(" ", "") if match else None


def extract_pan(text):
    clean_text = re.sub(r'[^A-Z0-9]', '', text.upper())
    match = re.search(r'[A-Z]{5}[0-9]{4}[A-Z]', clean_text)
    return match.group() if match else None


def extract_dob(text):
    dates = re.findall(r'\b\d{2}/\d{2}/\d{4}\b', text)

    for d in dates:
        try:
            date_obj = datetime.strptime(d, "%d/%m/%Y").date()
            if 1950 <= date_obj.year <= 2015:   # realistic Aadhaar age band
                return date_obj
        except ValueError:
            continue

    return None


def extract_name_from_text(text):
    lines = [l.strip() for l in text.split("\n") if l.strip()]

    for i, line in enumerate(lines):
        line_upper = line.upper()

        if "NAME" in line_upper or "PERMANENT ACCOUNT NUMBER" in line_upper:
            for j in range(i + 1, min(i + 4, len(lines))):
                candidate = lines[j].strip()

                if (
                    candidate.isupper()
                    and 5 <= len(candidate) <= 40
                    and not any(char.isdigit() for char in candidate)
                    and "INCOME" not in candidate.upper()
                ):
                    return candidate.title()

    return None



def extract_name_from_aadhaar(text):
    lines = [l.strip() for l in text.split("\n") if l.strip()]

    blacklist = [
        "GOVERNMENT", "INDIA", "UNIQUE", "IDENTIFICATION", "AUTHORITY",
        "FATHER", "DOB", "MALE", "FEMALE", "ADDRESS", "UIDAI"
    ]

    for i, line in enumerate(lines):
        line_upper = line.upper()

        if any(b in line_upper for b in blacklist):
            continue

        if any(char.isdigit() for char in line_upper):
            continue

        if 8 <= len(line_upper) <= 30:
            nearby = " ".join(lines[i:i+4]).upper()
            if "DOB" in nearby or "FATHER" in nearby:
                return line_upper.title()

    return None


'''def extract_address(text):
    if not text:
        return None

    text = text.replace("\r", "\n")
    lines = [l.strip() for l in text.split("\n") if l.strip()]

    address_lines = []
    start = False

    for line in lines:
        l = line.lower()

        # Start when "address" keyword found
        if "Address:" in l:
            start = True
            continue

        if start:
            # Stop when pincode found
            if re.search(r"\b\d{6}\b", line):
                address_lines.append(line)
                break

            # Skip garbage lines
            if any(x in l for x in ["uidai", "www", "help@", "1947", "gov", "india"]):
                continue

            address_lines.append(line)

    address = " ".join(address_lines)
    address = re.sub(r'\s+', ' ', address).strip()

    return address if len(address) > 15 else None'''

def extract_address(text):
    if not text:
        return None

    text = text.replace("\r", "\n")
    lines = [l.strip() for l in text.split("\n") if l.strip()]

    address_lines = []
    start = False

    for line in lines:
        l = line.lower()

        if "address" in l:
            start = True
            continue

        if start:
            if any(x in l for x in ["uidai", "www", "help@", "1947", "gov", "india"]):
                continue

            address_lines.append(line)

            # Stop when pincode found
            if re.search(r"\b\d{6}\b", line):
                break

    address = " ".join(address_lines)

    # Cleanup
    address = re.sub(r'\s+', ' ', address)
    address = re.sub(r' ,', ',', address)
    address = address.replace(" ,", ",")
    address = address.strip()

    return address if len(address) > 15 else None

