from pathlib import Path
import subprocess
import sys

from cleandata import main as clean_data
from question import main as answer_questions


# Run the full project
def main():
    # Clean the original data
    print("\n-Cleaning the data...")
    clean_data()

    # Print the answers to the required questions
    print("\n-Answering the questions...")
    answer_questions()

    # Start the Streamlit interface
    print("\n-Starting the interface...")

    base_dir = Path(__file__).resolve().parent
    interface_path = base_dir / "interface.py"

    try:
       subprocess.run(
        [ sys.executable,"-m",
                "streamlit",
                "run",
                str(interface_path)
            ],
            check=True
        )

    except KeyboardInterrupt:
        print("\nInterface stopped.")


if __name__ == "__main__":
    main()