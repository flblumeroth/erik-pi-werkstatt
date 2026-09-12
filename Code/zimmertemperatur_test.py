# =====================================================
#  MICRO:BIT-TEST  -  fuer Erik (Bonus-Kapitel)
#  Liest die Temperatur, die dein micro:bit
#  durchs USB-Kabel schickt, und zeigt sie unten an.
#  Vorher: micro:bit-Programm aus dem Bonus-Kapitel
#  aufspielen und micro:bit per USB an den Pi stecken.
#  Stoppen: roter Stopp-Knopf in Thonny.
# =====================================================

import serial   # spricht mit dem USB-Kabel

verbindung = serial.Serial("/dev/ttyACM0", 115200, timeout=1)
print("Lausche auf das micro:bit...")

while True:
    zeile = verbindung.readline().decode("utf-8", "ignore").strip()
    if zeile != "":
        print("micro:bit sagt:", zeile)
