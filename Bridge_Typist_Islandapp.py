import streamlit as st
import random
import time
from streamlit_autorefresh import st_autorefresh

# --- CONFIG ---
KATA_LIST = ["APEL", "BUKU", "LAUT", "POHON", "PULAU", "PASIR", "KAPAL", "OMBAK", "KELAPA", "JEMBATAN", "PENJELAJAH", "STRATEGI", "KOMPUTER", "MATAHARI"]

st.set_page_config(page_title="Bridge Typist", layout="centered")

# Refresh setiap 1 detik untuk timer
st_autorefresh(interval=1000, key="timer_refresh")

if 'pulau_ke' not in st.session_state:
    st.session_state.pulau_ke = 0
    st.session_state.kata_target = random.choice(KATA_LIST)
    st.session_state.game_over = False
    st.session_state.skor_tertinggi = 0
    st.session_state.start_time = time.time()

def reset_game():
    st.session_state.pulau_ke = 0
    st.session_state.kata_target = random.choice(KATA_LIST)
    st.session_state.game_over = False
    st.session_state.start_time = time.time()

# --- TIMER ---
waktu_maksimal = max(12.0 - (st.session_state.pulau_ke * 0.5), 4.0)
waktu_berjalan = time.time() - st.session_state.start_time
waktu_tersisa = waktu_maksimal - waktu_berjalan

st.title("🏝️ Bridge Typist")

if not st.session_state.game_over:
    if waktu_tersisa <= 0:
        st.session_state.game_over = True
        st.rerun()

    st.metric("🏝️ Pulau", st.session_state.pulau_ke, f"⏳ {max(0.0, waktu_tersisa):.1f}s")
    st.progress(max(0.0, waktu_tersisa / waktu_maksimal))

    st.markdown(f"""
        <div style="text-align: center; background-color: #f0f2f6; padding: 20px; border-radius: 10px; border: 2px solid #3498db;">
            <h1 style="color: #2c3e50; letter-spacing: 5px;">{st.session_state.kata_target}</h1>
        </div>
    """, unsafe_allow_html=True)

    # Input menggunakan on_change agar tidak gampang error saat mengetik
    input_user = st.text_input("Ketik di sini & Tekan ENTER:", key="input_box").upper().strip()

    if input_user:
        if input_user == st.session_state.kata_target:
            st.session_state.pulau_ke += 1
            st.session_state.kata_target = random.choice(KATA_LIST)
            st.session_state.start_time = time.time()
            st.rerun()
        elif not st.session_state.kata_target.startswith(input_user):
            st.session_state.game_over = True
            st.rerun()
else:
    st.error("🌊 BYURRR! Jembatan Rubuh!")
    st.write(f"### Skor: {st.session_state.pulau_ke} Pulau")
    if st.button("Main Lagi 🔄"):
        reset_game()
        st.rerun()
