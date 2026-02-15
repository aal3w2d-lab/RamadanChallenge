import streamlit as st
import pandas as pd
import google.generativeai as genai
import urllib.parse
from datetime import datetime
import time

# 1. إعدادات الهوية البصرية الملكية
st.set_page_config(page_title="منظومة فرسان رمضان الرقمية", page_icon="🌙", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    html, body, [class*="st-"] { font-family: 'Cairo', sans-serif; text-align: right; direction: rtl !important; }
    .main { background: linear-gradient(180deg, #001a11 0%, #002b1b 100%); color: #fdfdfd; }
    .stButton>button { 
        background: linear-gradient(90deg, #d4af37 0%, #f9d976 100%); 
        color: #001a11 !important; border-radius: 20px; font-weight: bold; border: none; width: 100%;
    }
    .card { background: rgba(255, 255, 255, 0.05); padding: 20px; border-radius: 15px; border: 1px solid #d4af37; margin-bottom: 20px; }
    .admin-section { border: 2px solid #ff4b4b; padding: 15px; border-radius: 10px; margin-top: 20px; }
    </style>
    """, unsafe_allow_html=True)

# 2. حوكمة البيانات (قاعدة البيانات المؤقتة)
if 'teams' not in st.session_state:
    st.session_state.teams = {"فريق الصقور": [], "فرسان مكة": []}
if 'pending_tasks' not in st.session_state:
    st.session_state.pending_tasks = []
if 'final_scores' not in st.session_state:
    st.session_state.final_scores = {}

# 3. إعداد المساعد الذكي
genai.configure(api_key="AIzaSyA0cI8HTLo0XRkzAdqV3BfQEAiLnVLARvs")
model = genai.GenerativeModel('gemini-1.5-flash')

# --- الواجهة الرئيسية ---
st.markdown("<h1 style='text-align: center;'>⚔️ منظومة فرسان رمضان المتكاملة</h1>", unsafe_allow_html=True)

# 4. المساعد الذكي وربط القرآن
with st.expander("🤖 المساعد الذكي ومركز التلاوة"):
    col_ai1, col_ai2 = st.columns(2)
    with col_ai1:
        st.markdown("""<a href="intent://#Intent;scheme=quran;package=com.quran.labs.androidquran;end" target="_blank">
            <button style="width:100%; padding:10px; background-color:#d4af37; border:none; border-radius:10px; cursor:pointer;">📖 فتح تطبيق القرآن</button>
            </a>""", unsafe_allow_html=True)
    with col_ai2:
        u_query = st.text_input("اسأل المساعد عن خطة أو تفسير")
        if st.button("استشارة"):
            res = model.generate_content(f"كخبير تطوير إداري، أجب باختصار: {u_query}")
            st.info(res.text)

# 5. سوق الفرق والتسجيل (الألعاب الجماعية)
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.subheader("🏟️ ساحة الفرق الجماعية")
col_reg1, col_reg2 = st.columns(2)
with col_reg1:
    selected_team = st.selectbox("اختر فريقك للمنافسة", list(st.session_state.teams.keys()))
with col_reg2:
    player_name = st.text_input("اسمك الكريم")

st.markdown("---")
st.write("📝 **تسجيل الإنجاز (نقطة لكل وحدة)**")
col_in1, col_in2, col_in3 = st.columns(3)
with col_in1:
    category = st.selectbox("النشاط", ["أذكار", "قرآن (وجه)", "أحاديث", "فعل خير"])
with col_in2:
    amount = st.number_input("العدد المنجز", min_value=1)
with col_in3:
    proof_link = st.text_input("إثبات/ملاحظة (للحوكمة)")

if st.button("🚀 تسجيل وإرسال للتدقيق"):
    if player_name:
        task = {
            "name": player_name, "team": selected_team, 
            "pts": amount, "cat": category, "proof": proof_link,
            "status": "معلق"
        }
        st.session_state.pending_tasks.append(task)
        # ربط الواتساب
        msg = urllib.parse.quote(f"🛡️ إثبات جديد: {player_name}\nالنشاط: {category}\nالعدد: {amount}")
        st.markdown(f'<a href="https://wa.me/?text={msg}" target="_blank">📲 أرسل الإثبات لمجموعة الواتساب</a>', unsafe_allow_html=True)
        st.success("تم الإرسال بنجاح.. بانتظار اعتماد القائد.")
st.markdown("</div>", unsafe_allow_html=True)

# 6. لوحة تحكم القائد (Admin Control)
st.sidebar.markdown("---")
admin_key = st.sidebar.text_input("قفل الحوكمة 🔐", type="password")
if admin_key == "1234":
    st.markdown("<div class='admin-section'>", unsafe_allow_html=True)
    st.header("🕵️ مركز تدقيق الاستحقاق")
    for i, t in enumerate(st.session_state.pending_tasks):
        st.write(f"🚩 {t['name']} ({t['team']}): {t['pts']} نقطة في {t['cat']}")
        c_app, c_rej = st.columns(2)
        if c_app.button(f"اعتماد ✅", key=f"a_{i}"):
            st.session_state.final_scores[t['team']] = st.session_state.final_scores.get(t['team'], 0) + t['pts']
            st.session_state.pending_tasks.pop(i)
            st.rerun()
        if c_rej.button(f"رفض ❌", key=f"r_{i}"):
            st.session_state.pending_tasks.pop(i)
            st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

# 7. التقارير ولوحة الصدارة الرسمية
st.header("🏆 لوحة الصدارة المعتمدة")
if st.session_state.final_scores:
    score_df = pd.DataFrame(st.session_state.final_scores.items(), columns=["الفريق", "إجمالي النقاط"])
    st.bar_chart(score_df.set_index("الفريق"))
    st.table(score_df.sort_values(by="إجمالي النقاط", ascending=False))
else:
    st.info("بانتظار اعتماد أولى النقاط من القائد.")
