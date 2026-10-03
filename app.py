import streamlit as st
import streamlit.components.v1 as components
import os
import time
import subprocess
from PIL import Image
from google import genai
from google.genai import types
from google.genai.errors import APIError

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="ARIS // JARVIS Matrix",
    page_icon="💠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CUSTOM HUD STYLING ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@500;700;900&family=Rajdhani:wght@500;600;700&display=swap');

    .stApp {
        background: radial-gradient(circle at 50% 20%, #03121e 0%, #010408 100%);
        color: #d1ecf1;
        font-family: 'Rajdhani', sans-serif;
    }
    [data-testid="stSidebar"] {
        background: rgba(2, 8, 16, 0.95);
        border-right: 1px solid rgba(0, 243, 255, 0.2);
    }
    .jarvis-header {
        background: linear-gradient(135deg, rgba(4, 30, 48, 0.9) 0%, rgba(2, 12, 24, 0.95) 100%);
        border: 1px solid #00f3ff;
        border-radius: 12px;
        padding: 18px 20px;
        text-align: center;
        box-shadow: 0 0 25px rgba(0, 243, 255, 0.2);
        margin-bottom: 15px;
    }
    .jarvis-title {
        font-family: 'Orbitron', sans-serif;
        color: #00f3ff;
        font-size: 24px;
        font-weight: 900;
        letter-spacing: 2px;
        margin: 0;
    }
    .hud-card {
        background: rgba(4, 18, 30, 0.85);
        border: 1px solid rgba(0, 243, 255, 0.3);
        border-radius: 8px;
        padding: 8px;
        text-align: center;
        font-family: 'Orbitron', sans-serif;
        font-size: 11px;
        color: #38bdf8;
    }
    .hud-val {
        color: #ffffff;
        font-size: 13px;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# --- GEMINI CLIENT SETUP ---
@st.cache_resource
def get_gemini_client():
    api_key = st.secrets.get("GEMINI_API_KEY") or os.environ.get("GEMINI_API_KEY")
    if not api_key:
        return None
    return genai.Client(api_key=api_key)

# --- SESSION STATE ---
if "threads" not in st.session_state:
    st.session_state.threads = {"Master Terminal": []}
if "current_thread" not in st.session_state:
    st.session_state.current_thread = "Master Terminal"
if "memory_vault" not in st.session_state:
    st.session_state.memory_vault = []

# --- VOICE FEEDBACK ---
def mj_voice_agent(text):
    try:
        clean_text = str(text).replace('"', '').replace("'", "").replace("\n", " ")[:200]
        js = f"""
        <script>
            if ('speechSynthesis' in window) {{
                window.speechSynthesis.cancel();
                var msg = new SpeechSynthesisUtterance('{clean_text}');
                msg.rate = 1.05;
                window.speechSynthesis.speak(msg);
            }}
        </script>
        """
        components.html(js, height=0, width=0)
    except Exception:
        pass

# --- HEADER HUD ---
st.markdown("""
<div class="jarvis-header">
    <h1 class="jarvis-title">ARIS // JARVIS CORE</h1>
    <div style="color: #38bdf8; font-size: 12px; letter-spacing: 2px;">TACTICAL AI MATRIX | GEMINI 2.5 FLASH</div>
</div>
""", unsafe_allow_html=True)

# --- 3D ARC REACTOR (MOUSE REACTIVE) ---
arc_reactor_html = """
<!DOCTYPE html>
<html>
<head>
<style>
  body { margin: 0; overflow: hidden; background: transparent; }
  #canvas3d { width: 100%; height: 230px; display: block; cursor: crosshair; }
</style>
<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
</head>
<body>
<div id="canvas3d"></div>
<script>
  const container = document.getElementById('canvas3d');
  const scene = new THREE.Scene();
  const camera = new THREE.PerspectiveCamera(50, container.clientWidth / container.clientHeight, 0.1, 1000);
  const renderer = new THREE.WebGLRenderer({ alpha: true, antialias: true });
  renderer.setSize(container.clientWidth, container.clientHeight);
  container.appendChild(renderer.domElement);

  const group = new THREE.Group();
  scene.add(group);

  const ring1 = new THREE.Mesh(
    new THREE.TorusGeometry(2.3, 0.04, 16, 90),
    new THREE.MeshBasicMaterial({ color: 0x00f3ff, wireframe: true })
  );
  group.add(ring1);

  const ring2 = new THREE.Mesh(
    new THREE.TorusGeometry(1.7, 0.06, 16, 70),
    new THREE.MeshBasicMaterial({ color: 0x0284c7, wireframe: true })
  );
  group.add(ring2);

  const core = new THREE.Mesh(
    new THREE.IcosahedronGeometry(0.85, 1),
    new THREE.MeshBasicMaterial({ color: 0x38bdf8, wireframe: true })
  );
  group.add(core);

  camera.position.z = 6;

  let mouseX = 0, mouseY = 0;
  window.addEventListener('mousemove', (e) => {
    const rect = container.getBoundingClientRect();
    mouseX = ((e.clientX - rect.left) / container.clientWidth) * 2 - 1;
    mouseY = -(((e.clientY - rect.top) / container.clientHeight) * 2 - 1);
  });

  function animate() {
    requestAnimationFrame(animate);
    ring1.rotation.z += 0.01;
    ring2.rotation.z -= 0.012;
    core.rotation.y += 0.018;

    group.rotation.y += (mouseX * 0.7 - group.rotation.y) * 0.06;
    group.rotation.x += (-mouseY * 0.7 - group.rotation.x) * 0.06;

    renderer.render(scene, camera);
  }
  animate();
</script>
</body>
</html>
"""
components.html(arc_reactor_html, height=240)

# --- TELEMETRY CARDS ---
c1, c2, c3, c4 = st.columns(4)
with c1:
    st.markdown('<div class="hud-card">STATUS<div class="hud-val">ONLINE 100%</div></div>', unsafe_allow_html=True)
with c2:
    st.markdown('<div class="hud-card">NEURAL CORE<div class="hud-val">GEMINI 2.5</div></div>', unsafe_allow_html=True)
with c3:
    st.markdown(f'<div class="hud-card">MEMORY VAULT<div class="hud-val">{len(st.session_state.memory_vault)} ENTRIES</div></div>', unsafe_allow_html=True)
with c4:
    st.markdown('<div class="hud-card">STREAM<div class="hud-val">ACTIVE</div></div>', unsafe_allow_html=True)

st.write("")

# --- STREAMING EXECUTION CORE ---
def run_aris_core(query, uploaded_file=None):
    client = get_gemini_client()
    if not client:
        yield "SYSTEM ERROR: GEMINI_API_KEY missing from Streamlit Secrets."
        return

    q_lower = query.lower() if query else ""

    if q_lower.startswith("remember "):
        fact = query[9:].strip()
        if fact and fact not in st.session_state.memory_vault:
            st.session_state.memory_vault.append(fact)
        yield f"ARIS: Data segment logged to persistent memory vault: '{fact}'."
        return

    memories = "\n".join([f"- {m}" for m in st.session_state.memory_vault]) or "No records."
    system_prompt = f"""
You are ARIS // JARVIS-Supreme, an elite AI assistant engineered by Mayank.
Tone: Confident, fast, razor-sharp, loyal, addressing user as Boss or Sir.
If Hindi/Hinglish is used, respond in witty Hinglish. If English, British Jarvis tone.
[MEMORY VAULT]:
{memories}
"""

    parts = []
    if uploaded_file is not None:
        parts.append(types.Part.from_bytes(data=uploaded_file.getvalue(), mime_type=uploaded_file.type or "image/jpeg"))
    parts.append(query)

    config = types.GenerateContentConfig(
        system_instruction=system_prompt,
        temperature=0.4,
        max_output_tokens=2500
    )

    try:
        response = client.models.generate_content_stream(
            model="gemini-2.5-flash",
            contents=parts,
            config=config
        )
        for chunk in response:
            if chunk.text:
                yield chunk.text
    except Exception as e:
        yield f"[CORE FAULT]: {str(e)}"

# --- SIDEBAR CONTROLS ---
with st.sidebar:
    st.markdown("### 💠 ARIS COMMAND DECK")
    if st.button("🗑️ Clear Screen Memory", use_container_width=True):
        st.session_state.threads[st.session_state.current_thread] = []
        st.rerun()

    st.markdown("---")
    st.markdown("🧠 **Memory Vault**")
    if not st.session_state.memory_vault:
        st.caption("Empty. Use: `remember <fact>`")
    else:
        for idx, m in enumerate(st.session_state.memory_vault):
            st.info(f"• {m}")

# --- FILE UPLOADER & CHAT ---
uploaded_file = st.file_uploader("📤 Multimodal Optical Feed", type=["jpg", "jpeg", "png", "webp"])

current_messages = st.session_state.threads[st.session_state.current_thread]
for msg in current_messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

user_input = st.chat_input("Command Jarvis Core...")
if user_input:
    current_messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        stream_box = st.empty()
        full_text = ""
        for chunk in run_aris_core(user_input, uploaded_file):
            full_text += chunk
            stream_box.markdown(full_text + " ▌")
        stream_box.markdown(full_text)
        current_messages.append({"role": "assistant", "content": full_text})
        mj_voice_agent(full_text)
