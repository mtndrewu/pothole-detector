import streamlit as st
from PIL import Image
# import cv2
# import numpy as np
import tempfile

st.set_page_config(page_title="Pothole Detection Dashboard", layout="wide")

st.title("Pothole Detection Dashboard")

# top area: image/video feed pane
st.markdown("## Live Input Preview")
input_container = st.empty()

# left and right panes
left_col, right_col = st.columns([1, 1])

with left_col:
    st.subheader("Input Source")
    uploaded_file = st.file_uploader("Choose an image or mp4 video", type=[
                                     "png", "jpg", "jpeg", "mp4"])

    if uploaded_file is not None:
        file_details = {
            "filename": uploaded_file.name,
            "filetype": uploaded_file.type,
            "filesize": uploaded_file.size,
        }
        st.write(file_details)

with right_col:
    st.subheader("Classification Results")
    st.write("Model is not available yet, showing dummy output to validate layout.")
    result_placeholder = st.empty()

# render preview
if uploaded_file is not None:
    if uploaded_file.type.startswith("image"):
        image = Image.open(uploaded_file)
        with input_container:
            st.image(image, caption="Selected image")

        # placeholder classification
        result_placeholder.info(
            "Detected: pothole-like pattern (dummy). Confidence: 0.00%")

    elif uploaded_file.type == "video/mp4":
        tfile = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4")
        tfile.write(uploaded_file.read())

        with input_container:
            st.video(tfile.name)

        result_placeholder.info(
            "Detected: no pothole (dummy) in video frames.")

else:
    with input_container:
        st.write("Upload an image or mp4 file to preview here.")
    result_placeholder.info("No input selected.")

st.markdown("---")
st.write("Use this dashboard as the skeleton for integrating your pothole model. Replace the dummy result with your model inference code in the classification/results section.")
