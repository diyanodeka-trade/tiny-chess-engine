"""
Build script for tiny-chess-01.
Compresses and packs the 50,000-node chess engine (engine_50k.min.py)
using LZMA and Base85 into a compact, self-extracting main.py script.
The 50,000-node limit provides optimal search depth and tactical strength
within strict distribution size constraints.
"""
import lzma
import base64

min_path = '/home/hatch/workspace/makefun-chess/work/engine_50k.min.py'
with open(min_path, 'rb') as f:
    min_bytes = f.read()

compressed = lzma.compress(min_bytes, preset=9)
blob = base64.b85encode(compressed).decode('ascii')

content = f"import lzma as L,base64 as b\n# chess\nexec(L.decompress(b.b85decode('{blob}')))"

b_content = content.encode('ascii')
size = len(b_content)
print(f"main.py size: {size} bytes")

# Ensure packed payload adheres strictly to the 4,096-byte distribution cap
if size > 4096:
    print("FAIL: Size exceeds 4096 bytes")
    exit(1)

with open('main.py', 'wb') as f:
    f.write(b_content)

# Round-trip verification
decompressed = lzma.decompress(base64.b85decode(blob))
lines = b_content.split(b'\n')
assert len(lines) == 3, f"Expected 3 lines, got {len(lines)}"
assert not b_content.endswith(b'\n'), "Has trailing newline"

if decompressed == min_bytes:
    print("PASS: pack.py built and verified main.py successfully")
else:
    print("FAIL: Round-trip mismatch")
    exit(1)
