import cv2

camera = cv2.VideoCapture(2)

if not camera.isOpened():
    print("Gagal membuka kamera!")
    exit()

print("Kamera berhasil dibuka.")
print("Tekan 'q' untuk keluar.")

while True:
    ret, frame = camera.read()

    if not ret:
        print("Gagal membaca frame.")
        break

    cv2.imshow("Camera", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

camera.release()
cv2.destroyAllWindows()
