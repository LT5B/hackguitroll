import subprocess
import sys

GREEN_COLOR = "\033[32m"
RESET_COLOR = "\033[0m"

def main():
    for _ in range(100):
        sys.stdout.write(GREEN_COLOR)
        sys.stdout.flush()
        
        subprocess.run(["find", "."], shell=False)

if __name__ == "__main__":
    try:
        main()
    finally:
        sys.stdout.write(RESET_COLOR)
        sys.stdout.flush()
