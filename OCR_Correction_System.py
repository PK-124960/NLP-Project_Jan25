import streamlit as st
import os
from ocr_processing import extract_text_from_pdf, load_correction_dict, save_correction
from text_extraction import extract_sections_123 

# ---------- PAGE CONFIG + THEME ----------
st.set_page_config(page_title="OCR Correction System", layout="wide")

# ---------- EARTH THEME CUSTOMIZATION ----------
st.markdown("""
    <style>
        /* พื้นหลังหลัก */
        [data-testid="stAppViewContainer"] > .main {
            background-color: #FAF3E0;
        }
        /* Sidebar */
        [data-testid="stSidebar"] {
            background-color: #D7B58A;
        }
        /* Card สวยๆ */
        .earth-card {
            background-color: #ffffff;
            padding: 25px;
            border-radius: 12px;
            border: 2px solid #D2B48C;
            margin-bottom: 20px;
            box-shadow: 2px 2px 8px rgba(0,0,0,0.05);
        }
        /* Input */
        .stTextInput > div > div > input,
        .stSelectbox > div > div > div,
        .stDateInput > div > div > input,
        .stTextArea > div > textarea {
            background-color: #ffffff;
            border: 1px solid #D2B48C;
            border-radius: 8px;
            padding: 10px;
        }
        /* Button */
        .stButton>button {
            background-color: #8FBC8F;
            color: white;
            border-radius: 10px;
            font-weight: bold;
            padding: 10px 20px;
        }
        .stButton>button:hover {
            background-color: #6B8E23;
        }
    </style>
""", unsafe_allow_html=True)

# ---------- SIDEBAR ----------
st.sidebar.title("📂 จัดการเอกสาร")
st.sidebar.info("อัปโหลดและแก้ไขเอกสารราชการ")

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

uploaded_files = st.sidebar.file_uploader("📂 อัปโหลดไฟล์ PDF", type=["pdf"], accept_multiple_files=True)

# ---------- MAIN WORKFLOW ----------
if uploaded_files:
    selected_file = st.sidebar.selectbox("📄 เลือกไฟล์", [file.name for file in uploaded_files])
    selected_pdf = next(file for file in uploaded_files if file.name == selected_file)
    pdf_path = os.path.join(UPLOAD_DIR, selected_pdf.name)
    
    with open(pdf_path, "wb") as f:
        f.write(selected_pdf.getbuffer())
    
    # 📖 ประมวลผล OCR
    st.title("📝 ตรวจสอบข้อความหนังสือเข้า")
    
    with st.spinner("📖 กำลังประมวลผล OCR..."):
        ocr_text = extract_text_from_pdf(pdf_path)
        sections = extract_sections_123(ocr_text)
        corrections = load_correction_dict()

    st.success("✅ OCR ประมวลผลสำเร็จแล้ว!")

    corrected_sections = {}

    # ---------- แสดงผลเนื้อหาแต่ละข้อ ----------
    st.markdown("<div class='earth-card'>", unsafe_allow_html=True)
    st.header("🔍 ข้อความที่ได้จาก OCR (แก้ไขได้)")

    for section, content in sections.items():
        with st.expander(f"✏️ {section}", expanded=True):
            corrected_text = st.text_area(
                f"แก้ไข {section}",
                value=content,
                height=250,
                key=f"text_area_{section}"
            )
            corrected_sections[section] = corrected_text

    st.markdown("</div>", unsafe_allow_html=True)

    # ---------- กรอกข้อมูลส่วนหัวเอกสาร ----------
    # 📌 กรอกข้อมูลส่วนหัวเอกสาร
    st.markdown("<div class='earth-card'>", unsafe_allow_html=True)
    st.header("📋 กรอกข้อมูลส่วนหัวเอกสาร")

    departments = ["กองบัญชาการทหารสูงสุด", "กองทัพบก", "กองทัพเรือ"]
    ref_numbers = ["กห.123/2568", "กห.456/2568", "กห.789/2568"]
    subjects = ["ขออนุมัติการฝึกอบรม", "ขออนุมัติเดินทางไปราชการ", "ขออนุมัติโครงการจัดซื้อจัดจ้าง"]
    recipients = ["ผู้บัญชาการทหารสูงสุด", "ผู้อำนวยการกองกำลังพล", "ผู้อำนวยการสำนักงานงบประมาณ"]

    col1, col2 = st.columns(2)
    with col1:
        department = st.selectbox("📌 ส่วนราชการ", departments)
        ref_number = st.selectbox("📌 ที่ กห.", ref_numbers)
        date = st.date_input("📅 วันที่")
    with col2:
        subject = st.selectbox("📌 เรื่อง", subjects)
        recipient = st.selectbox("📌 เรียน", recipients)

    # 📌 ฟอร์มอ้างถึง และ สิ่งที่ส่งมาด้วย
    st.markdown("""
    <div style="margin-top: 20px;">
        <label style="font-weight: bold; font-size: 1.1rem;">📌 อ้างถึง (ถ้ามี)</label>
    </div>
    """, unsafe_allow_html=True)

    reference = st.text_area(
        "",
        placeholder="ระบุข้อมูลอ้างถึง (ถ้ามี)...",
        height=120
    )

    st.markdown("""
    <div style="margin-top: 20px;">
        <label style="font-weight: bold; font-size: 1.1rem;">📌 สิ่งที่ส่งมาด้วย (ถ้ามี)</label>
    </div>
    """, unsafe_allow_html=True)

    attachments = st.text_area(
        "",
        placeholder="ระบุสิ่งที่ส่งมาด้วย (ถ้ามี)...",
        height=120
    )

    st.markdown("</div>", unsafe_allow_html=True)

    # รวมข้อมูล
    corrected_sections.update({
        "ส่วนราชการ": department,
        "ที่ กห.": ref_number,
        "วันที่": date.strftime("%d/%m/%Y"),
        "เรื่อง": subject,
        "เรียน": recipient,
        "อ้างถึง": reference,
        "สิ่งที่ส่งมาด้วย": attachments,
    })

    # ---------- บันทึก ----------
    st.markdown("<div class='earth-card'>", unsafe_allow_html=True)
    st.header("📥 ดำเนินการ")

    if st.button("💾 บันทึกและดูเอกสาร", key="save_corrected_doc"):
        save_correction(corrected_sections)
        st.session_state["corrected_sections"] = corrected_sections
        st.success("✅ บันทึกข้อมูลเรียบร้อย กำลังไปยังหน้าแสดงเอกสาร...")
        st.switch_page("pages/Incoming_Document.py")

    st.markdown("</div>", unsafe_allow_html=True)
