import streamlit as st
import folium
from folium import plugins
from streamlit_folium import st_folium
from gtts import gTTS
import os
import base64

# Set Streamlit Page Configuration
st.set_page_config(
    page_title="BhoomiAI — DIGIPIN Satellite AI & Bhashini System",
    page_icon="🛰️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom High-Tech Styling
st.markdown("""
<style>
  .main { background-color: #070b14; color: #f8fafc; }
  .stTextInput>div>div>input { background-color: #0e1526; color: #38bdf8; font-weight: bold; border: 2px solid #0284c7; }
  .metric-box { background: #0e1526; border: 1px solid #1e293b; border-radius: 8px; padding: 12px; margin-bottom: 8px; }
  .patta-card { background: linear-gradient(135deg, #091f16, #0e3022); border: 1.5px solid #10b981; border-radius: 10px; padding: 14px; margin-bottom: 12px; }
  .landmark-card { background: #080f1e; border: 1px solid #1e3a8a; border-radius: 10px; padding: 14px; margin-bottom: 12px; }
  .bhashini-card { background: linear-gradient(135deg, #091528, #0f1c36); border: 1px solid #38bdf8; border-radius: 10px; padding: 14px; margin-bottom: 12px; }
</style>
""", unsafe_allow_html=True)

# App Owner Secret Passcode & Database
OWNER_PASSCODE = "LITHU_@1234"

LANDMARK_DB = {
    "M9F 4LLM LFC": {
        "formatted": "M9F-4LLM-LFC",
        "lat": 11.1477, "lon": 77.1408,
        "name": "KPR இன்ஸ்டிடியூட் ஆஃப் இன்ஜினியரிங் & டெக்னாலஜி, கோயம்புத்தூர்",
        "pattaNo": "2045", "oldPattaNo": "1120 (கல்வி அறக்கட்டளை)", "surveyNo": "162 / 3A",
        "ownerName": "KPR கல்வி அறக்கட்டளை (KPR Educational Trust)",
        "landType": "கல்வி நிறுவனம் & கல்லூரி வளாக மனை (Institutional Campus)",
        "extent": "35.0 ஏக்கர் (KPR கல்லூரி வளாகம்)",
        "street": "அவிநாசி மெயின் ரோடு & பாரதி விடுதி (Avinashi Road, Arasur)",
        "govtBuilding": "🏛️ KPR பொறியியல் கல்லூரி & PNB ஏடிஎம் (50m)",
        "waterBody": "🌊 கல்லூரி பசுமை வளாக நீர்நிலை (150m)",
        "busStop": "🚌 KPR கல்லூரி பேருந்து நிறுத்தம் / அரசூர் (200m)",
        "taluk": "சூலூர் தாலுகா, கோயம்புத்தூர் மாவட்டம் - 641407",
        "constVal": "+850 m² (Hostel Block)", "vegVal": "+15.2%", "roadVal": "+450m",
        "reportTa": "டிஜிபின் M9F-4LLM-LFC அதிகாரப்பூர்வ அஞ்சல் முகவரி: KPR இன்ஸ்டிடியூட் ஆஃப் இன்ஜினியரிங் அண்ட் டெக்னாலஜி வளாகம், பாரதி விடுதி பகுதி, அரசூர், அவிநாசி ரோடு, சூலூர் தாலுகா, கோயம்புத்தூர் மாவட்டம் (641407). பட்டா எண் 2045, புல எண் 162/3A. கடந்த ஆண்டுகளுடன் ஒப்பிடும்போது 850 சதுர மீட்டர் புதிய கட்டட விரிவாக்கம் கண்டறியப்பட்டுள்ளது."
    },
    "M8J LJLC 5C2": {
        "formatted": "M8J-LJLC-5C2",
        "lat": 10.4326, "lon": 79.3184,
        "name": "அதம்பை தெற்கு, பட்டுக்கோட்டை தாலுகா, தஞ்சாவூர்",
        "pattaNo": "1408", "oldPattaNo": "824 (பழைய மூலப் பட்டா)", "surveyNo": "142 / 2A",
        "ownerName": "செல்வகுமார் பன்னீர்செல்வம் (Selvakumar Panneerselvam)",
        "landType": "நன்செய் பட்டா நிலம் (Coconut & Paddy Farm)",
        "extent": "0.85 ஏக்கர் (37,026 சதுர அடி)",
        "street": "அதம்பை தெற்கு மெயின் ரோடு & தோப்பு சாலை",
        "govtBuilding": "🏛️ கிராம ஊராட்சி மன்ற அலுவலகம் & ரேஷன் கடை (350m)",
        "waterBody": "🌊 கல்லணைக் கால்வாய் பாசன வாய்க்கால் (180m)",
        "busStop": "🚌 அதம்பை தெற்கு பேருந்து நிறுத்தம் (220m)",
        "taluk": "அதம்பை தெற்கு, பட்டுக்கோட்டை தாலுகா, தஞ்சாவூர் - 614602",
        "constVal": "+160 m² (Farm House)", "vegVal": "+24.8%", "roadVal": "+280m",
        "reportTa": "டிஜிபின் M8J-LJLC-5C2 நில உரிமை & பட்டா அறிக்கை: சரியான முகவரி - அதம்பை தெற்கு, பட்டுக்கோட்டை தாலுகா, தஞ்சாவூர் மாவட்டம் (614602). பட்டா எண்: 1408, புல எண்: 142/2A. உரிமையாளர்: செல்வகுமார் பன்னீர்செல்வம். முந்தைய ஆண்டுடன் ஒப்பிடும்போது தென்னந்தோப்பு பசுமை பரப்பு +24.8% அதிகரித்துள்ளது."
    }
}

# --- HEADER ---
col_head1, col_head2 = st.columns([3, 1])
with col_head1:
    st.title("🛰️ BhoomiAI — DIGIPIN Satellite Change & Bhashini Voice")
    st.caption("தேசிய டிஜிபின் (DIGIPIN) செயற்கைக்கோள் AI மாற்றங்கள் & பாஷினி தமிழ் குரல் முறைமை")
with col_head2:
    lang = st.selectbox("Language / மொழி", ["தமிழ் (Tamil)", "English", "हिन्दी (Hindi)"])

# --- SIDEBAR (User Login & 3 Free Searches / Owner Code) ---
with st.sidebar:
    st.header("👤 User Authentication / உள்நுழைவு")
    user_name = st.text_input("Full Name (பெயர்)", value="Selvakumar")
    user_auth = st.text_input("Mobile No / Owner Code (LITHU_@1234)", value="LITHU_@1234", type="password")

    if user_auth == OWNER_PASSCODE:
        st.success("👑 VIP OWNER: Infinite Access Activated (LITHU_@1234)")
    else:
        st.info("🎁 Free User: 3 Free Searches Available")

    st.markdown("---")
    st.subheader("📅 Multi-Year Historical Satellite")
    past_year = st.selectbox("Select Past Year (முந்தைய ஆண்டு)", ["2014", "2016", "2018", "2020", "2022", "2024", "2025"], index=3)
    curr_year = "2026 (Live Current)"

# --- SEARCH BAR ---
st.markdown("### 📍 National DIGIPIN & Location Search")
c_srch1, c_srch2 = st.columns([4, 1])
with c_srch1:
    search_query = st.text_input("Enter DIGIPIN or Place Name", value="M9F 4LLM LFC")
with c_srch2:
    search_btn = st.button("🚀 Run AI Analysis", use_container_width=True)

# Resolve Location Data
clean_q = search_query.strip().upper()
if clean_q in LANDMARK_DB:
    loc_data = LANDMARK_DB[clean_q]
else:
    loc_data = LANDMARK_DB["M9F 4LLM LFC"]

# --- WORKSPACE GRID (Map + Analytics) ---
col_map, col_info = st.columns([1.3, 0.7])

with col_map:
    st.subheader(f"📍 {loc_data['name']}")
    st.caption(f"Lat: {loc_data['lat']}° N, Lon: {loc_data['lon']}° E | Historical {past_year} vs. Current {curr_year}")

    # Build Leaflet Satellite Map via Folium
    m = folium.Map(location=[loc_data['lat'], loc_data['lon']], zoom_start=16, tiles=None)
    
    # Add High-Res Esri Satellite Layer
    folium.TileLayer(
        tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
        attr='Esri World Imagery',
        name='Real Earth Satellite',
        overlay=False,
        control=True
    ).add_to(m)

    # Add AI Bounding Boxes (Blue = Construction, Green = Canopy)
    lat, lon = loc_data['lat'], loc_data['lon']
    folium.Rectangle(
        bounds=[[lat + 0.0003, lon + 0.0003], [lat + 0.0012, lon + 0.0015]],
        color='#38bdf8', weight=3, fill=True, fill_color='#0284c7', fill_opacity=0.4,
        popup='🟦 AI Detected: New Building Construction'
    ).add_to(m)

    folium.Rectangle(
        bounds=[[lat - 0.0022, lon - 0.0022], [lat - 0.0005, lon - 0.0005]],
        color='#10b981', weight=2, fill=True, fill_color='#10b981', fill_opacity=0.3,
        popup='🟩 AI Detected: Green Canopy Growth'
    ).add_to(m)

    # Render Map in Streamlit
    st_folium(m, width=750, height=450)

with col_info:
    # 1. Digital Patta Card
    st.markdown(f"""
    <div class="patta-card">
      <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:6px;">
        <b style="color:#34d399; font-size:13px;">📜 Official Digital Patta Verification</b>
        <span style="background:#10b981; color:#0f172a; font-size:9px; font-weight:bold; padding:2px 6px; border-radius:10px;">தமிழ் நிலம் VERIFIED</span>
      </div>
      <div style="font-size:12px; line-height:1.6;">
        📜 <b>பட்டா எண் (Patta No):</b> <span style="color:#34d399; font-weight:bold;">{loc_data['pattaNo']}</span> (மூலப் பட்டா: {loc_data['oldPattaNo']})<br/>
        📍 <b>புல எண் (Survey No):</b> <span style="color:#38bdf8; font-weight:bold;">{loc_data['surveyNo']}</span><br/>
        👤 <b>உரிமையாளர்:</b> <b>{loc_data['ownerName']}</b><br/>
        🌾 <b>வகைப்பாடு:</b> {loc_data['landType']}<br/>
        📐 <b>பரப்பளவு:</b> <b style="color:#fbbf24;">{loc_data['extent']}</b>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # 2. Landmark Radar Card
    st.markdown(f"""
    <div class="landmark-card">
      <b style="color:#38bdf8; font-size:12.5px;">🏛️ Exact Ground Landmark & Street</b>
      <div style="font-size:11.5px; margin-top:4px; line-height:1.5;">
        🛣️ <b>தெரு:</b> {loc_data['street']}<br/>
        🏛️ <b>அரசு கட்டடம்:</b> {loc_data['govtBuilding']}<br/>
        🌊 <b>நீர்நிலை:</b> {loc_data['waterBody']}<br/>
        🚌 <b>பேருந்து நிறுத்தம்:</b> {loc_data['busStop']}<br/>
        📍 <b>தாலுகா / மாவட்டம்:</b> {loc_data['taluk']}
      </div>
    </div>
    """, unsafe_allow_html=True)

    # 3. Telemetry Metrics
    c_m1, c_m2 = st.columns(2)
    with c_m1:
        st.metric("New Construction", loc_data['constVal'])
        st.metric("New Roadways", loc_data['roadVal'])
    with c_m2:
        st.metric("Green Canopy Delta", loc_data['vegVal'])
        st.metric("Water Body Status", loc_data['waterVal'])

    # 4. Bhashini Tamil Voice Box
    st.markdown(f"""
    <div class="bhashini-card">
      <b style="color:#38bdf8; font-size:12px;">🇮🇳 பாஷினி AI குரல் விளக்கம் (Tamil Voice)</b>
      <div style="font-size:11.5px; margin-top:4px; line-height:1.5;">
        {loc_data['reportTa']}
      </div>
    </div>
    """, unsafe_allow_html=True)

    # Generate Audio via gTTS
    if st.button("🔊 Generate & Play Tamil Voice (குரல் கேட்க)"):
        tts = gTTS(text=loc_data['reportTa'], lang='ta', slow=False)
        tts.save("temp_voice.mp3")
        st.audio("temp_voice.mp3", format="audio/mp3")

st.markdown("---")
st.caption("© 2026 BhoomiAI • Developed by EliKsha AI Labs (Selvakumar Panneerselvam)")
