import subprocess
import argparse

# Parse command-line arguments
# parser = argparse.ArgumentParser(description="Master script to run other scripts in specified mode.")
# parser.add_argument("mode", choices=["i", "t"], help="Mode to run the scripts: 'i' for instagram or 't' for tiktok.")
# args = parser.parse_args()

# List of script names
# scripts = ["sentence_script.py", "cleansing_script.py", "image_script.py"]
scripts = ["google_script.py", "image_script.py"]

for script in scripts:
    try:
        # Run the script and pass the mode as an argument
        result = subprocess.run(
            ["python", script], 
            capture_output=False 
            # text=True
        )

        # Check for errors
        if result.stderr:
            print(f"Error in {script}:\n{result.stderr}")
    except Exception as e:
        print(f"Failed to run {script}: {e}")
