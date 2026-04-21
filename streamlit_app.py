import streamlit as st
import os
from ultralytics import YOLO
import glob


st.set_page_config(layout="wide")
st.title("Pothole Detection and Tracking App")

# --- Model Loading ---
@st.cache_resource
def load_yolo_model():
    # Use local path for weights
    weights_paths = glob.glob('./runs/detect/train*/weights/best.pt')
    if not weights_paths:
        st.error("No YOLO model weights found at ./runs/detect. Please train the model first.")
        return None

    # Get the most recently created weights file
    latest_weights = max(weights_paths, key=os.path.getctime)
    return YOLO(latest_weights)

model = load_yolo_model()

if model:
    st.success("YOLO Model loaded successfully!")

    # Create tabs for different modes
    tab1, tab2, tab3 = st.tabs(["Upload Image", "Upload Video", "Live Webcam"])

    with tab1:
        st.header("Upload an Image")
        uploaded_file = st.file_uploader("Choose an image", type=["jpg", "jpeg", "png"])
        if uploaded_file is not None:
            # Save the uploaded file temporarily to process with YOLO
            temp_image_path = os.path.join("/tmp", uploaded_file.name)
            with open(temp_image_path, "wb") as f:
                f.write(uploaded_file.getbuffer())

            st.image(uploaded_file, caption='Uploaded Image', use_column_width=True)
            st.write("Detecting potholes...")
            results = model.predict(temp_image_path, save=True, imgsz=640, conf=0.25)

            if results and results[0]: # Ensure results arent empty
                # Find the latest predict directory
                predict_results_dirs = glob.glob('./runs/detect/predict*')
                if predict_results_dirs:
                    latest_predict_dir = max(predict_results_dirs, key=os.path.getctime)
                    predicted_image_name = os.path.basename(temp_image_path)
                    predicted_image_path = os.path.join(latest_predict_dir, predicted_image_name)

                    if os.path.exists(predicted_image_path):
                        st.image(predicted_image_path, caption='Detection Results', use_column_width=True)
                    else:
                        st.warning(f"Could not find the annotated image at {predicted_image_path}. It might not have been saved correctly.")
                else:
                    st.warning("No prediction output directories found.")
                os.remove(temp_image_path) # Clean up temporary file
            else:
                st.warning("No detection results returned by the model or output path not available.")

    with tab2:
        st.header("Upload a Video")
        uploaded_video = st.file_uploader("Choose a video", type=["mp4", "avi", "mov"])
        if uploaded_video is not None:
            st.video(uploaded_video)
            st.write("Running tracking on video. This may take a while...")
            file_ext = os.path.splitext(uploaded_video.name)[1]
            video_path = f"temp_video{file_ext}"
            with open(video_path, "wb") as f:
                f.write(uploaded_video.getbuffer())
            results = model.track(source=video_path, show=False, save=True, tracker="bytetrack.yaml")
            st.success("Video tracking complete! Output saved to ./runs/detect/track/ folder.")
            os.remove(video_path)

        with tab3:
            st.header("Live Webcam Detection")
            st.write("Click START to enable your webcam for real-time pothole detection.")
            st.info("⚠️ Note: This feature requires a webcam and browser camera access. Performance depends on your device.")

            try:
                from streamlit_webrtc import webrtc_streamer, VideoTransformerBase, RTCConfiguration
                import av

                class VideoProcessor(VideoTransformerBase):
                    def __init__(self, model_instance):
                        self.model = model_instance
                        self.frame_count = 0
                        self.skip_frames = 2  # Process every 3rd frame for better performance

                    def recv(self, frame: av.VideoFrame) -> av.VideoFrame:
                        try:
                            # Skip frames for performance
                            self.frame_count += 1
                            if self.frame_count % (self.skip_frames + 1) != 0:
                                return frame
                            
                            # Convert frame to numpy array
                            img = frame.to_ndarray(format="bgr24")
                            
                            # Run YOLO inference
                            results = self.model.predict(img, conf=0.25, verbose=False)
                            
                            # Plot bounding boxes if detections found
                            if results and len(results) > 0 and results[0].boxes is not None:
                                annotated_frame = results[0].plot()
                            else:
                                annotated_frame = img
                            
                            return av.VideoFrame.from_ndarray(annotated_frame, format="bgr24")
                        
                        except Exception as e:
                            st.warning(f"Error processing frame: {str(e)}")
                            return frame

                # RTCConfiguration for better connection stability
                rtc_configuration = RTCConfiguration(
                    {"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]}
                )

                webrtc_streamer(
                    key="pothole-detection",
                    video_processor_factory=lambda: VideoProcessor(model),
                    rtc_configuration=rtc_configuration,
                    media_stream_constraints={"video": True, "audio": False}
                )
                
                st.caption("💡 Tip: Every 3rd frame is processed for better performance. Detections are shown in real-time.")

            except ImportError:
                st.error("❌ streamlit-webrtc is not installed. Run: pip install streamlit-webrtc")
else:
    st.info("YOLO model not loaded. Please ensure the model is trained and weights are available.")
    