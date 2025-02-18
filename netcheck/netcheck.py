#!/usr/bin/env python3
import csv
import os
import socket
import sys

def check_connectivity(host, port, timeout):
    """Attempt to connect to a given host and port within the specified timeout.
       Returns True if the connection succeeds, False otherwise.
    """
    try:
        with socket.create_connection((host, int(port)), timeout):
            return True
    except Exception:
        return False

def main():
    # Two separate timeouts:
    #  - TIMEOUT_OPEN   -> used if expected == "OPEN"   (defaults to 10s)
    #  - TIMEOUT_CLOSED -> used if expected == "CLOSED" (defaults to 1s)
    timeout_open = float(os.environ.get("TIMEOUT_OPEN", "10"))
    timeout_closed = float(os.environ.get("TIMEOUT_CLOSED", "1"))

    input_file = "/netcheck/input.csv"
    
    if not os.path.exists(input_file):
        print(f"[ERROR] CSV file not found at {input_file}", flush=True)
        sys.exit(1)

    # Read CSV file
    with open(input_file, "r", newline="") as f:
        csv_reader = csv.reader(f)

        # Print heading (optional)
        print("Description,Target,Port,Expected,TestResult", flush=True)

        for row in csv_reader:
            # Skip invalid/empty lines
            if len(row) < 3:
                continue

            description = row[0]
            target      = row[1]
            port        = row[2]

            # If a 4th column (Expected) is given, read it; otherwise default to "OPEN"
            expected = row[3].strip().upper() if len(row) >= 4 else "OPEN"
            if expected not in ("OPEN", "CLOSED"):
                expected = "OPEN"

            # Print partial line first, no newline yet
            print(f"{description},{target},{port},{expected},", end='', flush=True)

            # Determine which timeout to use
            if expected == "OPEN":
                is_open = check_connectivity(target, port, timeout_open)
                test_result = "SUCCESS" if is_open else "FAILURE"
            else:  # expected == "CLOSED"
                # For "CLOSED", we only wait up to timeout_closed seconds
                is_open = check_connectivity(target, port, timeout_closed)
                # If connection fails, that means it's closed, so success
                test_result = "FAILURE" if is_open else "SUCCESS"

            # Print final status with newline
            print(test_result, flush=True)

if __name__ == "__main__":
    main()
