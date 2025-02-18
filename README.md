# Netcheck

**Netcheck** is a container-based tool that checks TCP connectivity for a list of host/port pairs.
It reads a CSV file, attempts connections, and prints results in real time.

Key features:

- **Expected State** (`OPEN` or `CLOSED`):
  - If expected is `OPEN`, the check passes only if a connection succeeds.
  - If expected is `CLOSED`, the check passes only if a connection fails.
  - If a row is missing or omits the 4th column, it defaults to `OPEN`.
- **Real-Time Output**:
  - Prints the CSV row (minus the final status) immediately.
  - After the TCP check completes, appends `SUCCESS` or `FAILURE` on the same line.
- **Timeout**:
  - By default, each check is attempted with a timeout for `OPEN` or `CLOSED` ports
  - Override the `OPEN` default of 10 seconds with the `TIMEOUT_OPEN` environment variable.
  - Override the `CLOSED` default of 1 seconds with the `TIMEOUT_CLOSED` environment variable.

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

Netcheck expects **4 columns** in each row of `/netcheck/input.csv`:

```
Description,Target,Port,Expected
```

- **Description**: Arbitrary text (friendly name)
- **Target**: A hostname or IP address
- **Port**: TCP port number
- **Expected**: Either `OPEN` or `CLOSED`
  - If missing or invalid, defaults to `OPEN`.

Example:

```
Google DNS,8.8.8.8,53
Cloudflare DNS,1.1.1.1,53
Google (HTTPS),www.google.com,443
Example.org (HTTP),example.org,80
hell.com (NUMBER),hell.com,666,CLOSED
```

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

By default, each OPEN/CLOSED check has a unique timeout. You can override these via the `TIMEOUT_OPEN` and `TIMEOUT_CLOSED` environment variables:

```bash
docker run --rm \
  -e TIMEOUT_CLOSED=10 \
  spurin/netcheck:latest
```

---

## Sample Output

When the container runs, it prints each line in two parts:

1. Immediately prints the CSV columns (minus status).
2. Once the check completes, prints `SUCCESS` or `FAILURE`.

Example:

```text
Description,Target,Port,Expected,TestResult
Google DNS,8.8.8.8,53,OPEN,SUCCESS
Cloudflare DNS,1.1.1.1,53,OPEN,SUCCESS
Google (HTTPS),www.google.com,443,OPEN,SUCCESS
Example.org (HTTP),example.org,80,OPEN,SUCCESS
hell.com (NUMBER),hell.com,666,CLOSED,SUCCESS
```

*(Exact results depend on your network and what’s reachable)*
