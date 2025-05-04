import streamlit as st
import os
import tempfile
from models.voice_model import VoiceModel
from models.spiral_model import SpiralModel
from utils.audio_processor import AudioProcessor
from utils.image_processor import ImageProcessor
import matplotlib.pyplot as plt
import numpy as np
from login import login_page, logout, send_emergency_notification

# Set page config
st.set_page_config(
    page_title="Electro Spark - Parkinson's Disease Detection",
    page_icon="⚡",
    layout="wide"
)

# Initialize session state for authentication
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'username' not in st.session_state:
    st.session_state.username = None

# Initialize models
@st.cache_resource
def load_models():
    voice_model = VoiceModel()
    spiral_model = SpiralModel()
    return voice_model, spiral_model

# Initialize processors
audio_processor = AudioProcessor()
image_processor = ImageProcessor()

# Load models
voice_model, spiral_model = load_models()

# Check authentication
if not st.session_state.authenticated:
    login_page()
else:
    # Display welcome message and logout button in sidebar
    st.sidebar.write(f"Welcome, {st.session_state.username}!")
    if st.sidebar.button("Logout"):
        logout()
        st.experimental_rerun()

    # App title and description
    st.title("⚡ Electro Spark")
    st.subheader("Early Parkinson's Disease Detection using Voice and Spiral Analysis")

    # Create tabs for different input methods
    tab1, tab2 = st.tabs(["Voice Analysis", "Spiral Analysis"])

    # Voice Analysis Tab
    with tab1:
        st.header("Voice Analysis")
        st.write("Upload a voice recording for analysis")
        
        # File uploader for audio
        audio_file = st.file_uploader("Upload Audio File", type=['wav', 'mp3'])
        
        if audio_file is not None:
            try:
                # Save uploaded file temporarily
                with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as tmp_file:
                    tmp_file.write(audio_file.getvalue())
                    tmp_path = tmp_file.name
                
                # Process audio
                audio = audio_processor.load_audio(tmp_path)
                
                # Display audio player
                st.audio(audio_file)
                
                # Extract features
                mfccs = audio_processor.extract_mfcc(audio)
                spectral_features = audio_processor.extract_spectral_features(audio)
                temporal_features = audio_processor.extract_temporal_features(audio)
                
                # Make prediction
                prediction = voice_model.predict(tmp_path)
                
                # Display results with enhanced visualization
                col1, col2 = st.columns(2)
                
                with col1:
                    st.subheader("Analysis Results")
                    
                    # Create a more prominent prediction display
                    prediction_status = "Positive" if prediction['prediction'] == 1 else "Negative"
                    
                    # Color coding based on prediction
                    if prediction_status == "Positive":
                        st.error("⚠️ Parkinson's Disease Detection: Positive")
                        st.warning("Recommendation: Please consult a healthcare professional for further evaluation.")
                        
                        # Send emergency notification
                        if send_emergency_notification(st.session_state.username):
                            st.info("Emergency contacts have been notified.")
                        else:
                            st.warning("Could not send emergency notification. Please contact your emergency contacts manually.")
                    else:
                        st.success("✅ Parkinson's Disease Detection: Negative")
                
                with col2:
                    st.subheader("Voice Analysis")
                    st.write("Voice Parameters:")
                    if temporal_features:
                        for feature, value in temporal_features.items():
                            if isinstance(value, (np.ndarray, list)):
                                value = np.mean(value)  # Take mean if it's an array
                            st.write(f"• {feature}: {float(value):.2f}")
                    else:
                        st.write("No voice parameters available")
                
                # Clean up temporary file
                os.unlink(tmp_path)
                
            except Exception as e:
                st.error(f"An error occurred during processing: {str(e)}")
                st.info("Please make sure you're using a valid audio file in WAV or MP3 format.")

    # Spiral Analysis Tab
    with tab2:
        st.header("Spiral Analysis")
        st.write("Upload a spiral drawing image for analysis")
        
        # File uploader for image
        image_file = st.file_uploader("Upload Spiral Image", type=['png', 'jpg', 'jpeg'])
        
        if image_file is not None:
            try:
                # Save uploaded file temporarily
                with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as tmp_file:
                    tmp_file.write(image_file.getvalue())
                    tmp_path = tmp_file.name
                
                # Process image
                image = image_processor.load_image(tmp_path)
                processed_image = image_processor.preprocess_image(image)
                contours = image_processor.extract_contours(processed_image)
                
                # Make prediction
                prediction_result = spiral_model.predict(tmp_path)
                
                # Display results with enhanced visualization
                col1, col2 = st.columns(2)
                
                with col1:
                    st.subheader("Analysis Results")
                    
                    # Create a more prominent prediction display
                    prediction_status = "Positive" if prediction_result['prediction'] == 1 else "Negative"
                    
                    # Color coding based on prediction
                    if prediction_status == "Positive":
                        st.error("⚠️ Parkinson's Disease Detection: Positive")
                        st.warning("Recommendation: Please consult a healthcare professional for further evaluation.")
                        
                        # Send emergency notification
                        if send_emergency_notification(st.session_state.username):
                            st.info("Emergency contacts have been notified.")
                        else:
                            st.warning("Could not send emergency notification. Please contact your emergency contacts manually.")
                    else:
                        st.success("✅ Parkinson's Disease Detection: Negative")
                    
                    # Display detailed feature analysis
                    st.subheader("Spiral Analysis Metrics")
                    if prediction_result['features']:
                        metrics = {
                            'Circularity': prediction_result['features'].get('circularity', 0),
                            'Smoothness': prediction_result['features'].get('smoothness', 0),
                            'Regularity': prediction_result['features'].get('regularity', 0),
                            'Solidity': prediction_result['features'].get('solidity', 0)
                        }
                        
                        # Display metrics with progress bars
                        for metric, value in metrics.items():
                            st.write(f"{metric}:")
                            st.progress(float(value))
                    else:
                        st.warning("No features could be extracted from the image. Please ensure the image contains a clear spiral drawing.")
                
                with col2:
                    st.subheader("Spiral Analysis Visualization")
                    # Draw analysis on image
                    result_image = image_processor.draw_analysis(image, contours)
                    st.image(result_image, caption="Spiral Analysis", use_column_width=True)
                
                # Clean up temporary file
                os.unlink(tmp_path)
                
            except Exception as e:
                st.error(f"An error occurred during processing: {str(e)}")
                st.info("Please make sure you're using a valid image file in PNG, JPG, or JPEG format.")

    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center'>
        <p>Electro Spark - Early Parkinson's Disease Detection</p>
        <p>Built with  using Streamlit</p>
        <p style='color: #666; font-size: 0.8em;'>Note: This tool is for screening purposes only. Always consult healthcare professionals for medical diagnosis.</p>
    </div>
    """, unsafe_allow_html=True)