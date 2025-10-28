import subprocess
import sys
import os

def main():
    steps = [
        ("python create_db.py", "Creating database with schema"),
        ("python generate_data.py", "Generating data to CSV"),
        ("python load_to_db.py", "Loading data to database"),
    ]
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    for command, description in steps:
        print(f"\n{description}...")

        try:
            result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True, cwd=script_dir)
            print("Done")
        except subprocess.CalledProcessError as e:
            print(f"Failed (code {e.returncode}): {command}")
            if e.stdout.strip():
                print("Stdout:", e.stdout.strip())
            if e.stderr.strip():
                print("Stderr:", e.stderr.strip())
            sys.exit(1)
    
    print("\nSetup complete! Run 'python api.py' to start the API.")

if __name__ == "__main__":
    main()