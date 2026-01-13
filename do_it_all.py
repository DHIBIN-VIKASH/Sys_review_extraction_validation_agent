
import os
import subprocess
import pandas as pd
import argparse
import time

# Configuration
EXTRACTOR_SCRIPT = 'gemini_extractor.py'
VALIDATION_SCRIPT = 'validation_agent.py'
DISCREPANCY_FILE = 'validation_discrepancies.xlsx'
OUTPUT_FILE = 'extracted_studies.xlsx'
ARTICLES_DIR = 'Articles'

def run_script(script_name, args=[]):
    """Runs a python script as a subprocess."""
    print(f"\n>>> Running {script_name} with args: {args}...")
    cmd = ['python', script_name] + args
    try:
        # We use subprocess.run so we can see the output in real-time if possible
        # or at least wait for it to finish.
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running {script_name}: {e}")
        return False
    return True

def get_failed_files():
    """Reads the discrepancy log and returns a list of files that failed validation."""
    if not os.path.exists(DISCREPANCY_FILE):
        return []
    
    df = pd.read_excel(DISCREPANCY_FILE)
    if 'Source File' not in df.columns or 'Status' not in df.columns:
        return []
    
    # Get unique filenames where Status is FAIL
    failed_files = df[df['Status'] == 'FAIL']['Source File'].unique().tolist()
    return [str(f) for f in failed_files if pd.notnull(f)]

def cleanup_failed_entries(failed_files):
    """Removes the failed entries from the main output file to allow re-extraction."""
    if not os.path.exists(OUTPUT_FILE) or not failed_files:
        return
    
    df = pd.read_excel(OUTPUT_FILE)
    # Remove rows where Source File is in failed_files
    initial_len = len(df)
    df = df[~df['Source File'].isin(failed_files)]
    
    if len(df) < initial_len:
        print(f"Cleaned up {initial_len - len(df)} failed entries from {OUTPUT_FILE} to prepare for re-extraction.")
        df.to_excel(OUTPUT_FILE, index=False)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--browser", default="chrome", help="Browser to use")
    parser.add_argument("--run-extraction", action="store_true", help="Manually run the initial extraction phase")
    args = parser.parse_args()

    # Clear previous logs to ensure we only heal NEW failures
    if os.path.exists(DISCREPANCY_FILE):
        try:
            os.remove(DISCREPANCY_FILE)
            print(f"Cleared old log: {DISCREPANCY_FILE}")
        except:
            pass

    # PHASE 1: Initial Extraction (Skipped by default as per user request)
    if args.run_extraction:
        print("\n=== PHASE 1: INITIAL EXTRACTION (Manual Override) ===")
        run_script(EXTRACTOR_SCRIPT, ['--browser', args.browser])
    else:
        print("\n=== PHASE 1: INITIAL EXTRACTION (SKIPPED) ===")
        print("Note: Extraction is assumed to be completed by the external agent.")
    
    # PHASE 2: Initial Validation (Now the primary first step)
    print("\n=== PHASE 2: INITIAL VALIDATION ===")
    run_script(VALIDATION_SCRIPT, ['--browser', args.browser])
    
    # PHASE 3: Self-Healing Loop
    print("\n=== PHASE 3: SELF-HEALING (RE-EXTRACT FAILURES) ===")
    failed_files = get_failed_files()
    
    if not failed_files:
        print("No validation failures found. Pipeline complete!")
        return

    print(f"Found {len(failed_files)} files with discrepancies: {failed_files}")
    
    # Prepare for re-extraction by removing old failed data
    cleanup_failed_entries(failed_files)
    
    # Re-run extraction specifically for these files
    # Note: gemini_extractor.py currently processes everything not in the Excel file.
    # Since we removed them, it will naturally pick them up again.
    # We might want to pass them explicitly if we wanted to be more precise,
    # but the current logic works well for resume.
    print(f"Re-triggering extraction for {len(failed_files)} files...")
    run_script(EXTRACTOR_SCRIPT, ['--browser', args.browser])
    
    # Final Validation Check
    print("\n=== PHASE 4: FINAL VALIDATION OF HEALED DATA ===")
    run_script(VALIDATION_SCRIPT, ['--browser', args.browser])
    
    print("\nMaster Orchestration Complete.")

if __name__ == "__main__":
    main()
