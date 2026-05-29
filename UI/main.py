import streamlit as st
import pandas as pd
import requests
import base64
from pathlib import Path

# --- Configuration & Styling ---
st.set_page_config(page_title="Sports Person Classifier", page_icon="⚽", layout="wide")

custom_css = """
<style>
    .player-card {
        display: flex; flex-direction: column; align-items: center; justify-content: center;
        padding: 1rem; background: white; border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1); transition: transform 0.3s ease; margin-bottom: 1rem;
    }
    .player-card:hover { transform: translateY(-5px); box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1); }
    .circle-img {
        width: 120px; height: 120px; border-radius: 50%; object-fit: cover;
        border: 4px solid #f7fafc; box-shadow: 0 1px 3px rgba(0,0,0,0.12); margin-bottom: 1rem;
    }
    .player-name { font-weight: 600; text-transform: uppercase; color: #2d3748; font-size: 1.1rem; text-align: center; }
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# Presentation mapping for clean UI output
PLAYER_DISPLAY_NAMES = {
    "lionel_messi": "Lionel Messi",
    "maria_sharapova": "Maria Sharapova",
    "roger_federer": "Roger Federer",
    "serena_williams": "Serena Williams",
    "virat_kohli": "Virat Kohli"
}

# --- Service Layer ---
def classify_image(file_bytes, mime_type):
    """Encapsulates the external API interaction and data parsing."""
    url = "https://celebrity-classifier-nitin-pant.streamlit.app/classify_image"
    
    # Construct the dataURL format expected by the API
    b64_str = base64.b64encode(file_bytes).decode('utf-8')
    data_url = f"data:{mime_type};base64,{b64_str}"
    
    try:
        response = requests.post(url, data={'image_data': data_url}, timeout=15)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"API Connection Error: {str(e)}")
        return None

def find_best_match(api_data):
    """Replicates the JS logic to find the face with the highest probability score."""
    if not api_data or len(api_data) == 0:
        return None
        
    best_match = None
    best_score = -1
    
    for face in api_data:
        max_score = max(face['class_probability'])
        if max_score > best_score:
            best_score = max_score
            best_match = face
            
    return best_match

# --- UI Layout ---
st.markdown("<h1 style='text-align: center; color: #2b6cb0; margin-bottom: 2rem;'>Sports Person Classifier</h1>", unsafe_allow_html=True)

# 1. Player Roster
script_dir = Path(__file__).parent.resolve()
images_path = script_dir / "images"
f"Hello, {user_name}!"
players = [
    {"id": "lionel_messi", "name": "Lionel Messi", "img": f"{images_path}messi.jpeg"},
    {"id": "maria_sharapova", "name": "Maria Sharapova", "img": f"{images_path}sharapova.jpeg"},
    {"id": "roger_federer", "name": "Roger Federer", "img":  f"{images_path}federer.jpeg"},
    {"id": "serena_williams", "name": "Serena Williams", "img":  f"{images_path}serena.jpeg"},
    {"id": "virat_kohli", "name": "Virat Kohli", "img":  f"{images_path}virat.jpeg"}
]

cols = st.columns(5)
for idx, player in enumerate(players):
    with cols[idx]:
        try:
            with open(player["img"], "rb") as f:
                img_data = base64.b64encode(f.read()).decode()
            img_src = f"data:image/jpeg;base64,{img_data}"
        except FileNotFoundError:
            img_src = "https://via.placeholder.com/120"
            
        st.markdown(f"""
        <div class="player-card">
            <img src="{img_src}" class="circle-img" alt="{player['name']}">
            <div class="player-name">{player['name']}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("---")

# 2. Application Interaction Area
col1, col2 = st.columns(2)

with col1:
    st.subheader("Upload Image")
    uploaded_file = st.file_uploader("Drop files here or click to upload", type=["jpg", "jpeg", "png"])
    
    if uploaded_file is not None:
        st.image(uploaded_file, caption="Uploaded Image", use_container_width=True)
    
    classify_btn = st.button("Classify Image", type="primary", use_container_width=True)

with col2:
    st.subheader("Classification Results")
    
    if classify_btn:
        if uploaded_file is None:
            st.warning("Please upload an image first.")
        else:
            with st.spinner('Analyzing image via API...'):
                raw_data = classify_image(uploaded_file.getvalue(), uploaded_file.type)
                match = find_best_match(raw_data)
                
                if not match:
                    st.error("**Classification Failed:** The model was unable to detect a face and two eyes clearly. Please try a different image.")
                else:
                    detected_class = match['class']
                    display_name = PLAYER_DISPLAY_NAMES.get(detected_class, detected_class.replace('_', ' ').title())
                    
                    st.success(f"Successfully classified as: **{display_name}**")
                    
                    # Construct DataFrame from the matched probability data
                    class_dict = match['class_dictionary']
                    probabilities = match['class_probability']
                    
                    table_data = []
                    for person_id, index in class_dict.items():
                        person_name = PLAYER_DISPLAY_NAMES.get(person_id, person_id)
                        score = probabilities[index]
                        table_data.append({
                            "Player": person_name,
                            "Probability Score": f"{score:.2f}%"
                        })
                    
                    df = pd.DataFrame(table_data)
                    st.dataframe(df, use_container_width=True, hide_index=True)
    else:
        st.info("Upload an image and click 'Classify Image' to see results.")
