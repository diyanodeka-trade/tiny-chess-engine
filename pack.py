#!/usr/bin/env python3
"""Build script for tiny-chess-01 entry (main.py).

Minifies src/engine_golf100k.py using src/minify.py, compresses with LZMA
(preset=9), base85-encodes the result, and writes main.py as a self-extracting
one-liner under 4,096 bytes with built-in round-trip verification and size check.
"""
import sys
import lzma
import base64

def main():
    # 1. Minify src/engine_golf100k.py using src/minify.py logic
    min_path = 'engine_golf100k.min.py'
    sys.argv = ['minify.py', 'src/engine_golf100k.py', min_path]
    import src.minify

    with open(min_path, 'rb') as f:
        original_data = f.read()

    # 2. Compress with LZMA preset 9
    compressed = lzma.compress(original_data, preset=9)

    # 3. Base85 encode (avoid f-strings to prevent brace collision in base85 data)
    blob = base64.b85encode(compressed).decode('ascii')
    main_code = "import lzma as L,base64 as b;exec(L.decompress(b.b85decode('" + blob + "')))"

    # 4. Size check (< 4,096 bytes)
    size = len(main_code)
    print(f"Generated main.py size: {size} bytes (limit 4096)")
    assert size < 4096, f"Error: main.py size {size} exceeds 4,096 bytes limit!"

    # 5. Write main.py without trailing newline
    with open('main.py', 'wb') as f:
        f.write(main_code.encode('ascii'))

    # 6. Round-trip verification
    decompressed = lzma.decompress(base64.b85decode(blob))
    assert decompressed == original_data, "Round-trip verification failed: decompressed data mismatch!"
    print("Verification PASSED: Round-trip successful and byte-identical to minified source.")

if __name__ == '__main__':
    main()
