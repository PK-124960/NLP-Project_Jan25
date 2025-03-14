# import pytesseract
# import pdf2image
# import cv2
# import json
# import os
# import re
# import numpy as np
# from PIL import Image

# # 📌 ตั้งค่า Poppler และ Tesseract Path
# POPPLER_PATH = r"C:\poppler-24.08.0\Library\bin"
# pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
# os.environ["TESSDATA_PREFIX"] = r"C:\Program Files\Tesseract-OCR\tessdata"

# CORRECTION_FILE = "correction_db.json"

# def load_correction_dict():
#     """โหลดฐานข้อมูลคำที่ถูกแก้ไขแล้ว"""
#     if os.path.exists(CORRECTION_FILE):
#         with open(CORRECTION_FILE, "r", encoding="utf-8") as f:
#             data = json.load(f)
#             return data if isinstance(data, dict) else {}  # ป้องกันปัญหา list
#     return {}

# def apply_saved_corrections(text):
#     """📌 ใช้คำที่ถูกต้องที่บันทึกไว้ แก้ไขข้อความ OCR อัตโนมัติ"""
#     corrections = load_correction_dict()
#     for wrong, correct in corrections.items():
#         text = text.replace(wrong, correct)
#     return text

# def preprocess_image(image):
#     """ 📌 ปรับคุณภาพภาพก่อน OCR """
#     gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
#     gray = cv2.GaussianBlur(gray, (3,3), 0)
#     gray = cv2.fastNlMeansDenoising(gray, None, 10, 7, 21)

#     # ปรับ Adaptive Threshold ให้ OCR อ่านตัวอักษรคมขึ้น
#     adaptive_thresh = cv2.adaptiveThreshold(
#         gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 21, 7
#     )
    
#     return adaptive_thresh

# def extract_text_from_pdf(pdf_path):
#     """ 📌 แปลง PDF เป็นภาพแล้วใช้ OCR """
#     images = pdf2image.convert_from_path(pdf_path, dpi=400, poppler_path=POPPLER_PATH)
#     extracted_text = ""
#     for image in images:
#         open_cv_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
#         processed_img = preprocess_image(open_cv_image)
        
#         text = pytesseract.image_to_string(processed_img, lang="tha", config="--psm 6 --oem 1")
#         extracted_text += text + "\n\n"
    
#     return extracted_text


# import re

# def extract_sections(ocr_text):
#     """ 📌 แยกข้อความออกเป็นหัวข้อจากหนังสือราชการ และหลีกเลี่ยงข้อความซ้ำซ้อน """
#     sections = {
#         "ส่วนราชการ": "",
#         "ที่ กห.": "",
#         "วันที่": "",
#         "เรื่อง": "",
#         "เรียน": "",
#         "อ้างถึง": "",
#         "สิ่งที่ส่งมาด้วย": "",
#         "เนื้อหา": ""
#     }

#     patterns = {
#         "ส่วนราชการ": r"(ส่วนราชการ[:\s].*?)(?=ที่|วันที่|เรื่อง|เรียน|$)",
#         "ที่ กห.": r"(ที่ กห.*?)(?=วันที่|เรื่อง|เรียน|$)",
#         "วันที่": r"(วันที่.*?)(?=เรื่อง|เรียน|$)",
#         "เรื่อง": r"(เรื่อง[:\s].*?)(?=เรียน|$)",
#         "เรียน": r"(เรียน[:\s].*?)(?=อ้างถึง|สิ่งที่ส่งมาด้วย|\d+\.)",
#         "อ้างถึง": r"(อ้างถึง[:\s].*?)(?=สิ่งที่ส่งมาด้วย|\d+\.)",
#         "สิ่งที่ส่งมาด้วย": r"(สิ่งที่ส่งมาด้วย[:\s].*?)(?=\d+\.)",
#     }

#     for key, pattern in patterns.items():
#         match = re.search(pattern, ocr_text, re.DOTALL)
#         if match:
#             extracted_text = match.group(1).strip()
            
#             # 📌 หลีกเลี่ยงข้อความซ้ำ เช่น "เรื่อง เรื่อง"
#             if extracted_text.startswith(key):
#                 extracted_text = extracted_text[len(key):].strip()

#             sections[key] = extracted_text

#     # 📌 ดึงข้อความเนื้อหาหลังจาก "๑." หรือหมายเลขลำดับแรก จนถึง "จึงเรียนมาเพื่อ" หรือ "พ. อ."
#     main_body_match = re.search(r"(\b\d+\..*?)(?=\bจึงเรียนมาเพื่อ|\bพ\.\s*อ\.)", ocr_text, re.DOTALL)

#     sections["เนื้อหา"] = main_body_match.group(1).strip() if main_body_match else ""

#     # 📌 หากไม่มีข้อมูล ให้เติม "ไม่มีข้อมูล"
#     for key in sections:
#         if not sections[key]:
#             sections[key] = "ไม่มีข้อมูล"

#     return sections


# # 📌 ไฟล์ฐานข้อมูลการแก้ไขคำผิด
# CORRECTION_FILE = "ocr_corrections.json"

# def load_correction_dict():
#     """โหลดฐานข้อมูลคำที่ถูกแก้ไขแล้ว"""
#     if os.path.exists(CORRECTION_FILE):
#         with open(CORRECTION_FILE, "r", encoding="utf-8") as f:
#             data = json.load(f)
#             return data if isinstance(data, dict) else {}  # ป้องกันปัญหา list
#     return {}

# def save_correction(word_corrections):
#     """บันทึกคำที่ถูกแก้ไขลงฐานข้อมูล"""
#     corrections = load_correction_dict()
#     corrections.update(word_corrections)  # รวมข้อมูลใหม่กับเดิม
#     with open(CORRECTION_FILE, "w", encoding="utf-8") as f:
#         json.dump(corrections, f, ensure_ascii=False, indent=4)

# //-----------------------------------------------//

import pytesseract
import pdf2image
import cv2
import json
import os
import re
import numpy as np
from PIL import Image
from pythainlp.spell import correct
from difflib import get_close_matches

# 📌 ตั้งค่า Poppler และ Tesseract Path
POPPLER_PATH = r"C:\poppler-24.08.0\Library\bin"
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
os.environ["TESSDATA_PREFIX"] = r"C:\Program Files\Tesseract-OCR\tessdata"

CORRECTION_FILE = "ocr_corrections.json"

def load_correction_dict():
    """โหลดฐานข้อมูลคำที่ถูกแก้ไขแล้ว"""
    if os.path.exists(CORRECTION_FILE):
        with open(CORRECTION_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data if isinstance(data, dict) else {}
    return {}

def save_correction(word_corrections):
    """บันทึกคำที่ถูกแก้ไขลงฐานข้อมูล"""
    corrections = load_correction_dict()
    corrections.update(word_corrections)
    with open(CORRECTION_FILE, "w", encoding="utf-8") as f:
        json.dump(corrections, f, ensure_ascii=False, indent=4)

def preprocess_image(image):
    """ 📌 ปรับคุณภาพภาพก่อน OCR """
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (3,3), 0)
    gray = cv2.fastNlMeansDenoising(gray, None, 10, 7, 21)
    adaptive_thresh = cv2.adaptiveThreshold(
        gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 21, 7
    )
    return adaptive_thresh

def extract_text_from_pdf(pdf_path):
    """ 📌 แปลง PDF เป็นภาพแล้วใช้ OCR (รองรับหลายหน้า) """
    images = pdf2image.convert_from_path(pdf_path, dpi=400, poppler_path=POPPLER_PATH)
    extracted_text = ""
    for i, image in enumerate(images):
        open_cv_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
        processed_img = preprocess_image(open_cv_image)
        text = pytesseract.image_to_string(processed_img, lang="tha", config="--psm 6 --oem 1")
        extracted_text += f"\n\n--- หน้า {i+1} ---\n\n" + text
    return extracted_text

def extract_sections(ocr_text):
    """ 📌 แยกข้อความออกเป็นหัวข้อจากหนังสือราชการ """
    sections = {
        "ส่วนราชการ": "",
        "ที่ กห.": "",
        "วันที่": "",
        "เรื่อง": "",
        "เรียน": "",
        "อ้างถึง": "",
        "สิ่งที่ส่งมาด้วย": "",
        "เนื้อหา": ""
    }
    patterns = {
        "ส่วนราชการ": r"ส่วนราชการ[:\s](.*?)(?=ที่|วันที่|เรื่อง|เรียน|$)",
        "ที่ กห.": r"ที่ กห[:\s](.*?)(?=วันที่|เรื่อง|เรียน|$)",
        "วันที่": r"วันที่[:\s](.*?)(?=เรื่อง|เรียน|$)",
        "เรื่อง": r"เรื่อง[:\s](.*?)(?=เรียน|$)",
        "เรียน": r"เรียน[:\s](.*?)(?=อ้างถึง|สิ่งที่ส่งมาด้วย|\d+\.)",
        "อ้างถึง": r"อ้างถึง[:\s](.*?)(?=สิ่งที่ส่งมาด้วย|\d+\.)",
        "สิ่งที่ส่งมาด้วย": r"สิ่งที่ส่งมาด้วย[:\s](.*?)(?=\d+\.)"
    }
    for key, pattern in patterns.items():
        match = re.search(pattern, ocr_text, re.DOTALL)
        if match:
            extracted_text = match.group(1).strip()
            sections[key] = extracted_text
    main_body_match = re.search(r"(\b\d+\..*?)(?=\bจึงเรียนมาเพื่อ|\bพ\.\s*อ\.)", ocr_text, re.DOTALL)
    sections["เนื้อหา"] = main_body_match.group(1).strip() if main_body_match else ""
    for key in sections:
        if not sections[key]:
            sections[key] = "ไม่มีข้อมูล"
    return sections

def suggest_corrections(text):
    """ 📌 ใช้ PyThaiNLP และ difflib แนะนำคำที่ถูกต้อง """
    words = text.split()
    corrections = load_correction_dict()
    suggestions = {}
    for word in words:
        if word in corrections:
            continue
        corrected_by_model = correct(word)
        closest_match = get_close_matches(word, corrections.keys(), n=1)
        best_suggestion = corrected_by_model if corrected_by_model else (closest_match[0] if closest_match else word)
        suggestions[word] = best_suggestion
    return suggestions
