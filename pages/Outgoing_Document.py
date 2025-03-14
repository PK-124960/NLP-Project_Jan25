import streamlit as st
from datetime import datetime

# 📌 ตั้งค่า UI Theme ให้อยู่ในโทนเดียวกัน
st.set_page_config(page_title="กรอกข้อมูลหนังสือส่ง", layout="wide")
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

st.title("✍️ กรอกข้อมูลสำหรับสร้างหนังสือส่ง")

# 📌 แสดงเนื้อหาเดิมจากหนังสือรับ
received_content = st.session_state.get("corrected_sections", {}).get("เนื้อหา", "ไม่มีข้อมูล")
if received_content:
    with st.expander("📄 เนื้อหาจากหนังสือรับ", expanded=True):
        st.markdown(f"{received_content}")

# 📌 ส่วนราชการผู้ส่ง (Dropdown เลือกหน่วยงาน)
departments = ["กองบัญชาการทหารสูงสุด", "กองทัพบก", "กองทัพเรือ", "กองทัพอากาศ", "กระทรวงกลาโหม"]
sender_department = st.selectbox("📌 ส่วนราชการผู้ส่ง", departments)

# 📌 ที่ กห. ของหนังสือส่ง
document_no = st.text_input("📌 ที่ กห. ของหนังสือส่ง")

# 📌 วันที่ (เลือกวัน/เดือน/ปี พ.ศ.)
date = st.date_input("📅 วันที่ออกหนังสือ", datetime.today())

# 📌 เรื่อง
topic = st.text_input("📌 เรื่อง")

# 📌 เรียน
recipient = st.text_input("📌 เรียน")

# 📌 อ้างถึง (ถ้ามี)
reference = st.text_area("📌 อ้างถึง (ถ้ามี)")

# 📌 สิ่งที่ส่งมาด้วย (ถ้ามี)
attachments = st.text_area("📌 สิ่งที่ส่งมาด้วย (ถ้ามี)")

# 📌 ผู้รับ (ชั้นยศ ชื่อ - นามสกุล)
receiver_name = st.text_input("📌 ผู้รับ (ชั้นยศ ชื่อ - นามสกุล)")

# 📌 ผู้รับ (ตำแหน่ง)
receiver_position = st.text_input("📌 ผู้รับ (ตำแหน่ง)")

# 📌 ผู้พิมพ์ (เสมียน)
clerk_name = st.text_input("📌 ผู้พิมพ์ (เสมียน)")

# 📌 ปุ่มประมวลผลข้อมูล
if st.button("🚀 ดำเนินการสร้างหนังสือส่ง"):
    if not (sender_department and document_no and topic and recipient and receiver_name and receiver_position and clerk_name):
        st.error("❌ กรุณากรอกข้อมูลให้ครบทุกช่องที่จำเป็น!")
    else:
        # เก็บข้อมูลลง session state
        st.session_state["document_send"] = {
            "ส่วนราชการ": sender_department,
            "ที่ กห.": document_no,
            "วันที่": date.strftime("%d/%m/%Y"),
            "เรื่อง": topic,
            "เรียน": recipient,
            "อ้างถึง": reference,
            "สิ่งที่ส่งมาด้วย": attachments,
            "ผู้รับ (ชื่อ-นามสกุล)": receiver_name,
            "ผู้รับ (ตำแหน่ง)": receiver_position,
            "ผู้พิมพ์": clerk_name,
        }
        
        st.success("✅ ข้อมูลถูกบันทึกแล้ว! กำลังดำเนินการสร้างหนังสือส่ง...")
        st.switch_page("pages/generate_document.py")
