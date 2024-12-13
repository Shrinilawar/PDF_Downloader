import streamlit as st
import os
import time
from main import PDFDownloader
import tempfile

# Configure page settings
st.set_page_config(
    page_title="PDF Downloader",
    page_icon="📄",
    layout="wide"
)

# Custom CSS for frosted glass effect and Instagram color palette
st.markdown("""
    <style>
    .st-emotion-cache-13k62yr{
            background: rgb(131,58,180);
            background: linear-gradient(90deg, rgba(131,58,180,1) 0%, rgba(253,29,128,1) 100%);
                        }


    /* Instagram-inspired colors */
    :root {
        --ig-gradient: linear-gradient(135deg, #833AB4, #C13584, #E1306C, #FD1D1D);
        --ig-button: linear-gradient(90deg, #405DE6, #833AB4);
    }

    /* Button styling */
    .stButton>button {
        background: var(--ig-button) !important;
        color: white !important;
        font-weight: bold !important;
        border: none;
        border-radius: 10px;
        padding: 0.5rem 1rem;
        transition: all 0.3s ease;
    }

    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0px 4px 15px rgba(0, 0, 0, 0.2);
    }

    /* Centered progress text */
    .stProgress > div > div {
        background: var(--ig-gradient) !important;
        border-radius: 10px;
    }

    /* Adjust title and container */
    h1 {
        text-align: center;
        color: white;
        margin-bottom: 1.5rem;
    }

    .stTextArea textarea {
        font-family: monospace;
    }
    </style>
""", unsafe_allow_html=True)

def create_temp_links_file(urls):
    """Create a temporary file with the provided URLs."""
    temp_file = tempfile.NamedTemporaryFile(mode='w+', delete=False, suffix='.txt')
    for url in urls:
        temp_file.write(f"{url}\n")
    temp_file.close()
    return temp_file.name

def main():
    st.title("📄 PDF Downloader")
    st.write("Enter PDF URLs or upload a text file containing URLs.")

    # Add radio button for input method selection
    input_method = st.radio(
        "Choose input method:",
        ("Enter URLs manually", "Upload .txt file")
    )

    urls = []
    
    if input_method == "Enter URLs manually":
        # Text area for URL input
        default_text = """https://www.ebharatisampat.in/ebook/index.php?bookid=MjM1OTE2NTk3NzQ1MDI3#book/
https://ebharatisampat.in/readunicode.php?id=MDU1NTIyNDI3MTczMjI3
https://www.ebharatisampat.in/pdfs/Intermediate_Prartical_Botany-hi.pdf
https://ebharatisampat.in/readunicode.php?id=OD3"""
        
        urls_input = st.text_area(
            "Enter PDF URLs (one per line):",
            height=200,
            placeholder=default_text
        )
        if urls_input.strip():
            urls = [url.strip() for url in urls_input.splitlines() if url.strip()]
    else:
        # File uploader
        uploaded_file = st.file_uploader("Upload a .txt file containing URLs", type=['txt'])
        if uploaded_file is not None:
            content = uploaded_file.getvalue().decode()
            urls = [url.strip() for url in content.splitlines() if url.strip()]
            if urls:
                st.success(f"Successfully loaded {len(urls)} URLs from file")
            else:
                st.warning("No valid URLs found in the uploaded file")

    # Output directory selection
    output_dir = st.text_input(
        "Output Directory:",
        value="downloaded_pdfs",
        help="Enter the directory where PDFs will be saved"
    )

    if st.button("Download PDFs", type="primary"):
        if not urls:
            st.error("Please enter at least one URL or upload a file containing URLs")
            return

        # Progress and status display
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        try:
            # Create temporary file with URLs
            temp_file_path = create_temp_links_file(urls)
            
            # Initialize downloader 
            downloader = PDFDownloader(output_folder=output_dir)
            
            # Process each URL
            total_urls = len(urls)
            for i, url in enumerate(urls, 1):
                # Update progress
                progress = int((i / total_urls) * 100)
                progress_bar.progress(progress)
                status_text.text(f"Processing URL {i} of {total_urls}")
                
                # Process URL 
                try:
                    # Try to download the PDF
                    downloader.process_url(url)
                except Exception as e:
                    st.warning(f"Error downloading {url}: {str(e)}")
                


            # Cleanup
            downloader.cleanup()
            os.unlink(temp_file_path)
            
            # Final status
            progress_bar.progress(100)
            status_text.text("Download process completed!")
            
            # Display downloaded file names
            downloaded_files = os.listdir(output_dir)
            if downloaded_files:
                st.success(f"Downloads completed! The following files were downloaded:")
                for file in downloaded_files:
                    st.write(f"✅ {file}")
            else:
                st.warning("No files were successfully downloaded.")

        except Exception as e:
            st.error(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()