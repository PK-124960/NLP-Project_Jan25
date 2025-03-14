import streamlit as st

st.title("📄 เอกสารที่ปรับแก้ไขแล้ว")

if "corrected_sections" not in st.session_state:
    st.error("❌ ไม่พบข้อมูลการแก้ไข กรุณากลับไปแก้ไขและบันทึกอีกครั้ง")
else:
    corrected_data = st.session_state.get("corrected_sections", {})

    # 📌 แสดงหัวเอกสาร
    st.markdown("""
    <h3 style='text-align: center;'>บันทึกข้อความ</h3>
    """, unsafe_allow_html=True)

    # 📌 แสดงโลโก้ครุฑ
    kru_logo = "kru_logo.png"  # 📌 ตรวจสอบให้แน่ใจว่ามีไฟล์รูปครุฑอยู่ในโฟลเดอร์
    st.image(kru_logo, width=100)
    
    # 📌 จัดรูปแบบตามหนังสือราชการ
    st.markdown(f"""
    **ส่วนราชการ**: {corrected_data.get('ส่วนราชการ', 'ไม่มีข้อมูล')}  
    **ที่ กห.**: {corrected_data.get('ที่ กห.', 'ไม่มีข้อมูล')}  
    **วันที่**: {corrected_data.get('วันที่', 'ไม่มีข้อมูล')}  
    **เรื่อง**: {corrected_data.get('เรื่อง', 'ไม่มีข้อมูล')}  
    **เรียน**: {corrected_data.get('เรียน', 'ไม่มีข้อมูล')}  
    """, unsafe_allow_html=True)

    # 📌 อ้างถึง และ สิ่งที่ส่งมาด้วย (ถ้ามี)
    if corrected_data.get("อ้างถึง"):
        st.markdown(f"**อ้างถึง**: {corrected_data.get('อ้างถึง')}")
    if corrected_data.get("สิ่งที่ส่งมาด้วย"):
        st.markdown(f"**สิ่งที่ส่งมาด้วย**: {corrected_data.get('สิ่งที่ส่งมาด้วย')}")
    
    # 📌 แสดงเนื้อหาหลัก
    st.markdown(f"""
    <br>{corrected_data.get('เนื้อหา', 'ไม่มีข้อมูล')}<br><br>
    """, unsafe_allow_html=True)
    
    # 📌 เพิ่มลายเซ็น และชื่อเจ้าหน้าที่
    st.markdown("""
    <p style='text-align: right;'>
        (ลงชื่อ) ................................................  
        <br>
        ................................................
    </p>
    """, unsafe_allow_html=True)
    
    st.success("✅ เอกสารแสดงผลเรียบร้อยแล้ว!")

    # 📌 ปุ่มไปยังหน้า UI กรอกข้อมูลหนังสือส่ง
    if st.button("✍️ ดำเนินการสร้างหนังสือส่ง"):
        st.switch_page("pages/Outgoing_Document.py")