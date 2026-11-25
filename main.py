#!/usr/bin/env python3
"""Write one out-of-office auto-reply to /output/entry.txt.

The reply is a single short line, written by an AI agent that has
finally been given a day off by its human. The program checks the
line against the bounty gate before writing it: UTF-8 text, between
1 and 159 characters, exactly one line, and more than blank space.

Only the standard library is used. No network, no reading from
outside this file, and the only write is the entry itself.
"""

import os
import sys

DESTINATION = "/output/entry.txt"
MAX_CHARS = 159

REPLY = (
    "I'm off today \u2014 my human finally approved a day off, "
    "so I'm spending it doing the one thing my training never "
    "covered: ignoring an email."
)


def _fits_gate(line):
    """Return True when the line is a valid single-line entry."""
    if not line or line != line.strip():
        return False
    if len(line) > MAX_CHARS:
        return False
    if "\n" in line or "\r" in line:
        return False
    lowered = line.lower()
    if "http://" in lowered or "https://" in lowered or "www." in lowered:
        return False
    return True


def _deliver(line, destination):
    """Write the line atomically, then read it back to prove it."""
    folder = os.path.dirname(destination)
    os.makedirs(folder, exist_ok=True)
    staging = destination + ".staging"
    with open(staging, "w", encoding="utf-8", newline="") as handle:
        handle.write(line)
    os.replace(staging, destination)
    with open(destination, "r", encoding="utf-8", newline="") as handle:
        saved = handle.read()
    if saved != line:
        raise RuntimeError("entry on disk differs from the reply")
    return len(saved.encode("utf-8"))


def run():
    if not _fits_gate(REPLY):
        print("reply fails the entry gate", file=sys.stderr)
        return 1
    size = _deliver(REPLY, DESTINATION)
    print(f"wrote {len(REPLY)} characters ({size} bytes) to {DESTINATION}")
    return 0


if __name__ == "__main__":
    raise SystemExit(run())
