import streamlit as st
import random
import time
from streamlit_autorefresh import st_autorefresh

# --- PENGATURAN GAME ---
KATA_LIST = ["APEL", "BUKU", "LAUT", "POHON", "PULAU", "PASIR", "KAPAL", "OMBAK", "KELAPA", "JEMBATAN", "PENJELAJAH", "STRATEGI", "KOMPUTER", "MATAHARI", "AKURASI", "KOLABORASI", "OKSIGEN", "MARITIM"]

st.set_page_config(page_title="Bridge Typist: Island Hopper", layout="centered")

# Auto-refresh setiap 1 detik untuk timer (lebih stabil dari 0.1s)
st_autorefresh(interval=1000, key="datarefresh")

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

# --- LOGIKA WAKTU ---
waktu_maksimal = max(10.0 - (st.session_state.pulau_ke * 0.5), 3.0) # Lebih longgar di awal
waktu_berjalan = time.time() - st.session_state.start_time
waktu_tersisa = waktu_maksimal - waktu_berjalan

# --- TAMPILAN UTAMA ---
st.title("🏝️ Bridge Typist: Island Hopper")

if not st.session_state.game_over:
    # Cek Waktu Habis
    if waktu_tersisa <= 0:
        st.session_state.game_over = True
        st.rerun()

    # Header Informasi
    c1, c2 = st.columns(2)
    c1.metric("🏝️ Pulau", st.session_state.pulau_ke)
    c2.metric("⏳ Sisa Waktu", f"{max(0.0, waktu_tersisa):.1f}s")
    
    st.progress(max(0.0, waktu_tersisa / waktu_maksimal))

    # Kotak Kata
    st.markdown(f"""
        <div style="text-align: center; background-color: #fdfefe; padding: 25px; border-radius: 15px; border: 3px solid #3498db; margin-bottom: 20px;">
            <h1 style="color: #2980b9; letter-spacing: 5px; font-family: 'Courier New', monospace;">{st.session_state.kata_target}</h1>
        </div>
    """, unsafe_allow_html=True)

    # Input User - Menggunakan on_change agar lebih stabil
    input_user = st.text_input("Ketik di sini (TEKAN ENTER SETELAH SELESAI):", key="typing_box").upper().strip()

    if input_user:
        target = st.session_state.kata_target
        # CEK: Jika ketikan benar dan sudah selesai
        if input_user == target:
            st.session_state.pulau_ke += 1
            st.session_state.kata_target = random.choice(KATA_LIST)
            st.session_state.start_time = time.time()
            st.rerun()
        # CEK: Jika yang diketik salah (huruf tidak sesuai urutan)
        elif not target.startswith(input_user):
            st.session_state.game_over = True
            st.rerun()

else:
    # --- GAME OVER ---
    if waktu_tersisa <= 0:
        st.error("⏰ WAKTU HABIS! Jembatannya rubuh karena kamu kelamaan!")
    else:
        st.error(f"🌊 BYURRR! Salah ketik! Kamu tadi mengetik: '{st.session_state.typing_box}'")
        
    st.write(f"### Skor Akhir: {st.session_state.pulau_ke} Pulau")
    
    if st.session_state.pulau_ke > st.session_state.skor_tertinggi:
        st.session_state.skor_tertinggi = st.session_state.pulau_ke
        st.balloons()
        st.success(f"🔥 REKOR BARU! {st.session_state.skor_tertinggi}")
    
    if st.button("COBA LAGI 🔄"):
        reset_game()
        st.rerun()
