import streamlit as st
import pandas as pd
import google.generativeai as genai
import time
from datetime import datetime

# 1. إعدادات الصفحة الفاخرة
st.set_page_config(page_title="فرسان رمضان | Ramadan Knights", page_icon="🌙", layout="wide")

# 2. هندسة الواجهة (CSS) لتصميم احترافي
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    html, body, [class*="st-"] { font-family: 'Cairo', sans-serif; text-align: right; direction: rtl; }
    .main { background: linear-gradient(180deg, #001a11 0%, #002b1b 100%); color: #fdfdfd; }
    .stButton>button { 
        background: linear-gradient(90deg, #d4af37 0%, #f9d976 100%); 
        color: #001a11 !important; border-radius: 25px; font-weight: bold; border: none; padding: 10px 25px; width: 100%; font-size: 1.2rem;
    }
    .card { background: rgba(255, 255, 255, 0.05); padding: 20px; border-radius: 15px; border: 1px solid #d4af37; margin-bottom: 20px; }
    h1, h2, h3 { color: #f9d976 !important; }
    .stTextInput>div>div>input { background-color: #003d26; color: white; border: 1px solid #d4af37; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

# 3. إعداد المساعد (AIzaSyAcsMKzB2rZC-dPjcSzUFq6WxokPsewUMo)
genai.configure(api_key="AIzaSyAcsMKzB2rZC-dPjcSzUFq6WxokPsewUMo")
model = genai.GenerativeModel('gemini-1.5-flash')

# 4. لوحة التحكم الرئيسية
st.markdown("<h1 style='text-align: center;'>🌙 منصة فرسان رمضان</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 1.2rem;'>رحلتك نحو التطوير الإداري والنمو الذاتي</p>", unsafe_allow_html=True)

# 5. المساعد الذكي (بمظهر جديد)
with st.expander("🤖 اطلب استشارة من المساعد الذكي | AI Mentor"):
    user_q = st.text_input("كيف يمكنني مساعدتك في خطتك اليوم؟")
    if st.button("الحصول على إجابة"):
        with st.spinner('جاري تحليل طلبك...'):
            res = model.generate_content(f"بصفتك خبير تطوير إداري، أجب باختصار واحترافية باللغة العربية: {user_q}")
            st.info(res.text)

# 6. منطقة تسجيل الإنجاز
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.subheader("📝 تسجيل إنجاز اليوم")
name = st.text_input("اسم الفارس (Member Name)")

c1, c2 = st.columns(2)
with c1:
    skill = st.selectbox("اختر المهارة (Skill)", ["هندسة الأوامر AI", "المونتاج", "القراءة السريعة", "أخرى"])
    if skill == "أخرى": skill = st.text_input("اكتب مهارتك الخاصة")
with c2:
    habit = st.selectbox("اختر العادة (Habit)", ["العمل العميق", "الامتنان", "شرب الماء", "أخرى"])
    if habit == "أخرى": habit = st.text_input("اكتب عادتك الخاصة")

if st.button("✅ حفظ الإنجاز وكسب 20 نقطة"):
    if name:
        st.success(f"أحسنت يا {name}! تم تسجيل 20 نقطة في رصيدك.")
        st.balloons()
    else:
        st.error("يرجى كتابة الاسم أولاً")
st.markdown("</div>", unsafe_allow_html=True)

# 7. مؤقت التركيز
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.subheader("⏱️ مؤقت التركيز (20 دقيقة)")
if st.button("🚀 ابدأ جلسة العمل العميق"):
    ph = st.empty()
    for t in range(20*60, 0, -1):
        m, s = divmod(t, 60)
        ph.metric("الوقت المتبقي", f"{m:02d}:{s:02d}")
        time.sleep(1)
    st.success("انتهت الجلسة! أنت الآن فارس حقيقي.")
st.markdown("</div>", unsafe_allow_html=True)
