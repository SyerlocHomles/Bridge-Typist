import streamlit as st
import random
import time
from streamlit_autorefresh import st_autorefresh

# --- CONFIG & KATA ---
KATA_LIST = ["MATAHARI", "PASIR", "PULAU", "BUKU", "JEMBATAN", "STRATEGI", "KOMPUTER", "SAMUDRA", "GURITA", "HIU", "KARANG"]

st.set_page_config(page_title="Ship Navigator", layout="centered")

# CSS untuk Animasi Smooth & Tampilan Laut
st.markdown("""
<style>
    .ocean {
        background: #0077be;
        height: 300px;
        border-radius: 15px;
        position: relative;
        overflow: hidden;
        border: 5px solid #004d7a;
    }
    .ship {
        font-size: 50px;
        position: absolute;
        bottom: 20px;
        transition: left 0.5s ease-in-out, transform 0.3s;
    }
    .rock {
        font-size: 60px;
        position: absolute;
        top: 20px;
        transition: all 0.5s;
    }
    @keyframes wave {
        0% { transform: translateX(0); }
        50% { transform: translateX(-10px); }
        100% { transform: translateX(0); }
    }
    .water-effect {
        animation: wave 2s infinite;
        opacity: 0.3;
        font-size: 100px;
        position: absolute;
        top: 50%;
    }
</style>
""", unsafe_allow_html=True)

st_autorefresh(interval=1000, key="timer_refresh")

# Inisialisasi State
if 'posisi_kapal' not in st.session_state:
    st.session_state.posisi_kapal = "tengah" # kiri, tengah, kanan
    st.session_state.posisi_batu = random.choice(["kiri", "kanan"])
    st.session_state.kata_target = random.choice(KATA_LIST)
    st.session_state.skor = 0
    st.session_state.game_over = False
    st.session_state.start_time = time.time()

def reset_game():
    st.session_state.posisi_kapal = "tengah"
    st.session_state.skor = 0
    st.session_state.game_over = False
    st.session_state.start_time = time.time()
    st.session_state.kata_target = random.choice(KATA_LIST)

# Logika Waktu
waktu_maksimal = max(10.0 - (st.session_state.skor * 0.3), 3.0)
waktu_tersisa = waktu_maksimal - (time.time() - st.session_state.start_time)

st.title("🚢 Ship Navigator: Rock Evader")

if not st.session_state.game_over:
    if waktu_tersisa <= 0:
        st.session_state.game_over = True
        st.rerun()

    # Tentukan koordinat CSS berdasarkan state
    # Kapal menghindari batu: Jika batu di kanan, kapal harus ke kiri
    pos_css = {"kiri": "15%", "tengah": "45%", "kanan": "75%"}
    ship_left = pos_css[st.session_state.posisi_kapal]
    rock_left = pos_css[st.session_state.posisi_batu]

    # --- VISUALISASI LAUT ---
    st.markdown(f"""
        <div class="ocean">
            <div class="water-effect">🌊🌊🌊🌊🌊🌊</div>
            <div class="rock" style="left: {rock_left};">🪨</div>
            <div class="ship" style="left: {ship_left};">🚢</div>
        </div>
    """, unsafe_allow_html=True)

    st.write(f"### 🎯 Skor: {st.session_state.skor} | ⏳ {max(0.0, waktu_tersisa):.1f}s")
    
    st.info(f"AWAS! Ada batu di sebelah **{st.session_state.posisi_batu.upper()}**! Ketik kata di bawah untuk menghindar ke arah berlawanan!")

    st.markdown(f"""
        <div style="text-align: center; background: #fdfefe; padding: 15px; border-radius: 10px; border: 2px solid #3498db;">
            <h2 style="letter-spacing: 5px;">{st.session_state.kata_target}</h2>
        </div>
    """, unsafe_allow_html=True)

    with st.form(key='nav_form', clear_on_submit=True):
        input_user = st.text_input("Ketik dengan benar untuk bermanuver:").upper().strip()
        submit = st.form_submit_button("MANUVER SEKARANG! ⚙️")

    if submit:
        if input_user == st.session_state.kata_target:
            # Berhasil! Kapal pindah ke posisi aman
            if st.session_state.posisi_batu == "kanan":
                st.session_state.posisi_kapal = "kiri"
            else:
                st.session_state.posisi_kapal = "kanan"
            
            st.session_state.skor += 1
            st.session_state.kata_target = random.choice(KATA_LIST)
            st.session_state.posisi_batu = random.choice(["kiri", "kanan"])
            st.session_state.start_time = time.time()
            st.rerun()
        else:
            st.session_state.game_over = True
            st.rerun()
else:
    st.error(f"💥 BRAKKK! Kapal menabrak batu! Skor akhir: {st.session_state.skor}")
    if st.button("Perbaiki Kapal & Mulai Lagi 🛠️"):
        reset_game()
        st.rerun()
