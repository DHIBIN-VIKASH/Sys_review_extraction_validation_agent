# 🤖 Study Checker & Fixer

This tool checks your study data for mistakes and tries to fix them automatically.

---

## 🚀 Quick Start

### 1. Prepare your files
*   Place all your study PDF files into the folder named **`Articles`**.
*   This repo includes a **`template_extracted_studies.xlsx`**. You should rename this to **`extracted_studies.xlsx`** and fill in your initial extracted data before running the fixer.

### 2. Run the tool
Just run this command:
```powershell
python do_it_all.py --browser chrome
```

### 3. Log in to Gemini
*   A Chrome browser window will open automatically.
*   **Action Required:** If you aren't logged in, please sign in to your Google Gemini account.
*   Once you see the Gemini chat interface, **just wait**. The agent will detect your login and start working immediately.

---

## 🛠️ What happens behind the scenes?

The pipeline runs in 3 automatic phases in this workspace:

1.  **Phase 1: Validation (Start Here)**: The agent takes the Excel data (extracted by the external agent) and double-checks every piece of data against the original PDF in the `Articles` folder. Any errors found are logged in `validation_discrepancies.xlsx`.
2.  **Phase 2: Self-Healing**: This is where the agent fixes errors. For every file that "Failed" validation, the agent automatically triggers a targeted re-extraction to try and get the correct data.
3.  **Phase 3: Final Check**: A final validation pass is run on the newly corrected data to ensure the healed entries are now 100% accurate.

*Note: The initial bulk extraction of all files is handled by your other agent in a separate folder.*

---

## 📈 Troubleshooting & Logic

*   **"Blank Tab" or "Not Loading"**: We use a local browser profile located at `C:\Users\HP\gemini_chrome_profile` to prevent OneDrive from locking files. If the page doesn't load, try closing all other Chrome windows and restarting.
*   **"NO DATA" logs**: If you see "NO DATA" in the discrepancy log, it means the row in the Excel sheet was empty. The agent will correctly skip these and move to the next "next" valid row.
*   **Browser Window**: Keep the Chrome window open. Don't close it until the terminal says it's finished.

---

## 📂 Key Files
*   `Articles/`: Your PDFs.
*   `extracted_studies.xlsx`: Your data.
*   `validation_discrepancies.xlsx`: Where the errors are logged.
*   `do_it_all.py`: The only file you need to run.

---

## ⚙️ Customization & Open Source

This project is built to be flexible! Feel free to modify the code to suit your specific research needs.

*   **Internet Speed**: If you have a very slow or very fast connection, you can adjust the `timeout` and `time.sleep` values in `validation_agent.py` and `gemini_extractor.py`. Search for `# SMART WAIT` in the code to find the best places to tweak.
*   **Prompting Logic**: You can customize the extraction rules by editing the `create_validation_prompt` function in the script files.
*   **Browser Choice**: While Chrome is recommended, you can try running with `--browser edge` if you have it installed.

---
*Developed for Advanced Agentic Coding Projects.*
