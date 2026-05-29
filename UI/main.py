import streamlit as st
import pandas as pd
import time

# 1. Page Configuration
st.set_page_config(
    page_title="Sports Person Classifier",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 2. Targeted CSS Injection
# We inject minimal CSS to recreate the circular card styling without breaking Streamlit's native theme.
custom_css = """
<style>
    .player-card {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        padding: 1rem;
        background: white;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        transition: transform 0.3s ease;
        margin-bottom: 1rem;
    }
    .player-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
    }
    .circle-img {
        width: 120px;
        height: 120px;
        border-radius: 50%;
        object-fit: cover;
        border: 4px solid #f7fafc;
        box-shadow: 0 1px 3px rgba(0,0,0,0.12);
        margin-bottom: 1rem;
    }
    .player-name {
        font-weight: 600;
        text-transform: uppercase;
        color: #2d3748;
        font-size: 1.1rem;
        text-align: center;
    }
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# 3. Header
st.markdown("<h1 style='text-align: center; color: #2b6cb0; margin-bottom: 2rem;'>Sports Person Classifier</h1>", unsafe_allow_html=True)

# 4. Player Roster (Top Section)
# Define players and their local image paths (matching your HTML structure)
players = [
    {"name": "Lionel Messi", "img": "./images/messi.jpeg"},
    {"name": "Maria Sharapova", "img": "./images/sharapova.jpeg"},
    {"name": "Roger Federer", "img": "./images/federer.jpeg"},
    {"name": "Serena Williams", "img": "./images/serena.jpeg"},
    {"name": "Virat Kohli", "img": "./images/virat.jpeg"}
]

# Create 5 columns for the roster
cols = st.columns(5)
for idx, player in enumerate(players):
    with cols[idx]:
        # Using a try-except block to handle missing images gracefully during development
        try:
            # We encode the image to base64 to inject it cleanly into the HTML block
            import base64
            with open(player["img"], "rb") as f:
                img_data = base64.b64encode(f.read()).decode()
            img_src = f"data:image/jpeg;base64,{img_data}"
        except FileNotFoundError:
            # Fallback placeholder if local image is missing
            img_src = "https://via.placeholder.com/120"
            
        card_html = f"""
        <div class="player-card">
            <img src="{img_src}" class="circle-img" alt="{player['name']}">
            <div class="player-name">{player['name']}</div>
        </div>
        """
        st.markdown(card_html, unsafe_allow_html=True)

st.markdown("---")

# 5. Application Interaction Area
col1, col2 = st.columns(2)

with col1:
    st.subheader("Upload Image")
    # Streamlit's native replacement for Dropzone
    uploaded_file = st.file_uploader("Drop files here or click to upload", type=["jpg", "jpeg", "png"])
    
    if uploaded_file is not None:
        st.image(uploaded_file, caption="Uploaded Image", use_container_width=True)
    
    classify_btn = st.button("Classify Image", type="primary", use_container_width=True)

with col2:
    st.subheader("Classification Results")
    
    # State Management: Only process/show results if button is clicked AND file exists
    if classify_btn:
        if uploaded_file is None:
            st.error("**Classification Failed:** Please upload an image first.")
        else:
            with st.spinner('Analyzing image...'):
                # MOCK BACKEND PROCESSING - Replace with actual model inference
                time.sleep(1.5) 
                
                # Mock result: Assuming the model detected Federer
                mock_success = True 
                
                if not mock_success:
                    st.error("**Classification Failed:** The model was unable to detect a face and two eyes clearly. Please try a different image.")
                else:
                    st.success("Successfully classified as: **Roger Federer**")
                    
                    # Probability Data Table
                    data = {
                        "Player": ["Lionel Messi", "Maria Sharapova", "Roger Federer", "Serena Williams", "Virat Kohli"],
                        "Probability Score": ["2.1%", "0.5%", "94.2%", "1.1%", "2.1%"]
                    }
                    df = pd.DataFrame(data)
                    
                    # Streamlit's native table is cleaner and automatically handles the layout you defined in app.css
                    st.table(df)
    else:
        st.info("Upload an image and click 'Classify Image' to see results.")
