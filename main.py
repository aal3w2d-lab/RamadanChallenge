import streamlit as st
import pandas as pd
import urllib.parse
from datetime import datetime

# 1. إعدادات الصفحة والهوية البصرية
st.set_page_config(page_title="Ramadan Knights | فرسان رمضان", page_icon="🌙", layout="centered")

st.markdown("""
    <style>
    .main { background-color: #0e1117; color: #ffffff; }
    .stButton>button { width: 100%; border-radius: 20px; background-color: #f0c04a; color: black; font-weight: bold; height: 3em; }
    .stTextInput>div>div>input { background-color: #1a1c24; color: white; border: 1px solid #f0c04a; }
    h1, h2, h3 { text-align: center; color: #f0c04a; font-family: 'Cairo', sans-serif; }
    div.stStatusWidget { visibility: hidden; }
    </style>
    """, unsafe_allow_html=True)

# 2. بنك الأفكار (Bilingual Content)
skills_list = ["AI Prompting | هندسة الأوامر", "Video Editing | المونتاج", "Speed Reading | القراءة السريعة", "Public Speaking | الإلقاء", "Financial Planning | التخطيط المالي"]
habits_list = ["Deep Work | العمل العميق", "Daily Gratitude | الامتنان اليومي", "Hydration | شرب الماء بانتظام", "Digital Detox | الانقطاع الرقمي", "Immediate Order | الترتيب الفوري"]
impact_list = ["Knowledge Seed | بذرة المعرفة", "Eco-friendly | مبادرة صديق البيئة", "Family Archive | توثيق ذاكرة العائلة", "Kindness Messages | رسائل الشكر"]

# 3. إدارة البيانات (Simple Session State for Demo)
if 'family_data' not in st.session_state:
    st.session_state.family_data = pd.DataFrame(columns=["Name", "Skill", "Habit", "Points"])

# 4. واجهة التطبيق
st.title("🌙 Ramadan Knights Challenge")
st.subheader("تحدي فرسان رمضان لعام 1447هـ")

# تسجيل فرد جديد
with st.expander("👤 Register New Member | تسجيل فرد جديد"):
    new_name = st.text_input("Enter Name | أدخل الاسم")
    col1, col2 = st.columns(2)
    with col1:
        chosen_skill = st.selectbox("Choose Skill | اختر مهارة", skills_list)
    with col2:
        chosen_habit = st.selectbox("Choose Habit | اختر عادة", habits_list)
    
    if st.button("Join Challenge | انضم للتحدي"):
        if new_name and new_name not in st.session_state.family_data["Name"].values:
            new_row = {"Name": new_name, "Skill": chosen_skill, "Habit": chosen_habit, "Points": 0}
            st.session_state.family_data = pd.concat([st.session_state.family_data, pd.DataFrame([new_row])], ignore_index=True)
            st.success(f"Welcome {new_name}! | أهلاً بك يا {new_name}!")
        else:
            st.warning("Please enter a unique name. | يرجى إدخال اسم جديد.")

# تسجيل الإنجاز اليومي
st.divider()
if not st.session_state.family_data.empty:
    current_user = st.selectbox("Who is recording? | من الذي يسجل الآن؟", st.session_state.family_data["Name"])
    
    st.write(f"### Welcome, {current_user}! | أهلاً بك")
    c1, c2 = st.columns(2)
    with c1:
        s_check = st.checkbox("20 min Skill done | أتممت المهارة")
    with c2:
        h_check = st.checkbox("Habit maintained | التزمت بالعادة")
    
    impact_note = st.text_input("Daily Impact Note | أثر اليوم (خاطرة أو فعل خيّر)")

    if st.button("🚀 Save & Share | حفظ ومشاركة"):
        points_earned = (10 if s_check else 0) + (10 if h_check else 0)
        st.session_state.family_data.loc[st.session_state.family_data["Name"] == current_user, "Points"] += points_earned
        
        # تجهيز رسالة الواتساب
        message = f"🌙 *تحدي فرسان رمضان* 🌙\n\nالبطل: *{current_user}*\n✅ أتممت إنجازي اليوم بنجاح!\n⭐ النقاط المكتسبة: {points_earned}\n🌱 الأثر: {impact_note}\n\n_نصنع مستقبلنا في رمضان!_"
        whatsapp_url = f"https://wa.me/?text={urllib.parse.quote(message)}"
        
        st.balloons()
        st.markdown(f'''
            <a href="{whatsapp_url}" target="_blank" style="text-decoration: none;">
                <div style="background-color: #25D366; color: white; padding: 10px; border-radius: 10px; text-align: center; font-weight: bold;">
                    Share on WhatsApp Group | شارك في قروب العائلة
                </div>
            </a>
            ''', unsafe_allow_html=True)

# لوحة الصدارة
st.divider()
st.header("🏆 Leaderboard | لوحة الصدارة")
st.table(st.session_state.family_data[["Name", "Points"]].sort_values(by="Points", ascending=False))

st.caption("Designed for Family Growth | صُمم لتطوير العائلة - 2026")
