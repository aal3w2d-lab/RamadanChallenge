import streamlit as st
import pandas as pd
import urllib.parse
import google.generativeai as genai
import time
from datetime import datetime

# 1. إعدادات الهوية البصرية
st.set_page_config(page_title="Ramadan Knights | فرسان رمضان", page_icon="🌙", layout="centered")

st.markdown("""
    <style>
    .main { background-color: #002b1b; color: #fdfdfd; }
    .stButton>button { 
        background: linear-gradient(135deg, #d4af37 0%, #f9d976 100%); 
        color: #002b1b !important; border-radius: 15px; font-weight: bold;
    }
    .reward-card { background-color: #004d33; padding: 15px; border-radius: 10px; border: 1px dashed #d4af37; margin: 10px 0; }
    h1, h2, h3 { color: #f9d976 !important; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

# 2. إعداد الذكاء الاصطناعي AIzaSyAcsMKzB2rZC-dPjcSzUFq6WxokPsewUMo
genai.configure(api_key="AIzaSyAcsMKzB2rZC-dPjcSzUFq6WxokPsewUMo")
model = genai.GenerativeModel('gemini-1.5-flash')

# 3. إدارة البيانات
if 'history' not in st.session_state:
    st.session_state.history = []

# 4. واجهة التطبيق
st.title("🌙 Ramadan Knights Challenge")

# المساعد الذكي
with st.sidebar:
    st.header("🤖 AI Growth Mentor")
    ai_q = st.text_input("Ask for advice | اطلب نصيحة")
    if st.button("Ask AI"):
        resp = model.generate_content(f"كخبير تطوير إداري، أعط نصيحة قصيرة لـ: {ai_q}")
        st.info(resp.text)

# 5. تسجيل الإنجاز
st.header("1️⃣ Record Achievement")
user_name = st.text_input("Member Name | اسم الفرد")

col1, col2 = st.columns(2)
with col1:
    sel_skill = st.selectbox("Skill", ["AI Prompting", "Video Editing", "Other"])
    final_skill = st.text_input("Custom Skill") if sel_skill == "Other" else sel_skill
with col2:
    sel_habit = st.selectbox("Habit", ["Deep Work", "Hydration", "Other"])
    final_habit = st.text_input("Custom Habit") if sel_habit == "Other" else sel_habit

# 6. الحفظ وحساب النقاط
if st.button("✅ Save & Earn 20 Points!"):
    if user_name:
        entry = {"name": user_name, "date": datetime.now().strftime("%Y-%m-%d"), "pts": 20}
        st.session_state.history.append(entry)
        st.success(f"Bravo {user_name}! +20 Points")
        st.balloons()

# 7. لوحة الصدارة ونظام الحوافز
st.divider()
st.header("🏆 Leaderboard & Rewards")

if st.session_state.history:
    df = pd.DataFrame(st.session_state.history)
    leaderboard = df.groupby("name")["pts"].sum().sort_values(ascending=False).reset_index()
    
    for i, row in leaderboard.iterrows():
        name = row['name']
        points = row['pts']
        st.write(f"🥇 **{name}**: {points} Points")
        
        # نظام المكافآت المقترح إدارياً
        with st.expander(f"🎁 View Rewards for {name}"):
            if points >= 100:
                st.markdown("<div class='reward-card'>🌟 <b>الوسام الذهبي:</b> رحلة اختيارية أو هدية قيمة من القائد</div>", unsafe_allow_html=True)
            elif points >= 60:
                st.markdown("<div class='reward-card'>🥈 <b>الوسام الفضي:</b> إعفاء من مهمة منزلية لمدة يوم</div>", unsafe_allow_html=True)
            elif points >= 20:
                st.markdown("<div class='reward-card'>🥉 <b>وسام الفارس:</b> وجبة مفضلة أو وقت إضافي للهوايات</div>", unsafe_allow_html=True)
else:
    st.info("No records yet. Be the first knight!")

st.divider()
st.caption("صمم بواسطة باحث في التطوير الإداري لتعزيز النمو الذاتي")
