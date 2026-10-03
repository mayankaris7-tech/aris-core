# --- HOLOGRAPHIC COMM-LINK (VOICE INPUT COMPONENT) ---
voice_input_html = """
<div style="display: flex; justify-content: center; margin-bottom: 15px;">
    <button id="micBtn" onclick="toggleSpeech()" style="
        background: rgba(3, 22, 33, 0.9);
        border: 2px solid #00f3ff;
        border-radius: 30px;
        color: #00f3ff;
        padding: 10px 24px;
        font-family: 'Orbitron', sans-serif;
        font-size: 13px;
        font-weight: 700;
        letter-spacing: 2px;
        cursor: pointer;
        box-shadow: 0 0 15px rgba(0, 243, 255, 0.4);
        transition: all 0.3s ease;
    ">
        🎙️ ACTIVATE COMM LINK
    </button>
</div>

<script>
    let recognizing = false;
    let recognition;

    if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
        const SpeechRec = window.SpeechRecognition || window.webkitSpeechRecognition;
        recognition = new SpeechRec();
        recognition.continuous = false;
        recognition.interimResults = false;
        recognition.lang = 'en-US'; // Supports Hinglish/English auto-mix

        recognition.onstart = function() {
            recognizing = true;
            const btn = document.getElementById('micBtn');
            btn.innerText = "🔴 LISTENING... SPEAK NOW";
            btn.style.borderColor = "#ff0055";
            btn.style.boxShadow = "0 0 25px rgba(255, 0, 85, 0.8)";
            btn.style.color = "#ff0055";
        };

        recognition.onresult = function(event) {
            const transcript = event.results[0][0].transcript;
            // Inject transcript directly into Streamlit's chat input field
            const chatInput = window.parent.document.querySelector('textarea[data-testid="stChatInputTextArea"]');
            if (chatInput) {
                chatInput.value = transcript;
                chatInput.dispatchEvent(new Event('input', { bubbles: true }));
                // Auto trigger send button
                setTimeout(() => {
                    const sendBtn = window.parent.document.querySelector('button[data-testid="stChatInputSubmitButton"]');
                    if (sendBtn) sendBtn.click();
                }, 200);
            }
        };

        recognition.onerror = function(event) {
            console.error("Speech Recognition Error:", event.error);
            resetBtn();
        };

        recognition.onend = function() {
            recognizing = false;
            resetBtn();
        };
    }

    function resetBtn() {
        const btn = document.getElementById('micBtn');
        btn.innerText = "🎙️ ACTIVATE COMM LINK";
        btn.style.borderColor = "#00f3ff";
        btn.style.boxShadow = "0 0 15px rgba(0, 243, 255, 0.4)";
        btn.style.color = "#00f3ff";
    }

    function toggleSpeech() {
        if (!recognition) {
            alert("Speech recognition is not supported in this browser. Please use Chrome/Edge.");
            return;
        }
        if (recognizing) {
            recognition.stop();
        } else {
            recognition.start();
        }
    }
</script>
"""

# Render Comm Link Button
components.html(voice_input_html, height=65)
