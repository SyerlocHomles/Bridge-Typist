import streamlit as st
import random
import time

# --- PENGATURAN GAME ---
KATA_LIST = ["APEL", "BUKU", "LAUT", "POHON", "PULAU", "PASIR", "KAPAL", "OMBAK", "KELAPA", "JEMBATAN", "PENJELAJAH", "STRATEGI", "KOMPUTER", "MATAHARI", "AKURASI", "KOLABORASI", "OKSIGEN", "MARITIM"]

st.set_page_config(page_title="Bridge Typist: Extreme", layout="centered")

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
waktu_maksimal = max(8.0 - (st.session_state.pulau_ke * 0.3), 2.0)
waktu_berjalan = time.time() - st.session_state.start_time
waktu_tersisa = waktu_maksimal - waktu_berjalan

# --- TAMPILAN UTAMA ---
st.title("🏝️ Bridge Typist: Extreme Edition")

if not st.session_state.game_over:
    if waktu_tersisa <= 0:
        st.session_state.game_over = True
        st.rerun()

    cols = st.columns([3, 1])
    with cols[0]:
        st.subheader(f"🏝️ Pulau Ke: {st.session_state.pulau_ke}")
    with cols[1]:
        st.metric("⏳ Waktu", f"{max(0.0, waktu_tersisa):.1f}s")

    st.progress(max(0.0, waktu_tersisa / waktu_maksimal))

    st.markdown(f"""
        <div style="text-align: center; background-color: #fdfefe; padding: 25px; border-radius: 15px; border: 3px solid #e67e22;">
            <h1 style="color: #d35400; letter-spacing: 7px; font-family: monospace;">{st.session_state.kata_target}</h1>
        </div>
    """, unsafe_allow_html=True)

    input_user = st.text_input("Ketik di sini (Cepat!):", key="typing_input").upper()

    if input_user:
        target = st.session_state.kata_target
        if target.startswith(input_user):
            if input_user == target:
                st.session_state.pulau_ke += 1
                st.session_state.kata_target = random.choice(KATA_LIST)
                st.session_state.start_time = time.time() 
                st.rerun()
        else:
            st.session_state.game_over = True
            st.rerun()
    
    time.sleep(0.1)
    st.rerun()

else:
    # --- TAMPILAN GAME OVER ---
    if waktu_tersisa <= 0:
        st.error("⏰ WAKTU HABIS! Jembatannya rubuh!")
    else:
        st.error("🌊 BYURRR! Salah ketik!")
        
    st.write(f"### Skor Akhir: {st.session_state.pulau_ke} Pulau")
    
    if st.session_state.pulau_ke > st.session_state.skor_tertinggi:
        st.session_state.skor_tertinggi = st.session_state.pulau_ke
        st.balloons()
        st.success(f"🔥 REKOR BARU! {st.session_state.skor_tertinggi}")
    else:
        st.write(f"🏆 Rekor Tertinggi: {st.session_state.skor_tertinggi}")

    if st.button("MULAI LAGI 🔄"):
        reset_game()
        st.rerun()
