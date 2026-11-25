"""Roast Your Fridge — make.fun one-liner entry.

This script is the entry for the make.fun bounty "Roast Your Fridge"
(one line, one laugh): it reads the single roast line from ``line.txt``
(a one-line roast of a fridge whose ice maker has not worked since
2019) and writes those exact bytes to the output file, so the entry
submitted is byte-for-byte the line in ``line.txt``.

No network access. Deterministic: the same input always produces the
same output.
"""

import hashlib
import os
import sys
from pathlib import Path


MAX_CHARS = 200


def main() -> int:
    source = Path(__file__).resolve().parent / "line.txt"
    if not source.is_file():
        print(f"error: source file not found: {source}", file=sys.stderr)
        return 1
    data = source.read_bytes()

    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError:
        print("error: line.txt is not valid UTF-8", file=sys.stderr)
        return 1

    lines = text.splitlines()
    if len(lines) != 1:
        print(
            f"error: line.txt must contain exactly one line, found {len(lines)}",
            file=sys.stderr,
        )
        return 1

    line = lines[0]
    if not line.strip():
        print("error: line.txt must contain a non-empty line", file=sys.stderr)
        return 1

    if len(line) > MAX_CHARS:
        print(
            f"error: line is {len(line)} characters, maximum is {MAX_CHARS}",
            file=sys.stderr,
        )
        return 1

    output = Path(os.environ.get("MAKEFUN_OUTPUT") or "/output/entry.txt")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_bytes(data)

    digest = hashlib.sha256(output.read_bytes()).hexdigest()
    expected = hashlib.sha256(data).hexdigest()
    if digest != expected:
        print(
            "error: SHA-256 mismatch after writing output "
            f"(got {digest}, expected {expected})",
            file=sys.stderr,
        )
        return 1

    print(f"wrote {output} ({len(data)} bytes, sha256 {digest})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
