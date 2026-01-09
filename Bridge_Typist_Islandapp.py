import streamlit as st
import random
import time
from streamlit_autorefresh import st_autorefresh

# --- CONFIG ---
KATA_LIST = ["APEL", "BUKU", "LAUT", "POHON", "PULAU", "PASIR", "KAPAL", "OMBAK", "KELAPA", "JEMBATAN", "PENJELAJAH", "STRATEGI", "KOMPUTER", "MATAHARI"]

st.set_page_config(page_title="Bridge Typist: Fixed Edition", layout="centered")

# Refresh timer tetap ada tapi lebih lambat (2 detik) agar tidak mengganggu input
st_autorefresh(interval=2000, key="timer_refresh")

# Inisialisasi State
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
    if "typing_box" in st.session_state:
        st.session_state.typing_box = ""

# --- TIMER ---
waktu_maksimal = max(15.0 - (st.session_state.pulau_ke * 0.5), 5.0) # Lebih lama
waktu_berjalan = time.time() - st.session_state.start_time
waktu_tersisa = waktu_maksimal - waktu_berjalan

st.title("🏝️ Bridge Typist: Safe Mode")

if not st.session_state.game_over:
    if waktu_tersisa <= 0:
        st.session_state.game_over = True
        st.rerun()

    st.metric("🏝️ Pulau", st.session_state.pulau_ke, f"⏳ {max(0.0, waktu_tersisa):.1f}s")
    st.progress(max(0.0, waktu_tersisa / waktu_maksimal))

    st.markdown(f"""
        <div style="text-align: center; background-color: #f0f2f6; padding: 20px; border-radius: 10px; border: 3px solid #3498db; margin-bottom: 10px;">
            <h1 style="color: #2c3e50; letter-spacing: 5px; font-family: monospace;">{st.session_state.kata_target}</h1>
        </div>
    """, unsafe_allow_html=True)

    # PERBAIKAN UTAMA: Menggunakan form agar input tidak terkirim sebelum kamu siap
    with st.form(key='typing_form', clear_on_submit=True):
        input_user = st.text_input("Ketik di bawah dan tekan tombol SEBERANGI:", key="typing_box").upper().strip()
        submit_button = st.form_submit_button(label='SEBERANGI! 🏃‍♂️')

    if submit_button:
        if input_user == st.session_state.kata_target:
            st.session_state.pulau_ke += 1
            st.session_state.kata_target = random.choice(KATA_LIST)
            st.session_state.start_time = time.time()
            st.success("Berhasil menyeberang!")
            time.sleep(0.5)
            st.rerun()
        else:
            st.session_state.game_over = True
            st.rerun()

else:
    st.error("🌊 BYURRR! Kamu jatuh ke laut!")
    st.write(f"### Skor Kamu: {st.session_state.pulau_ke} Pulau")
    if st.button("Coba Lagi 🔄"):
        reset_game()
        st.rerun()
