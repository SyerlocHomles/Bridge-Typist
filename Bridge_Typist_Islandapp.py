import streamlit as st
import random
import time
from streamlit_autorefresh import st_autorefresh

# --- 1. BANK KATA YANG LEBIH BANYAK ---
KATA_LIST = [
    "APEL", "BUKU", "LAUT", "POHON", "PULAU", "PASIR", "KAPAL", "OMBAK", "KELAPA", 
    "JEMBATAN", "STRATEGI", "MATAHARI", "KOMPUTER", "PENJELAJAH", "BINTANG", "DUNIA",
    "KEBERANIAN", "PETUALANGAN", "SAMUDRA", "BAJAK", "PEROMPAK", "HARTA", "KARUN",
    "MERDEKA", "INDONESIA", "CEMERLANG", "CAKRAWALA", "SAHABAT", "KELUARGA", "PINTAR",
    "BELAJAR", "KREATIF", "MISTERI", "LEGENDA", "RAKSASA", "GURITA", "HIU", "KARANG"
]

st.set_page_config(page_title="Bridge Typist: Adventure Mode", layout="centered")

# Auto-refresh untuk timer
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

# --- LOGIKA GAME ---
waktu_maksimal = max(15.0 - (st.session_state.pulau_ke * 0.4), 4.0)
waktu_berjalan = time.time() - st.session_state.start_time
waktu_tersisa = waktu_maksimal - waktu_berjalan

st.title("🏴‍☠️ Bridge Typist: Adventure")

if not st.session_state.game_over:
    if waktu_tersisa <= 0:
        st.session_state.game_over = True
        st.rerun()

    # --- 2. ANIMASI KARAKTER (VISUAL) ---
    # Membuat animasi sederhana karakter yang berjalan menuju pulau
    posisi = min(st.session_state.pulau_ke * 10, 90) # Biar tidak lewat layar
    
    st.markdown(f"""
        <div style="background-color: #87CEEB; padding: 20px; border-radius: 15px; text-align: left; overflow: hidden; position: relative; height: 120px; border: 3px solid #2980b9;">
            <div style="font-size: 40px; position: absolute; left: 5px; bottom: 10px;">🏝️</div>
            <div style="font-size: 50px; position: absolute; left: 45%; bottom: 20px; transition: all 0.5s;">{"🌉" if st.session_state.pulau_ke > 0 else ""}</div>
            <div style="font-size: 40px; position: absolute; left: {posisi}%; bottom: 15px; transition: all 1s ease-in-out;">🏃‍♂️💨</div>
            <div style="font-size: 40px; position: absolute; right: 5px; bottom: 10px;">🏝️</div>
        </div>
    """, unsafe_allow_html=True)

    st.write(f"### 🏝️ Pulau ke-{st.session_state.pulau_ke}")
    st.progress(max(0.0, waktu_tersisa / waktu_maksimal))
    st.caption(f"Sisa Waktu: {max(0.0, waktu_tersisa):.1f} detik")

    st.markdown(f"""
        <div style="text-align: center; background: white; padding: 20px; border-radius: 10px; border: 4px dashed #e67e22; margin: 20px 0;">
            <h1 style="color: #d35400; letter-spacing: 10px; font-family: 'Courier New';">{st.session_state.kata_target}</h1>
        </div>
    """, unsafe_allow_html=True)

    with st.form(key='typing_form', clear_on_submit=True):
        input_user = st.text_input("Ketik kata di atas dan tekan Enter:", key="typing_box").upper().strip()
        submit = st.form_submit_button("SEBERANGI! 🚀")

    if submit:
        if input_user == st.session_state.kata_target:
            st.session_state.pulau_ke += 1
            st.session_state.kata_target = random.choice(KATA_LIST)
            st.session_state.start_time = time.time()
            st.balloons()
            st.rerun()
        else:
            st.session_state.game_over = True
            st.rerun()
else:
    # --- GAME OVER DENGAN ANIMASI ---
    st.markdown("<h1 style='text-align: center; color: red;'>BYURRR! 🌊😵</h1>", unsafe_allow_html=True)
    st.error(f"Kamu terjatuh di Pulau ke-{st.session_state.pulau_ke}!")
    
    if st.button("MULAI LAGI 🔄"):
        reset_game()
        st.rerun()
