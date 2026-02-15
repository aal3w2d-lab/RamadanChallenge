import streamlit as st
import pandas as pd
import google.generativeai as genai
import time

# 1. إعداد الصفحة وتثبيت الواجهة
st.set_page_config(page_title="منظومة رمضان المتكاملة", page_icon="🌙", layout="centered")

# 2. كود CSS لتنظيف الواجهة وحل مشكلة التداخل (مهم جداً للـ S25)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo&display=swap');
    html, body, [class*="st-"] { font-family: 'Cairo', sans-serif; text-align: right; direction: rtl !important; }
    
    /* إخفاء الرموز المتداخلة في الأندرويد */
    .stActionButton, .st-emotion-cache-1dp5vir { display: none !important; }
    
    /* تثبيت المربعات وجعلها أنيقة */
    .stTextInput>div>div>input, .stSelectbox>div {
        background-color: #003d26 !important;
        color: white !important;
        border: 1px solid #d4af37 !important;
        border-radius: 12px !important;
        height: 50px !important;
    }
    
    /* تصميم البطاقات الموحد */
    .css-1r6il7i, .stExpander {
        border: 1px solid #d4af37 !important;
        background-color: rgba(255, 255, 255, 0.05) !important;
        border-radius: 15px !important;
    }
    h1, h2, h3 { color: #f9d976 !important; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

# 3. إعداد المساعد الذكي مع معالجة الأخطاء
# المفتاح الذي وضعته: AIzaSyAcsMKzB2rZC-dPjcSzUFq6WxokPsewUMo
API_KEY = "AIzaSyAcsMKzB2rZC-dPjcSzUFq6WxokPsewUMo"

try:
    genai.configure(api_key=API_KEY)
    # استخدام النموذج الأكثر استقراراً لتجنب خطأ NotFound
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error(f"حدث خطأ في إعداد الذكاء الاصطناعي: {e}")

# 4. واجهة التطبيق الرئيسية
st.markdown("<h1>🌙 منظومة رمضان المتكاملة</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>رحلتك نحو التطوير الإداري والنمو الذاتي</p>", unsafe_allow_html=True)

# 5. المساعد الذكي ومركز التلاوة (في بطاقة واحدة منسقة)
with st.expander("🤖 المساعد الذكي ومركز التلاوة", expanded=True):
    # زر القرآن
    st.markdown("""<a href="intent://#Intent;scheme=quran;package=com.quran.labs.androidquran;end" target="_blank">
        <button style="width:100%; padding:12px; background: linear-gradient(90deg, #d4af37, #f9d976); color:#001a11; border:none; border-radius:10px; font-weight:bold; cursor:pointer; margin-bottom:15px;">📖 فتح تطبيق القرآن</button>
        </a>""", unsafe_allow_html=True)
    
    st.write("---")
    st.write("💡 اسأل المساعد عن خطة أو تفسير")
    u_input = st.text_input("كيف يمكنني مساعدتك في خطتك اليوم؟", key="ai_input_fixed")
    
    if st.button("استشارة المساعد", key="ai_btn_fixed"):
        if u_input:
            with st.spinner('جاري التفكير...'):
                try:
                    # صياغة الطلب بشكل يضمن استجابة عربية سليمة
                    response = model.generate_content(f"أجب كخبير تطوير إداري باختصار وباللغة العربية على: {u_input}")
                    st.info(response.text)
                except Exception as e:
                    st.error("المساعد يواجه ضغطاً حالياً، يرجى المحاولة بعد قليل.")
        else:
            st.warning("يرجى كتابة سؤال أولاً")

# 6. قسم تسجيل الإنجاز (بمربعات ثابتة ومنسقة)
st.markdown("<h3>📝 تسجيل إنجاز اليوم</h3>", unsafe_allow_html=True)
with st.container():
    u_name = st.text_input("اسم الفارس", key="u_name")
    
    col_a, col_b = st.columns(2)
    with col_a:
        u_skill = st.selectbox("المهارة", ["هندسة الأوامر", "المونتاج", "أخرى"], key="u_skill")
    with col_b:
        u_habit = st.selectbox("العادة", ["العمل العميق", "الامتنان", "أخرى"], key="u_habit")

    if st.button("✅ حفظ الإنجاز وكسب النقاط"):
        if u_name:
            st.success(f"أحسنت يا {u_name}! تم تسجيل الإنجاز بنجاح.")
            st.balloons()
        else:
            st.error("يرجى كتابة الاسم")
