import re

def thai_to_arabic_number(text):
    """แปลงเลขไทยเป็นเลขอารบิกในข้อความ"""
    thai_num_map = str.maketrans("๐๑๒๓๔๕๖๗๘๙", "0123456789")
    return text.translate(thai_num_map)

def extract_sections_123(text):
    """
    สกัดเนื้อหาจากข้อ 1, 2, 3 อัตโนมัติ และแปลงเลขไทยเป็นเลขอารบิก
    - text: ข้อความ OCR ที่ได้จากไฟล์
    - return: dict {"ข้อ 1": ..., "ข้อ 2": ..., "ข้อ 3": ...}
    """
    # ✅ แปลงเลขไทยเป็นเลขอารบิกก่อน
    text = thai_to_arabic_number(text)

    # ✅ ใช้ regex หา pattern "1.", "2.", "3." พร้อมข้อความถัดไป
    pattern = r"(\d+\.)\s*(.*?)\s*(?=\d+\.|$)"
    matches = re.findall(pattern, text, re.DOTALL)

    sections = {}
    for number, content in matches:
        number_clean = number.strip('.')
        sections[f"ข้อ {number_clean}"] = content.strip()
    
    return sections
