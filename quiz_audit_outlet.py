import streamlit as st
import random
import time

# ─── PAGE CONFIG ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Quiz Audit Outlet",
    page_icon="📋",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ─── CUSTOM CSS ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Plus Jakarta Sans', sans-serif;
}

/* Background */
.stApp {
    background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 50%, #0f172a 100%);
    min-height: 100vh;
}

/* Hide default streamlit elements */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 2rem; padding-bottom: 2rem; max-width: 780px; }

/* Card */
.quiz-card {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 20px;
    padding: 2rem;
    backdrop-filter: blur(10px);
    margin-bottom: 1.2rem;
}

/* Header badge */
.category-badge {
    display: inline-block;
    background: linear-gradient(90deg, #6366f1, #8b5cf6);
    color: white;
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    padding: 0.3rem 0.8rem;
    border-radius: 999px;
    margin-bottom: 0.8rem;
    font-family: 'JetBrains Mono', monospace;
}

/* Question text */
.question-text {
    color: #f1f5f9;
    font-size: 1.15rem;
    font-weight: 600;
    line-height: 1.6;
    margin: 0.5rem 0 1.2rem 0;
}

/* Progress bar custom */
.stProgress > div > div > div > div {
    background: linear-gradient(90deg, #6366f1, #a855f7) !important;
    border-radius: 999px;
}
.stProgress > div > div > div {
    background: rgba(255,255,255,0.08) !important;
    border-radius: 999px;
}

/* Buttons */
.stButton > button {
    width: 100%;
    background: rgba(255,255,255,0.06) !important;
    color: #e2e8f0 !important;
    border: 1.5px solid rgba(255,255,255,0.12) !important;
    border-radius: 12px !important;
    padding: 0.75rem 1rem !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-size: 0.95rem !important;
    font-weight: 500 !important;
    transition: all 0.2s ease !important;
    text-align: left !important;
    margin-bottom: 0.5rem;
}
.stButton > button:hover {
    background: rgba(99,102,241,0.25) !important;
    border-color: #6366f1 !important;
    color: white !important;
    transform: translateX(4px);
}

/* Correct / Wrong answer feedback */
.feedback-correct {
    background: rgba(34,197,94,0.15);
    border: 1.5px solid rgba(34,197,94,0.4);
    border-radius: 12px;
    padding: 1rem 1.2rem;
    color: #86efac;
    font-weight: 600;
    margin: 0.8rem 0;
}
.feedback-wrong {
    background: rgba(239,68,68,0.15);
    border: 1.5px solid rgba(239,68,68,0.4);
    border-radius: 12px;
    padding: 1rem 1.2rem;
    color: #fca5a5;
    font-weight: 600;
    margin: 0.8rem 0;
}
.explanation-box {
    background: rgba(99,102,241,0.12);
    border-left: 3px solid #6366f1;
    border-radius: 0 10px 10px 0;
    padding: 0.8rem 1rem;
    color: #c7d2fe;
    font-size: 0.9rem;
    line-height: 1.6;
    margin-top: 0.5rem;
}

/* Score card */
.score-card {
    text-align: center;
    padding: 2.5rem;
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.12);
    border-radius: 24px;
}
.score-big {
    font-size: 5rem;
    font-weight: 800;
    background: linear-gradient(135deg, #a5b4fc, #f0abfc);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    line-height: 1;
}
.score-label {
    color: #94a3b8;
    font-size: 1rem;
    margin-top: 0.4rem;
}
.progress-text {
    color: #94a3b8;
    font-size: 0.85rem;
    font-family: 'JetBrains Mono', monospace;
    margin-bottom: 0.5rem;
}
.title-main {
    color: white;
    font-size: 2rem;
    font-weight: 800;
    margin-bottom: 0.3rem;
}
.title-sub {
    color: #94a3b8;
    font-size: 1rem;
    margin-bottom: 2rem;
}
.stat-box {
    background: rgba(255,255,255,0.06);
    border-radius: 12px;
    padding: 1rem;
    margin: 0.4rem 0;
}
</style>
""", unsafe_allow_html=True)

# ─── QUIZ DATA ─────────────────────────────────────────────────────────────────
ALL_QUESTIONS = [
    # ── Kategori C: Pengelolaan Persediaan ──────────────────────────────────
    {
        "category": "C · Pengelolaan Persediaan",
        "question": "Kapan stock card di freezer/chiller wajib diperbarui setelah pengambilan WIP (Work In Progress)?",
        "options": [
            "A. Setelah proses thawing selesai",
            "B. Secara real-time, segera setelah pengambilan",
            "C. Setiap akhir shift",
            "D. Saat stock opname bulanan",
        ],
        "answer": "B. Secara real-time, segera setelah pengambilan",
        "explanation": "Temuan: Personel membiasakan update stock card SETELAH thawing, bukan saat pengambilan. Hal ini menyebabkan ketidakakuratan data stok (mis. Bumbu Hitam 4 pack tidak tercatat).",
    },
    {
        "category": "C · Pengelolaan Persediaan",
        "question": "Chest freezer yang terletak di LUAR area kitchen wajib dalam kondisi…",
        "options": [
            "A. Terkunci setiap saat, kecuali saat proses pengambilan bahan",
            "B. Terbuka agar sirkulasi udara lancar",
            "C. Dikunci hanya saat malam hari",
            "D. Tidak perlu dikunci karena ada CCTV",
        ],
        "answer": "A. Terkunci setiap saat, kecuali saat proses pengambilan bahan",
        "explanation": "Berdasarkan HNTK MKI-OPS-OK-3.2: tempat penyimpanan seperti dry storage, chiller, dan freezer yang tidak berada di dalam kitchen WAJIB dalam keadaan terkunci. Temuan: freezer dibiarkan tidak terkunci setelah proses thawing.",
    },
    {
        "category": "C · Pengelolaan Persediaan",
        "question": "Mengonsumsi produk (mis. prep kremes) di area produksi oleh personel outlet termasuk kategori…",
        "options": [
            "A. Pelanggaran ringan yang bisa ditoleransi",
            "B. Fraud (mengambil barang WIP) dan pelanggaran food safety",
            "C. Diperbolehkan selama jam istirahat",
            "D. Bukan pelanggaran karena produk belum dijual",
        ],
        "answer": "B. Fraud (mengambil barang WIP) dan pelanggaran food safety",
        "explanation": "Modul Fraud menyatakan salah satu contoh fraud adalah mengambil barang WIP. Selain itu, konsumsi di area produksi menimbulkan risiko kontaminasi silang pada produk.",
    },
    # ── Kategori G: Pengamanan Aset ─────────────────────────────────────────
    {
        "category": "G · Pengamanan Aset",
        "question": "Handphone outlet yang sudah ter-install portal Talenta saat closing disimpan di…",
        "options": [
            "A. Meja kasir agar mudah diakses keesokan harinya",
            "B. Lemari kasir yang terkunci",
            "C. Brankas",
            "D. Bisa di mana saja, yang penting aman",
        ],
        "answer": "B. Lemari kasir yang terkunci",
        "explanation": "Berdasarkan SOP Outlet Ver. 1.1: 1 HP yang sudah ter-install portal Talenta disimpan di lemari kasir yang terkunci (BUKAN di brankas). Temuan: personel tidak menyimpan di lemari terkunci karena terburu-buru pulang.",
    },
    {
        "category": "G · Pengamanan Aset",
        "question": "Siapa yang wajib memegang kunci box DVR CCTV di outlet?",
        "options": [
            "A. Security/satpam",
            "B. Area Manager (AM)",
            "C. Store Manager (SM)",
            "D. Siapa saja asal personel outlet",
        ],
        "answer": "C. Store Manager (SM)",
        "explanation": "HNTK MKI-OPS-OK-6.5: SM memastikan tempat penyimpanan DVR dalam keadaan terkunci dan kunci dipegang oleh SM. Temuan: DVR tidak terkunci karena kunci tidak ada sejak pergantian SM.",
    },
    {
        "category": "G · Pengamanan Aset",
        "question": "Pihak luar (non-Hangry) yang memasuki area outlet WAJIB…",
        "options": [
            "A. Menunjukkan KTP kepada kasir",
            "B. Mengisi Logbook Kunjungan Outlet yang tersedia di dalam bantex",
            "C. Ditemani personel outlet setiap saat",
            "D. Tidak perlu prosedur khusus",
        ],
        "answer": "B. Mengisi Logbook Kunjungan Outlet yang tersedia di dalam bantex",
        "explanation": "HNTK Outlet Restricted Area Procedure: seluruh pihak luar wajib mengisi daftar kunjungan melalui Logbook Kunjungan Outlet yang sudah dicetak dan disimpan dalam bantex. Temuan: outlet tidak menyediakan logbook sama sekali.",
    },
    # ── Kategori H: Pencegahan Hama ─────────────────────────────────────────
    {
        "category": "H · Pencegahan & Penanganan Hama",
        "question": "Gluepad fly catcher wajib dicek dan diganti setiap…",
        "options": [
            "A. Seminggu sekali (setiap Senin)",
            "B. Setiap tanggal 1 dan 15 setiap bulan",
            "C. Sebulan sekali di akhir bulan",
            "D. Hanya jika terlihat kotor",
        ],
        "answer": "B. Setiap tanggal 1 dan 15 setiap bulan",
        "explanation": "Dokumen Form Pergantian Gluepad: cek dan ganti gluepad setiap tanggal 1 & 15 setiap bulan, dan hasilnya wajib diisi pada form. Temuan: form pergantian gluepad area loker tidak tersedia.",
    },
    {
        "category": "H · Pencegahan & Penanganan Hama",
        "question": "Pintu area storage, kitchen, dan area air cooler harus dalam kondisi… setelah digunakan.",
        "options": [
            "A. Setengah terbuka untuk ventilasi",
            "B. Tertutup rapat",
            "C. Terbuka selama jam operasional",
            "D. Dikunci dari dalam",
        ],
        "answer": "B. Tertutup rapat",
        "explanation": "HNTK MKI-OPS-OK-6.6 Food Safety: seluruh pintu dan jendela dalam keadaan tertutup agar tidak terjadi cemaran (debu, asap, serangga, dan benda asing lainnya). Temuan: pintu storage terbuka hingga 15 jam, pintu kitchen 50 menit.",
    },
    # ── Kategori I: Kebersihan & Sanitasi ───────────────────────────────────
    {
        "category": "I · Kebersihan & Sanitasi",
        "question": "Bak kontrol di outlet wajib dibersihkan…",
        "options": [
            "A. Seminggu sekali sesuai jadwal cleaning",
            "B. Setiap hari saat proses closing",
            "C. Hanya jika tersumbat atau berbau",
            "D. Sebulan sekali",
        ],
        "answer": "B. Setiap hari saat proses closing",
        "explanation": "HNTK Kebersihan dan Sanitasi Hal 14: bak kontrol harus selalu dibersihkan saat melakukan proses closing. Temuan: SM/PIC hanya mengacu cleaning schedule dan tidak tahu bak kontrol harus dibersihkan harian.",
    },
    {
        "category": "I · Kebersihan & Sanitasi",
        "question": "Alat kebersihan (mis. floor wiper) dan chemical setelah digunakan harus disimpan di…",
        "options": [
            "A. Area front/kasir agar mudah dijangkau",
            "B. Area kitchen",
            "C. Area janitor, terpisah dari area kitchen/bar/storage",
            "D. Di mana saja asalkan tidak di lantai",
        ],
        "answer": "C. Area janitor, terpisah dari area kitchen/bar/storage",
        "explanation": "HNTK Kebersihan dan Sanitasi Hal 32: chemical dan peralatan kebersihan harus disimpan pada area Janitor. Temuan: floor wiper ditemukan di area front. Ini juga menjadi temuan BERULANG dari audit sebelumnya (Kategori P).",
    },
    {
        "category": "I · Kebersihan & Sanitasi",
        "question": "Bottle spray chemical (mis. Nuvet) WAJIB…",
        "options": [
            "A. Diberi label sesuai identitas chemical dengan jelas",
            "B. Tidak perlu label karena semua staf sudah tahu isinya",
            "C. Diberi label hanya jika chemical baru",
            "D. Cukup dibedakan berdasarkan warna botol",
        ],
        "answer": "A. Diberi label sesuai identitas chemical dengan jelas",
        "explanation": "HNTK Kebersihan dan Sanitasi Hal 32: lakukan penamaan pada wadah berisi chemical sesuai identitasnya menggunakan label yang terbaca jelas. Tanpa label, chemical bisa tertukar dan proses cleaning tidak optimal.",
    },
    # ── Kategori J: Equipment ───────────────────────────────────────────────
    {
        "category": "J · Kondisi & Kelayakan Equipment",
        "question": "Standar suhu display chest freezer/upright freezer yang berlaku adalah…",
        "options": [
            "A. 0°C s.d. 5°C",
            "B. -5°C s.d. -10°C",
            "C. -18°C s.d. -12°C",
            "D. -25°C s.d. -20°C",
        ],
        "answer": "C. -18°C s.d. -12°C",
        "explanation": "HNTK MKI-OPS-OK-4.2: standar suhu freezer adalah -18°C s.d. -12°C. Temuan: chest freezer menunjukkan -0.9°C (jauh dari standar) dan tidak ditindaklanjuti oleh SM.",
    },
    {
        "category": "J · Kondisi & Kelayakan Equipment",
        "question": "Jika selisih suhu display dan suhu aktual chiller/freezer MELEBIHI +5°C lebih dari 1 jam, tindakan yang harus dilakukan adalah…",
        "options": [
            "A. Tunggu sampai suhu normal sendiri",
            "B. Pindahkan semua produk ke freezer lain tanpa laporan",
            "C. Laporkan ke Troubleshoot sesuai prosedur",
            "D. Matikan freezer dan nyalakan kembali",
        ],
        "answer": "C. Laporkan ke Troubleshoot sesuai prosedur",
        "explanation": "HNTK MKI-OPS-OK-4.2: apabila perbedaan suhu display vs aktual melebihi +5°C lebih dari 1 jam, lakukan proses report ke Troubleshoot. Temuan: undercounter chiller suhu display 7.8°C dan aktual 11.2°C tidak ditindaklanjuti.",
    },
    # ── Kategori M: Food Safety ─────────────────────────────────────────────
    {
        "category": "M · Keamanan Pangan (Food Safety)",
        "question": "Berapa lama standar waktu resting Simple Syrup?",
        "options": [
            "A. 5 menit",
            "B. 10 menit",
            "C. 20 menit",
            "D. 1 jam",
        ],
        "answer": "C. 20 menit",
        "explanation": "SPM Simple Syrup (PREP) Rev 02: waktu resting adalah 20 menit. Temuan: resting dilakukan selama 1 jam 5 menit karena personel terdistraksi oleh aktivitas operasional.",
    },
    {
        "category": "M · Keamanan Pangan (Food Safety)",
        "question": "Setelah proses resting, Marinated Whole Chicken (UB) harus disimpan di…",
        "options": [
            "A. Suhu ruang hingga siap digunakan",
            "B. Di dalam chiller",
            "C. Freezer",
            "D. Bisa di suhu ruang maksimal 2 jam",
        ],
        "answer": "B. Di dalam chiller",
        "explanation": "SPM Marinated Whole Chicken (PREP): waktu thawing 36 jam di chiller. Temuan: ayam disimpan di suhu ruang selama 1 jam 16 menit setelah resting, berisiko menurunkan kualitas hingga keracunan makanan.",
    },
    {
        "category": "M · Keamanan Pangan (Food Safety)",
        "question": "GN Pan berisi Prep Kremes, Beras Ketan, dan Prep Iced Tea yang tidak sedang digunakan harus…",
        "options": [
            "A. Dibiarkan terbuka agar mudah diakses dan mempercepat service",
            "B. Ditutup dengan tutup wadah atau plastic wrap",
            "C. Dipindahkan ke dalam chiller",
            "D. Ditutup hanya jika lebih dari 30 menit tidak digunakan",
        ],
        "answer": "B. Ditutup dengan tutup wadah atau plastic wrap",
        "explanation": "HNTK Food Safety Hal 4: seluruh bahan pangan disimpan dalam keadaan tertutup. SPM Black Tea Extract: tutup wadah resting dengan plastic wrap. Temuan: GN Pan terbuka 29 menit, Beras Ketan terbuka tanpa wrap, Iced Tea terbuka.",
    },
    # ── Kategori N: Grooming ────────────────────────────────────────────────
    {
        "category": "N · Grooming Sesuai Standar",
        "question": "Apron wajib DILEPAS saat personel berada di…",
        "options": [
            "A. Area produksi kitchen",
            "B. Bar/serving area",
            "C. Toilet, area istirahat, dan keluar outlet",
            "D. Hanya saat keluar gedung",
        ],
        "answer": "C. Toilet, area istirahat, dan keluar outlet",
        "explanation": "SOP Outlet Ver. 1.10 Hal 3: Apron, Hairnet, dan Plastic Mask wajib dilepas saat ke toilet, saat break, dan keluar dari outlet. Temuan: personel masih menggunakan apron saat menyapu di area depan outlet.",
    },
    {
        "category": "N · Grooming Sesuai Standar",
        "question": "Hand gloves wajib digunakan oleh penjamah makanan saat…",
        "options": [
            "A. Hanya saat proses thawing",
            "B. Hanya saat memasak",
            "C. Setiap menangani/menyajikan makanan",
            "D. Tidak wajib jika tangan sudah dicuci",
        ],
        "answer": "C. Setiap menangani/menyajikan makanan",
        "explanation": "HNTK Food Safety Hal 5: penjamah makanan setiap menangani makanan WAJIB menggunakan hand glove (sarung tangan plastik sekali pakai) untuk menghindari kontak langsung. Temuan: hand gloves tidak konsisten digunakan saat penyajian.",
    },
    {
        "category": "N · Grooming Sesuai Standar",
        "question": "Standar seragam staff Front/Kitchen mencakup penggunaan…",
        "options": [
            "A. Masker kain dan celemek pribadi",
            "B. Masker plastik dan Celemek Hangry",
            "C. Masker medis dan sarung tangan",
            "D. Hairnet dan masker kain",
        ],
        "answer": "B. Masker plastik dan Celemek Hangry",
        "explanation": "HNTK Kebersihan dan Penampilan Pribadi Hal 8: standar seragam staff Front/Kitchen adalah masker plastik dan Celemek Hangry. Temuan: personel tidak konsisten menggunakan masker karena merasa tidak nyaman.",
    },
    # ── Kategori P: Tindak Lanjut Temuan ───────────────────────────────────
    {
        "category": "P · Tindak Lanjut Temuan Audit",
        "question": "Jika suatu temuan sudah muncul di audit sebelumnya namun terulang kembali, hal itu dikategorikan sebagai…",
        "options": [
            "A. Temuan baru yang independen",
            "B. Pengulangan temuan (Kategori P) — kelemahan monitoring aktivitas",
            "C. Hal yang wajar dan tidak perlu dicatat ulang",
            "D. Temuan minor yang tidak berpengaruh pada skor",
        ],
        "answer": "B. Pengulangan temuan (Kategori P) — kelemahan monitoring aktivitas",
        "explanation": "SOP MKI-HO-IA-1.0 mengacu pada COSO Internal Control - Integrated Framework (Monitoring Activity). Pengulangan temuan menunjukkan SM belum memastikan semua temuan audit ditindaklanjuti secara tuntas. Contoh temuan berulang: alat kebersihan tidak disimpan di janitor.",
    },
]

# ─── SESSION STATE ────────────────────────────────────────────────────────────
def init_state():
    if "quiz_started" not in st.session_state:
        st.session_state.quiz_started = False
    if "questions" not in st.session_state:
        st.session_state.questions = []
    if "q_index" not in st.session_state:
        st.session_state.q_index = 0
    if "score" not in st.session_state:
        st.session_state.score = 0
    if "answered" not in st.session_state:
        st.session_state.answered = False
    if "selected" not in st.session_state:
        st.session_state.selected = None
    if "quiz_done" not in st.session_state:
        st.session_state.quiz_done = False
    if "wrong_list" not in st.session_state:
        st.session_state.wrong_list = []
    if "num_questions" not in st.session_state:
        st.session_state.num_questions = 10

init_state()

# ─── HELPERS ──────────────────────────────────────────────────────────────────
def start_quiz(n):
    st.session_state.questions = random.sample(ALL_QUESTIONS, min(n, len(ALL_QUESTIONS)))
    st.session_state.q_index = 0
    st.session_state.score = 0
    st.session_state.answered = False
    st.session_state.selected = None
    st.session_state.quiz_done = False
    st.session_state.wrong_list = []
    st.session_state.quiz_started = True

def answer_question(option):
    if st.session_state.answered:
        return
    st.session_state.selected = option
    st.session_state.answered = True
    q = st.session_state.questions[st.session_state.q_index]
    if option == q["answer"]:
        st.session_state.score += 1
    else:
        st.session_state.wrong_list.append({
            "question": q["question"],
            "your_answer": option,
            "correct": q["answer"],
            "explanation": q["explanation"],
        })

def next_question():
    if st.session_state.q_index + 1 >= len(st.session_state.questions):
        st.session_state.quiz_done = True
    else:
        st.session_state.q_index += 1
        st.session_state.answered = False
        st.session_state.selected = None

def restart():
    st.session_state.quiz_started = False
    st.session_state.quiz_done = False

# ─── RENDER: HOME ─────────────────────────────────────────────────────────────
if not st.session_state.quiz_started:
    st.markdown('<div class="title-main">📋 Quiz Audit Outlet</div>', unsafe_allow_html=True)
    st.markdown('<div class="title-sub">Uji pemahaman SOP agar temuan audit tidak terulang kembali</div>', unsafe_allow_html=True)

    st.markdown('<div class="quiz-card">', unsafe_allow_html=True)
    st.markdown("**Topik yang diujikan:**")
    topics = [
        ("C", "Pengelolaan Persediaan (Stock Card, Freezer, Fraud)"),
        ("G", "Pengamanan Aset (HP, DVR, Logbook Tamu)"),
        ("H", "Pencegahan & Penanganan Hama (Gluepad, Pintu)"),
        ("I", "Kebersihan & Sanitasi (Bak Kontrol, Chemical)"),
        ("J", "Kondisi & Kelayakan Equipment (Suhu Freezer/Chiller)"),
        ("M", "Keamanan Pangan / Food Safety (Resting, Penutupan Wadah)"),
        ("N", "Grooming (Apron, Hand Gloves, Masker)"),
        ("P", "Tindak Lanjut Temuan Audit"),
    ]
    for code, desc in topics:
        st.markdown(f"<span class='category-badge'>{code}</span> &nbsp;{desc}", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    n = st.slider("Jumlah soal", min_value=5, max_value=len(ALL_QUESTIONS), value=10, step=1)
    st.session_state.num_questions = n

    if st.button("🚀 Mulai Quiz", use_container_width=True):
        start_quiz(n)
        st.rerun()

# ─── RENDER: QUIZ DONE ────────────────────────────────────────────────────────
elif st.session_state.quiz_done:
    total = len(st.session_state.questions)
    score = st.session_state.score
    pct = int(score / total * 100)

    st.markdown(f"""
    <div class="score-card">
        <div style="font-size:1rem;color:#94a3b8;margin-bottom:0.5rem;">HASIL QUIZ</div>
        <div class="score-big">{pct}%</div>
        <div class="score-label">{score} dari {total} soal benar</div>
    </div>
    """, unsafe_allow_html=True)

    # Grade
    if pct == 100:
        msg = "🏆 Sempurna! Kamu sudah paham SOP dengan sangat baik."
        color = "#86efac"
    elif pct >= 80:
        msg = "✅ Bagus! Tingkatkan konsistensi dalam operasional harian."
        color = "#93c5fd"
    elif pct >= 60:
        msg = "⚠️ Cukup. Masih ada area yang perlu diperdalam."
        color = "#fcd34d"
    else:
        msg = "❌ Perlu belajar lebih lanjut. Review SOP dan temuan audit!"
        color = "#fca5a5"

    st.markdown(f"<div style='text-align:center;color:{color};font-weight:700;font-size:1.1rem;margin:1rem 0'>{msg}</div>", unsafe_allow_html=True)

    # Wrong answers review
    if st.session_state.wrong_list:
        st.markdown("---")
        st.markdown("<div style='color:#f1f5f9;font-weight:700;font-size:1rem;margin-bottom:0.8rem'>📌 Soal yang perlu diperhatikan:</div>", unsafe_allow_html=True)
        for i, w in enumerate(st.session_state.wrong_list, 1):
            with st.expander(f"Soal {i}: {w['question'][:70]}..."):
                st.markdown(f"<div class='feedback-wrong'>❌ Jawaban kamu: {w['your_answer']}</div>", unsafe_allow_html=True)
                st.markdown(f"<div class='feedback-correct'>✅ Jawaban benar: {w['correct']}</div>", unsafe_allow_html=True)
                st.markdown(f"<div class='explanation-box'>💡 {w['explanation']}</div>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔄 Ulangi Quiz", use_container_width=True):
            start_quiz(st.session_state.num_questions)
            st.rerun()
    with col2:
        if st.button("🏠 Kembali ke Menu", use_container_width=True):
            restart()
            st.rerun()

# ─── RENDER: QUIZ IN PROGRESS ────────────────────────────────────────────────
else:
    questions = st.session_state.questions
    idx = st.session_state.q_index
    q = questions[idx]
    total = len(questions)

    # Progress
    progress = (idx + 1) / total
    st.markdown(f'<div class="progress-text">Soal {idx+1} dari {total} &nbsp;|&nbsp; Skor: {st.session_state.score}</div>', unsafe_allow_html=True)
    st.progress(progress)

    # Question card
    st.markdown(f"""
    <div class="quiz-card">
        <div class="category-badge">{q["category"]}</div>
        <div class="question-text">{q["question"]}</div>
    </div>
    """, unsafe_allow_html=True)

    # Options
    if not st.session_state.answered:
        for opt in q["options"]:
            if st.button(opt, key=f"opt_{idx}_{opt}", use_container_width=True):
                answer_question(opt)
                st.rerun()
    else:
        correct = q["answer"]
        selected = st.session_state.selected
        for opt in q["options"]:
            if opt == correct:
                st.markdown(f"<div class='feedback-correct'>✅ {opt}</div>", unsafe_allow_html=True)
            elif opt == selected and opt != correct:
                st.markdown(f"<div class='feedback-wrong'>❌ {opt}</div>", unsafe_allow_html=True)
            else:
                st.markdown(f"<div style='background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.07);border-radius:12px;padding:0.75rem 1rem;color:#64748b;margin-bottom:0.5rem'>{opt}</div>", unsafe_allow_html=True)

        # Explanation
        st.markdown(f"<div class='explanation-box'>💡 <b>Penjelasan:</b> {q['explanation']}</div>", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        label = "Selesai →" if idx + 1 >= total else "Soal Berikutnya →"
        if st.button(label, use_container_width=True):
            next_question()
            st.rerun()
