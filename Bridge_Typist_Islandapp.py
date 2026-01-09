import streamlit as st
import random
import time
from streamlit_autorefresh import st_autorefresh

# --- CONFIG & BANK KATA ---
KATA_LIST = [
    "MATAHARI", "PASIR", "PULAU", "BUKU", "JEMBATAN", "STRATEGI", 
    "KOMPUTER", "PENJELAJAH", "SAMUDRA", "PEROMPAK", "HARTA", "KARUN",
    "MERDEKA", "CAKRAWALA", "SAHABAT", "MISTERI", "GURITA", "HIU", "KARANG"
]

st.set_page_config(page_title="Bridge Typist: Animated", layout="centered")

# CSS untuk Animasi (Karakter Bergoyang & Jembatan Muncul)
st.markdown("""
<style>
    @keyframes walking {
        0% { transform: translateY(0px) rotate(0deg); }
        50% { transform: translateY(-10px) rotate(5deg); }
        100% { transform: translateY(0px) rotate(0deg); }
    }
    .char-animation {
        display: inline-block;
        animation: walking 0.5s infinite;
        font-size: 50px;
    }
    .sea-box {
        background: linear-gradient(180deg, #4da6ff 0%, #0066cc 100%);
        padding: 30px;
        border-radius: 20px;
        height: 150px;
        position: relative;
        overflow: hidden;
        border: 4px solid #fff;
    }
</style>
""", unsafe_allow_html=True)

st_autorefresh(interval=1000, key="timer_refresh")

if 'pulau_ke' not in st.session_state:
    st.session_state.pulau_ke = 0
    st.session_state.kata_target = random.choice(KATA_LIST)
    st.session_state.game_over = False
    st.session_state.start_time = time.time()

def reset_game():
    st.session_state.pulau_ke = 0
    st.session_state.kata_target = random.choice(KATA_LIST)
    st.session_state.game_over = False
    st.session_state.start_time = time.time()

# --- LOGIKA ---
waktu_maksimal = max(15.0 - (st.session_state.pulau_ke * 0.5), 5.0)
waktu_berjalan = time.time() - st.session_state.start_time
waktu_tersisa = waktu_maksimal - waktu_berjalan

st.title("🏴‍☠️ Bridge Typist Animated")

if not st.session_state.game_over:
    if waktu_tersisa <= 0:
        st.session_state.game_over = True
        st.rerun()

    # --- VISUALISASI ANIMASI ---
    # Karakter akan bergeser ke kanan setiap naik level
    posisi_x = min(10 + (st.session_state.pulau_ke * 15), 80)
    
    st.markdown(f"""
        <div class="sea-box">
            <div style="position: absolute; left: 5px; bottom: 20px; font-size: 40px;">🏝️</div>
            <div style="position: absolute; right: 5px; bottom: 20px; font-size: 40px;">🏝️</div>
            <div style="position: absolute; left: 40px; right: 40px; bottom: 35px; border-top: 8px dashed #8b4513; opacity: 0.6;"></div>
            <div class="char-animation" style="position: absolute; left: {posisi_x}%; bottom: 40px;">🏃‍♂️</div>
        </div>
    """, unsafe_allow_html=True)

    st.write(f"### 🚩 Level: Pulau {st.session_state.pulau_ke}")
    st.progress(max(0.0, waktu_tersisa / waktu_maksimal))

    # Tampilan Kata
    st.markdown(f"""
        <div style="text-align: center; margin: 20px; padding: 20px; background: #fff; border-radius: 10px; box-shadow: 0px 4px 10px rgba(0,0,0,0.1);">
            <h1 style="letter-spacing: 8px; color: #2c3e50;">{st.session_state.kata_target}</h1>
        </div>
    """, unsafe_allow_html=True)

    with st.form(key='typing_form', clear_on_submit=True):
        input_user = st.text_input("Ketik & Tekan Enter:", key="typing_box").upper().strip()
        submit = st.form_submit_button("LONCAT! 🚀")

    if submit:
        if input_user == st.session_state.kata_target:
            st.session_state.pulau_ke += 1
            st.session_state.kata_target = random.choice(KATA_LIST)
            st.session_state.start_time = time.time()
            st.rerun()
        else:
            st.session_state.game_over = True
            st.rerun()
else:
    # Animasi Jatuh
    st.markdown("""
        <div style="text-align: center;">
            <h1 style="font-size: 100px;">🌊😵</h1>
            <h2 style="color: red;">BYURRR! Jembatan Rubuh!</h2>
        </div>
    """, unsafe_allow_html=True)
    st.subheader(f"Skor Akhir: {st.session_state.pulau_ke} Pulau")
    if st.button("Coba Lagi 🔄"):
        reset_game()
        st.rerun()
