#!/usr/bin/env python3
import sys, lzma, base64

def main():
    min_path = 'src/engine_golf100k.min.py'
    sys.argv = ['minify.py', 'src/engine_golf100k.py', min_path]
    import src.minify

    with open(min_path, 'rb') as f:
        orig = f.read()

    comp = lzma.compress(orig, preset=9)
    blob = base64.b85encode(comp).decode('ascii')

    with open('main.py', 'r', encoding='ascii') as f:
        tmpl = f.read()

    code = tmpl.replace('__BLOB__', blob)
    size = len(code.encode('ascii'))
    print(f"Generated main.py size: {size} bytes (limit 4096)")

    with open('main.py', 'w', encoding='ascii', newline='') as f:
        f.write(code)

    decomp = lzma.decompress(base64.b85decode(blob))
    assert decomp == orig, "Round-trip verification failed!"
    
    if size < 4096 and decomp == orig:
        print("PASS: Size < 4096 and round-trip verification successful.")
    else:
        print("FAIL: Size or verification failed.")

if __name__ == '__main__':
    main()
