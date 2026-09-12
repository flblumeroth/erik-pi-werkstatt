# Eriks Raspberry-Pi-Werkstatt 🍓

Zwei Projekte (und ein Bonus) für den Raspberry Pi mit 3,5"-Touch-Display — gemacht für den Umstieg von MakeCode-Blöcken auf einfaches Python:

| Projekt | Was es kann | Programm |
|---|---|---|
| ⛅ **Wetterstation** | Holt das echte Wetter aus dem Internet und malt eigene Wettersymbole | [`code/wetterstation.py`](code/wetterstation.py) |
| 📷 **Foto-Rahmen** | Zeigt deine Kamera-Fotos, blättern per Touch, Diashow | [`code/fotoanzeige.py`](code/fotoanzeige.py) |
| 🌡️ **Bonus: micro:bit-Sensor** | Dein micro:bit (MakeCode!) misst die Zimmertemperatur und schickt sie an die Wetterstation | [`code/wetterstation_mit_microbit.py`](code/wetterstation_mit_microbit.py) |
| 🕒 **Wanduhr** | Große Uhr mit Datum und Sekundenbalken — [Projekt zum Selbst-Knobeln](https://flblumeroth.github.io/erik-pi-werkstatt/projekt-uhr.html) | [`code/wanduhr.py`](code/wanduhr.py) |

## 👉 Hier geht's los

**Für Erik im Browser:** [flblumeroth.github.io/erik-pi-werkstatt](https://flblumeroth.github.io/erik-pi-werkstatt/) — die `index.html` zeigt das komplette Tutorial als bunte Seite mit Kapitel-Haken zum Abhaken und Kopier-Knöpfen an jedem Code-Block. (Einmalig im Repo aktivieren: *Settings → Pages → Deploy from a branch → `main`, Ordner `/ (root)`*.)

Dieselben Inhalte als Text: [TUTORIAL.md](TUTORIAL.md). Das Tutorial hat zwei Teile: **Teil 0** ist die einmalige Einrichtung für Erwachsene (Display-Treiber, Bibliotheken, Foto-Ordner). Ab **„Hallo Erik!"** geht es Schritt für Schritt zum Selbermachen — vom ersten `print` bis zum fertigen Projekt.

## Schnellstart auf dem Pi

```bash
git clone https://github.com/flblumeroth/erik-pi-werkstatt.git
sudo apt install -y python3-pygame python3-requests python3-serial
```

Danach eine Datei aus `code/` in **Thonny** öffnen und auf den grünen Pfeil klicken. Die Einrichtung des 3,5"-Displays steht in [TUTORIAL.md, Teil 0](TUTORIAL.md).

## Was du brauchst

Raspberry Pi (3B+, 4 oder 5) · 3,5"-Touch-Display (BerryBase RPI-35LCD, 480x320) · microSD-Karte · WLAN · eigene Fotos im Ordner `/home/erik/Fotos` · für den Bonus: ein micro:bit mit USB-Datenkabel

---

*Gebaut für Erik zum Geburtstag. 🎁 Erst selbst tippen, dann mit den Musterlösungen in `code/` vergleichen!*
