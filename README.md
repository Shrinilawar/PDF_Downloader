# PDF Downloader

This repository contains a Streamlit-based application for downloading PDF files from given URLs. The application uses Python and includes support for both static and dynamic content handling with the help of libraries like `requests`, `beautifulsoup4`, and `selenium`.

---

## Features

- Allows manual entry of PDF URLs or uploads of `.txt` files containing URLs.
- Saves downloaded PDFs in a specified folder (`downloaded_pdfs` by default).
- Skips re-downloading existing PDFs.
- Gracefully handles invalid URLs and logs errors for failed downloads.
- Provides a user-friendly interface with gradient styling inspired by Instagram.

---

## Installation

### Prerequisites
- Python 3.8 or higher.
- Ensure the following libraries are installed:
  - `streamlit`
  - `requests`
  - `beautifulsoup4`
  - `selenium`
  - `pandas`

### Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/pdf_downloader.git
   cd pdf_downloader
   ```

2. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Download the appropriate WebDriver for Selenium (e.g., ChromeDriver):
   - Make sure the driver version matches your browser version.
   - Add the driver to your system's PATH or specify its location in the script.

---

## Usage

### Running Locally
1. Start the application:
   ```bash
   streamlit run secEnd.py
   ```

2. Access the app in your browser at `http://localhost:8501`.

3. Follow these steps:
   - Choose an input method (manual entry or file upload).
   - Provide the URLs or upload a `.txt` file containing the URLs.
   - Specify an output folder (default: `downloaded_pdfs`).
   - Click the **Download PDFs** button to begin downloading.


---

## Folder Structure
```
pdf_downloader/
|-- main.py                 # Core logic for downloading PDFs
|-- secEnd.py               # Streamlit application code
|-- requirements.txt        # Python dependencies
|-- downloaded_pdfs/        # Default output folder for PDFs
|-- README.md               # Documentation
```

---

## Troubleshooting

### Common Issues
1. **Missing `bs4` or `selenium`:**
   - Ensure these are included in `requirements.txt` and installed using `pip install -r requirements.txt`.

2. **WebDriver not found:**
   - Verify the WebDriver path and ensure it's compatible with your browser.

3. **Streamlit deployment errors:**
   - Check logs for missing dependencies and update `requirements.txt` as needed.

---

## License
This project is licensed under the MIT License.

---

## Contribution
Feel free to contribute by creating issues or submitting pull requests. For major changes, please open a discussion first to propose your ideas.

---

## Contact
For any queries, reach out at `your-email@example.com`.
