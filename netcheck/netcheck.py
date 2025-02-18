#!/usr/bin/env python3
import csv
import os
import socket
import sys

def check_connectivity(host, port, timeout):
    """Attempt to connect to a given host and port within the specified timeout.

    Returns True if connection succeeds, False otherwise.
    """
    try:
        with socket.create_connection((host, int(port)), timeout):
            return True
    except Exception:
        return False

def main():
    # Read the timeout from the environment or default to 10 seconds
    timeout = float(os.environ.get("TIMEOUT", "10"))

    input_file = "/netcheck/input.csv"
    
    if not os.path.exists(input_file):
        print(f"[ERROR] CSV file not found at {input_file}", flush=True)
        sys.exit(1)

    # Read CSV file
    with open(input_file, "r", newline="") as f:
        csv_reader = csv.reader(f)

        # Optional: print CSV header
        print("Description,Target,Port,Result", flush=True)

        for row in csv_reader:
            if len(row) < 3:
                # Skip invalid lines or handle as needed
                continue

            description, target, port = row[0], row[1], row[2]

            # Print partial line immediately (no newline yet)
            # so the user sees which line is currently being processed.
            print(f"{description},{target},{port},", end='', flush=True)

            # Attempt connectivity
            success = check_connectivity(target, port, timeout)
            status = "SUCCESS" if success else "FAILURE"

            # Print result with newline, also flushed immediately
            print(status, flush=True)

if __name__ == "__main__":
    main()
