# Netcheck

**Netcheck** is a simple container image that checks TCP connectivity to a list of targets specified in a CSV file.  
For each line in the CSV, it attempts to connect on a given port and prints `SUCCESS` or `FAILURE`.

---

## Table of Contents

1. [Overview](#overview)
2. [Building the Container](#building-the-container)
3. [Running the Container](#running-the-container)
    - [Default CSV](#default-csv)
    - [Mounting a Custom CSV](#mounting-a-custom-csv)
    - [Adjusting the Timeout](#adjusting-the-timeout)
4. [Sample Output](#sample-output)

---

## Overview

- **netcheck.py**:
  - Reads `/netcheck/input.csv` by default.
  - Each CSV line should have at least 3 fields: `Description, Target, Port`.
  - Tries a TCP connection to each `Target:Port` within a specified `TIMEOUT`.
  - Prints status in “real-time”:
    - First prints `Description,Target,Port,` immediately.
    - Then, after the check finishes, appends `SUCCESS` or `FAILURE`.

- **Dockerfile**:
  - Builds a minimal Python3 container.
  - Copies the script and a sample `input.csv` into the image.
  - Sets `TIMEOUT=10` by default (can be overridden).

---

## Building the Container

Build the container image locally by running:

```bash
docker build -t spurin/netcheck:latest .
```

This creates a local image called `netcheck` with the `latest` tag.

Alternatively, see the example in build.sh for multi-arch container builds.

---

## Running the Container

### Default CSV

By default, the container will read the CSV at `/netcheck/input.csv`, which is included in the image:

```bash
docker run --rm spurin/netcheck:latest
```

### Mounting a Custom CSV

If you have your own CSV file locally (e.g., `my_input.csv` in the current directory), you can mount it into the container at `/netcheck/input.csv`:

```bash
docker run --rm \
  -v $(pwd)/my_input.csv:/netcheck/input.csv \
  spurin/netcheck:latest
```

### Adjusting the Timeout

By default, each check has a 10-second timeout. You can override this via the `TIMEOUT` environment variable:

```bash
docker run --rm \
  -e TIMEOUT=5 \
  spurin/netcheck:latest
```

---

## Sample Output

When the container runs, it prints each line in two parts:

1. Immediately prints the CSV columns (minus status).
2. Once the check completes, prints `SUCCESS` or `FAILURE`.

Example:

```text
Description,Target,Port,Result
Google DNS,8.8.8.8,53,SUCCESS
Cloudflare DNS,1.1.1.1,53,SUCCESS
Google (HTTPS),www.google.com,443,SUCCESS
Example.org (HTTP),example.org,80,SUCCESS
hell.com (NUMBER),hell.com,666,FAILURE
```

*(Exact results depend on your network and what’s reachable)*
