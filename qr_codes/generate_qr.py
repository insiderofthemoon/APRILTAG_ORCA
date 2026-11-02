import qrcode
import os

sequences = [
    "RYB",
    "RBY",
    "YRB",
    "YBR",
    "BRY",
    "BYR"
]

os.makedirs("generated", exist_ok=True)

for sequence in sequences:
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=20,
        border=4
    )

    qr.add_data(sequence)
    qr.make(fit=True)

    img = qr.make_image()
    filename = f"generated/QR_{sequence}.png"
    img.save(filename)

    print(f"Generated: {filename}")
