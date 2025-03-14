# import streamlit as st
# import json
# import os
# import difflib
# from ocr_processing import extract_text_from_pdf, extract_sections, load_correction_dict, save_correction, suggest_corrections

# # 📌 ตั้งค่า UI ของ Streamlit
# st.set_page_config(page_title="OCR Correction System", layout="wide")
# st.title("📄 OCR Correction System")

# # 📌 ตรวจสอบและสร้างโฟลเดอร์ uploads หากไม่มี
# UPLOAD_DIR = "uploads"
# os.makedirs(UPLOAD_DIR, exist_ok=True)

# # 📌 อัปโหลดไฟล์ PDF
# uploaded_files = st.file_uploader("📂 อัปโหลดไฟล์ PDF", type=["pdf"], accept_multiple_files=True)

# if uploaded_files:
#     selected_file = st.selectbox("📄 เลือกไฟล์ที่ต้องการแก้ไข", [file.name for file in uploaded_files])
#     selected_pdf = next(file for file in uploaded_files if file.name == selected_file)
#     pdf_path = os.path.join(UPLOAD_DIR, selected_pdf.name)
    
#     with open(pdf_path, "wb") as f:
#         f.write(selected_pdf.getbuffer())
    
#     # 📌 ใช้ OCR ดึงข้อความจาก PDF และแยกส่วนข้อมูล
#     ocr_text = extract_text_from_pdf(pdf_path)
#     sections = extract_sections(ocr_text)
#     corrections = load_correction_dict()
#     word_corrections = {}

#     st.subheader("🔍 คำที่อาจผิดจาก OCR พร้อมตำแหน่งในเอกสาร")
#     corrected_sections = {}
    
#     for section, text in sections.items():
#         st.markdown(f"### 📝 {section}")
        
#         # 📌 ตรวจหาคำที่อาจผิด
#         words = text.split()
#         corrected_words = []
        
#         for i, word in enumerate(words):
#             suggested_word = corrections.get(word, word)  # ใช้คำที่เคยแก้ไข หรือค่าเดิม
#             corrected_word = st.text_input(
#                 f"แก้ไข `{word}`", 
#                 key=f"edit_{section}_{i}_{word}", 
#                 value=suggested_word
#             )
#             word_corrections[word] = corrected_word
#             corrected_words.append(corrected_word)
        
#         # 📌 รวมคำที่ถูกแก้ไขแล้วกลับมาเป็นประโยค
#         corrected_sections[section] = " ".join(corrected_words)
    
#     # # 📌 ปุ่มบันทึกการแก้ไข
#     # if st.button("💾 บันทึกการแก้ไข"):
#     #     save_correction(word_corrections)
#     #     st.session_state["corrected_sections"] = corrected_sections  # เก็บข้อมูลที่แก้ไขไว้
#     #     st.success("✅ บันทึกการแก้ไขสำเร็จ!")
    
#     # # 📌 แสดงข้อความที่ถูกแก้ไข
#     # if "corrected_sections" in st.session_state:
#     #     st.subheader("📜 เอกสารที่ปรับแก้ไขแล้ว")
#     #     for section, text in st.session_state["corrected_sections"].items():
#     #         st.markdown(f"### 📝 {section}")
#     #         st.markdown(f"{text}")
    
#     # 📌 ปุ่มบันทึกการแก้ไข และเปลี่ยนไปหน้าเอกสาร
#     if st.button("💾 บันทึกและแสดงเอกสารที่แก้ไขแล้ว"):
#         save_correction(word_corrections)
#         st.session_state["corrected_sections"] = corrected_sections  # เก็บข้อมูลที่แก้ไขไว้
#         st.success("✅ บันทึกการแก้ไขสำเร็จ!")
#         st.switch_page("pages/document.py")  # เปลี่ยนไปยังหน้าแสดงเอกสาร

#  //---------------------------------------------------//

import streamlit as st
import json
import os
import difflib
from ocr_processing import extract_text_from_pdf, extract_sections, load_correction_dict, save_correction, suggest_corrections

# 📌 ตั้งค่า UI ของ Streamlit พร้อมธีมน้ำตาล Minimal
st.set_page_config(page_title="OCR Correction System", layout="wide")
st.markdown("""
    <style>
        body {
            background-color: #FAF3E0;
        }
        .stSidebar {
            background-color: #D4A373;
        }
        .stTextInput > div > div > input {
            border-radius: 8px;
            border: 2px solid #8D6E63;
            padding: 10px;
        }
        .stButton > button {
            background-color: #8D6E63;
            color: white;
            border-radius: 8px;
            padding: 10px;
        }
        .stExpander {
            background-color: #EDE0D4;
            border-radius: 10px;
        }
    </style>
""", unsafe_allow_html=True)

# 📌 เพิ่ม Sidebar
st.sidebar.title("📂 จัดการเอกสาร")
st.sidebar.info("อัปโหลดและแก้ไขเอกสารราชการ")

# 📌 ตรวจสอบและสร้างโฟลเดอร์ uploads หากไม่มี
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# 📌 อัปโหลดไฟล์ PDF
uploaded_files = st.sidebar.file_uploader("📂 อัปโหลดไฟล์ PDF", type=["pdf"], accept_multiple_files=True)

if uploaded_files:
    selected_file = st.sidebar.selectbox("📄 เลือกไฟล์ที่ต้องการแก้ไข", [file.name for file in uploaded_files])
    selected_pdf = next(file for file in uploaded_files if file.name == selected_file)
    pdf_path = os.path.join(UPLOAD_DIR, selected_pdf.name)
    
    with open(pdf_path, "wb") as f:
        f.write(selected_pdf.getbuffer())
    
    # 📌 ใช้ OCR ดึงข้อความจาก PDF และแยกส่วนข้อมูล
    st.title("📝 แก้ไขข้อความ OCR")
    st.write("ระบบตรวจสอบและแก้ไขคำผิดจาก OCR")
    
    with st.spinner("📖 กำลังประมวลผล OCR..."):
        ocr_text = extract_text_from_pdf(pdf_path)
        sections = extract_sections(ocr_text)
        corrections = load_correction_dict()
        word_corrections = {}
    
    st.success("✅ OCR ประมวลผลสำเร็จ!")
    
    # 📌 ใช้ Container เพื่อจัดระเบียบ UI
    corrected_sections = {}
    for section, text in sections.items():
        with st.expander(f"🔍 {section}", expanded=True):
            words = text.split()
            corrected_words = []
            
            for i, word in enumerate(words):
                suggested_word = corrections.get(word, word)
                corrected_word = st.text_input(
                    f"✏️ `{word}`", 
                    key=f"edit_{section}_{i}_{word}", 
                    value=suggested_word
                )
                word_corrections[word] = corrected_word
                corrected_words.append(corrected_word)
            
            corrected_sections[section] = " ".join(corrected_words)
    
    # 📌 ปุ่มบันทึกการแก้ไขและเปลี่ยนหน้า
    # st.markdown("""
    #     <div style='text-align: center; margin-top: 20px;'>
    #         <button style='background-color: #8D6E63; color: white; padding: 15px 30px; border-radius: 10px;'>
    #             💾 บันทึกและดูเอกสาร
    #         </button>
    #     </div>
    # """, unsafe_allow_html=True)

    if st.button("💾 บันทึกและดูเอกสาร"):
        save_correction(word_corrections)
        st.session_state["corrected_sections"] = corrected_sections
        st.success("✅ บันทึกสำเร็จ กำลังไปยังเอกสาร...")
        st.switch_page("pages/Incoming_Document.py")