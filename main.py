import streamlit as st
import pandas as pd
import google.generativeai as genai
import time

# 1. إعداد الصفحة مع فرض اتجاه النص العربي
st.set_page_config(page_title="فرسان رمضان", page_icon="🌙", layout="centered")

# 2. تحسين الواجهة وتثبيت المربعات (CSS المطور)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo&display=swap');
    html, body, [class*="st-"] { font-family: 'Cairo', sans-serif; text-align: right; direction: rtl !important; }
    
    /* تثبيت أحجام مربعات النص ومنع التداخل */
    .stTextInput>div>div>input, .stSelectbox>div {
        text-align: right; direction: rtl; min-height: 45px; border: 1px solid #d4af37 !important;
    }
    
    /* تصميم البطاقات الموحد */
    .stExpander { border: 1px solid #d4af37; border-radius: 10px; background-color: rgba(212, 175, 55, 0.05); }
    
    /* تنسيق العناوين */
    h1, h2, h3 { color: #f9d976 !important; margin-bottom: 20px; }
    
    /* إخفاء عناصر التداخل في الأندرويد */
    .stActionButton { display: none; }
    </style>
    """, unsafe_allow_html=True)

# 3. الربط مع الذكاء الاصطناعي (تأكد من كتابة المفتاح بدقة)
# وضعنا 'gemini-1.5-flash' لأنه الأسرع والأكثر استقراراً حالياً
try:
    genai.configure(api_key="AIzaSyAcsMKzB2rZC-dPjcSzUFq6WxokPsewUMo")
    model = genai.GenerativeModel('gemini-1.5-flash')
except:
    st.error("خطأ في ربط مفتاح الذكاء الاصطناعي")

st.markdown("<h1 style='text-align: center;'>🌙 منصة فرسان رمضان</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>خطوتك نحو التطوير الإداري والنمو الذاتي</p>", unsafe_allow_html=True)

# 4. المساعد الذكي (المكان المطور)
with st.expander("🤖 اطلب خطة من المساعد الذكي", expanded=False):
    st.write("اسأل المساعد ليقترح عليك خطة لمهارة اليوم")
    user_input = st.text_input("مثلاً: اقترح لي خطة 20 دقيقة لتعلم المونتاج", key="ai_input")
    if st.button("الحصول على إجابة", key="ai_btn"):
        if user_input:
            try:
                with st.spinner('جاري التفكير...'):
                    # صياغة الأمر (Prompt) ليكون المساعد دقيقاً
                    prompt = f"بصفتك خبير تطوير إداري، اقترح خطة عملية ومختصرة جداً في 3 نقاط لـ: {user_input}"
                    response = model.generate_content(prompt)
                    st.info(response.text)
            except Exception as e:
                st.error("عذراً، المساعد يحتاج لإعادة ضبط المفتاح أو هناك ضغط على الخدمة.")
        else:
            st.warning("يرجى كتابة سؤالك أولاً")

# 5. تسجيل الإنجاز (مربعات ثابتة)
st.divider()
st.subheader("📝 تسجيل إنجاز اليوم")
name = st.text_input("اسم الفارس", key="user_name")

skill = st.selectbox("اختر المهارة", ["هندسة الأوامر AI", "المونتاج", "أخرى"], key="skill_sel")
if skill == "أخرى":
    skill = st.text_input("اكتب مهارتك هنا", key="custom_skill")

habit = st.selectbox("اختر العادة", ["العمل العميق", "شرب الماء", "أخرى"], key="habit_sel")
if habit == "أخرى":
    habit = st.text_input("اكتب عادتك هنا", key="custom_habit")

if st.button("✅ حفظ الإنجاز وكسب 20 نقطة"):
    if name:
        st.success(f"أحسنت يا {name}! تم الحفظ.")
        st.balloons()
    else:
        st.error("يرجى كتابة الاسم")
# 6. لوحة الصدارة التلقائية (تظهر في الأسفل دائماً)
st.divider()
st.markdown("<h2 style='text-align: center;'>🏆 لوحة صدارة الفرسان</h2>", unsafe_allow_html=True)

# إدارة البيانات في الذاكرة (Session State) لضمان ثبات النقاط أثناء التصفح
if 'leaderboard_data' not in st.session_state:
    st.session_state.leaderboard_data = {}

# تحديث البيانات عند الضغط على زر الحفظ
if st.button("تحديث النقاط وعرض الترتيب"):
    if name:
        if name in st.session_state.leaderboard_data:
            st.session_state.leaderboard_data[name] += 20
        else:
            st.session_state.leaderboard_data[name] = 20
        st.success(f"تم تحديث رصيد {name}!")
    else:
        st.warning("سجل إنجازك أولاً لتظهر في لوحة الصدارة")

# عرض لوحة الصدارة بشكل أنيق
if st.session_state.leaderboard_data:
    sorted_data = dict(sorted(st.session_state.leaderboard_data.items(), key=lambda item: item[1], reverse=True))
    for i, (knight, score) in enumerate(sorted_data.items()):
        rank_icon = "🥇" if i == 0 else "🥈" if i == 1 else "🥉" if i == 2 else "🎖️"
        st.markdown(f"""
        <div style='background: rgba(212, 175, 55, 0.1); padding: 10px; border-radius: 10px; border-right: 5px solid #d4af37; margin: 5px 0;'>
            <span style='font-size: 1.2rem;'>{rank_icon} <b>{knight}</b></span>
            <span style='float: left; color: #f9d976; font-weight: bold;'>{score} نقطة</span>
        </div>
        """, unsafe_allow_html=True)
else:
    st.info("لا توجد بيانات حالياً، كن أول فارس يسجل إنجازه!")
