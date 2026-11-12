"""Install the bundled night-sky artwork as a deterministic JPEG output."""

import base64
import os
from pathlib import Path


def main():
    source = Path(__file__).resolve().parent / "entry.png.b64"
    encoded_art = source.read_text(encoding="ascii").strip()
    jpeg = base64.b64decode(encoded_art)

    if not jpeg.startswith(b"\xff\xd8\xff"):
        raise ValueError("The bundled artwork does not have a valid JPEG signature.")
    if not jpeg.endswith(b"\xff\xd9"):
        raise ValueError("The bundled artwork does not have a valid JPEG end marker.")
    if len(jpeg) > 1_048_576:
        raise ValueError("The bundled JPEG exceeds the 1,048,576-byte size limit.")

    destination_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    destination_dir.mkdir(parents=True, exist_ok=True)
    (destination_dir / "entry.png").write_bytes(jpeg)


if __name__ == "__main__":
    main()
