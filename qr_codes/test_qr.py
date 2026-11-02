from pyzbar.pyzbar import decode
import cv2
import glob
import os

files = sorted(glob.glob("generated/*.png"))

passed = 0

for filename in files:
    image = cv2.imread(filename)
    results = decode(image)

    expected = os.path.basename(filename)[3:6]
    detected = ""

    for result in results:
        if result.type == "QRCODE":
            detected = result.data.decode("utf-8")
            break

    print(f"{os.path.basename(filename)}")
    print(f"  Expected : {expected}")
    print(f"  Detected : {detected}")

    if detected == expected:
        print("  STATUS   : PASS")
        passed += 1
    else:
        print("  STATUS   : FAIL")

    print()

print(f"Final result: {passed}/{len(files)} QR codes decoded")
