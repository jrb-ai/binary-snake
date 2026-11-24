"""Turn snake.bits into the executable `snake`.

This is a bit loader, not an assembler: it knows no instructions or
labels. It drops comments, turns each group of 8 binary digits into a
byte, honours '@XXXX' zero padding, then ad-hoc signs the file, which
macOS on Apple Silicon requires before it will run any executable.
"""

from __future__ import annotations

import subprocess
from pathlib import Path


def load_bits(source: Path | str) -> bytes:
    """Return the bytes described by a commented binary-digit file."""
    out = bytearray()
    for number, line in enumerate(Path(source).read_text().splitlines(), 1):
        text = line.split(";", 1)[0].strip()
        if text.startswith("@"):
            target = int(text[1:], 16)
            if target < len(out):
                raise ValueError(f"line {number}: @{text[1:]} is behind offset {len(out):#x}")
            out.extend(bytes(target - len(out)))
            continue
        for group in text.split():
            if len(group) != 8 or set(group) - {"0", "1"}:
                raise ValueError(f"line {number}: {group!r} is not 8 binary digits")
            out.append(int(group, 2))
    return bytes(out)


def build(source: Path | str, target: Path | str) -> None:
    """Write and sign the executable."""
    target = Path(target)
    target.write_bytes(load_bits(source))
    target.chmod(0o755)
    subprocess.run(["codesign", "-s", "-", "-f", str(target)], check=True)


if __name__ == "__main__":
    here = Path(__file__).parent
    build(here / "snake.bits", here / "snake")
