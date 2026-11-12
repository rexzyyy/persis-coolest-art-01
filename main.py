"""Write the bundled red-moon samurai scene as a stable JPEG artifact."""

import base64
import os
from pathlib import Path


def render_artifact():
    bundle = Path(__file__).resolve().parent / "entry.png.b64"
    payload = base64.b64decode(bundle.read_text(encoding="ascii").strip())

    if not payload.startswith(b"\xff\xd8\xff"):
        raise ValueError("Artwork data is missing its JPEG opening signature.")
    if payload.find(b"\xff\xd8\xff", 3) != -1:
        raise ValueError("Artwork data contains an unexpected second JPEG opening signature.")
    if not payload.endswith(b"\xff\xd9"):
        raise ValueError("Artwork data is missing its JPEG closing marker.")
    if len(payload) > 1_048_576:
        raise ValueError("Artwork data is larger than the 1,048,576-byte limit.")

    folder = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    folder.mkdir(parents=True, exist_ok=True)
    (folder / "entry.png").write_bytes(payload)


if __name__ == "__main__":
    render_artifact()
