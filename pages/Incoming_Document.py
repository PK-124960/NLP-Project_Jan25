import streamlit as st

# ---------- CUSTOM EARTH THEME CSS ----------
st.markdown("""
    <style>
        [data-testid="stAppViewContainer"] > .main {
            background-color: #F5F5DC; /* Earth tone: Beige */
        }
        .earth-card {
            background-color: #FAF0E6; /* Light earth tone */
            padding: 20px;
            border-radius: 12px;
            border: 2px solid #D2B48C; /* Tan border */
            margin-bottom: 20px;
        }
        h3 {
            color: #6B4226; /* Earth Brown */
        }
        .stButton>button {
            background-color: #8FBC8F; /* Soft green */
            color: white;
            border-radius: 10px;
            padding: 10px 20px;
            font-weight: bold;
        }
        .stButton>button:hover {
            background-color: #6B8E23; /* Darker green on hover */
        }
    </style>
""", unsafe_allow_html=True)

# ---------- UI START ----------
st.title("📄 หนังสือเข้า (Incoming Letter)")

# 📍 ตรวจสอบข้อมูล
if "corrected_sections" not in st.session_state:
    st.error("❌ ไม่พบข้อมูลการแก้ไข กรุณากลับไปแก้ไขและบันทึกอีกครั้ง")
else:
    corrected_data = st.session_state.get("corrected_sections", {})

    with st.spinner('🚀 กำลังโหลดข้อมูลหนังสือเข้า...'):
        st.markdown("<div class='earth-card'>", unsafe_allow_html=True)

        # โลโก้
        kru_logo = "kru_logo.png"
        st.image(kru_logo, width=100)

        # ชื่อเรื่อง
        st.markdown("""
        <h3 style='text-align: center;'>บันทึกข้อความ</h3>
        """, unsafe_allow_html=True)

        # ส่วนหัวเอกสาร
        st.markdown(f"""
        **ส่วนราชการ**: {corrected_data.get('ส่วนราชการ', 'ไม่มีข้อมูล')}  
        **ที่ กห.**: {corrected_data.get('ที่ กห.', 'ไม่มีข้อมูล')}  
        **วันที่**: {corrected_data.get('วันที่', 'ไม่มีข้อมูล')}  
        **เรื่อง**: {corrected_data.get('เรื่อง', 'ไม่มีข้อมูล')}  
        **เรียน**: {corrected_data.get('เรียน', 'ไม่มีข้อมูล')}  
        """, unsafe_allow_html=True)

        if corrected_data.get("อ้างถึง"):
            st.markdown(f"**อ้างถึง**: {corrected_data.get('อ้างถึง')}")
        if corrected_data.get("สิ่งที่ส่งมาด้วย"):
            st.markdown(f"**สิ่งที่ส่งมาด้วย**: {corrected_data.get('สิ่งที่ส่งมาด้วย')}")

        st.markdown("<br>", unsafe_allow_html=True)

        # เนื้อหาแต่ละข้อ
        for i in range(1, 4):
            section_key = f"ข้อ {i}"
            content = corrected_data.get(section_key, "").strip()
            if content:
                thai_number = ["๑", "๒", "๓"][i-1]

                if i == 1:
                    display_content = f"ตามที่ {content}"
                elif i == 2:
                    display_content = content
                elif i == 3:
                    display_content = f"เพื่อให้การดำเนินการเป็นไปด้วยความเรียบร้อย {content}"

                st.markdown(f"""
                <div style='text-indent: 2em; font-size: 1.1rem; line-height: 1.8;'>
                    <strong>{thai_number}.</strong> {display_content}
                </div>
                <br>
                """, unsafe_allow_html=True)

        # ลายเซ็น
        st.markdown("""
        <p style='text-align: right;'>
            (ลงชื่อ) ................................................<br>
            (.............................................)
        </p>
        """, unsafe_allow_html=True)

        st.success("✅ เอกสารแสดงผลเรียบร้อยแล้ว!")

        st.markdown("</div>", unsafe_allow_html=True)  # 🔚 ปิด div earth-card

    # 🔵 ปุ่มย้อนกลับ / ดำเนินการ
    st.markdown("<div class='earth-card'>", unsafe_allow_html=True)
    st.subheader("🛠️ การดำเนินการถัดไป")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("⬅️ ย้อนกลับไปแก้ไขรายละเอียด", key="back_button"):
            st.switch_page("OCR_Correction_System.py")

    with col2:
        if st.button("✍️ ดำเนินการสร้างหนังสือส่ง", key="outgoing_button"):
            st.switch_page("pages/Outgoing_Document.py")

    st.markdown("</div>", unsafe_allow_html=True)
