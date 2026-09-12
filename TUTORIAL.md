# Eriks Raspberry-Pi-Werkstatt 🍓
## Projekt A: Wetterstation · Projekt B: Foto-Rahmen

---

## Teil 0 — Für Papa (bitte zuerst lesen)

**Warum Python und nicht MakeCode?** MakeCode läuft im Browser und programmiert kleine Chips wie den micro:bit — auf dem Raspberry Pi selbst gibt es kein MakeCode. Der Pi ist ein richtiger Computer, und dort ist Python die natürliche Kindersprache. Damit der Umstieg leichtfällt, zeigt jedes Kapitel zuerst, *welcher MakeCode-Block* gemeint wäre, und dann die Python-Zeile dazu. Erik tippt in **Thonny** (ist auf Raspberry Pi OS vorinstalliert) — kurze Programme, jedes sofort startbar. Der MakeCode-Editor selbst läuft übrigens trotzdem im Chromium-Browser des Pi — im **Bonus-Kapitel** verbinden wir beide Welten: ein micro:bit als echter Zimmersensor für die Wetterstation.

**Das brauchst du an Hardware:** Raspberry Pi (3B+, 4 oder 5), das 3,5"-Touch-Shield, microSD-Karte (ab 16 GB), Netzteil, für die Einrichtung einmalig einen HDMI-Monitor mit Maus/Tastatur, und einen SD-Kartenleser, um Fotos von Eriks Kamera zu übertragen. Für das Bonus-Kapitel zusätzlich: ein micro:bit samt USB-Datenkabel.

### Einmalige Einrichtung (ca. 45 Minuten)

1. **System aufspielen:** Raspberry Pi Imager → „Raspberry Pi OS (64-bit)" mit Desktop. In den Einstellungen (Zahnrad) Benutzername `erik`, WLAN und Sprache gleich eintragen. *Hinweis: Wenn du einen anderen Benutzernamen wählst, musst du in den beiden Programmen den Pfad `/home/erik/...` anpassen.*
2. **Erster Start ohne Display-Aufsatz**, dafür mit HDMI-Monitor. (Das SPI-Shield zeigt vor der Konfiguration nur ein weißes Bild — das ist normal, nichts ist kaputt.)
3. **Display aktivieren — es ist das BerryBase RPI-35LCD:** Das ist ein Waveshare-Klon (Display-Controller ILI9486, Touch-Controller XPT2046). Die gute Nachricht: Der passende Treiber („piscreen") steckt bereits im aktuellen Raspberry Pi OS — es muss **nichts installiert** werden, nur eine Zeile in die Konfiguration. Am Pi im Terminal `sudo nano /boot/firmware/config.txt` öffnen und ganz unten ergänzen:
   ```
   dtoverlay=piscreen,speed=16000000,rotate=270,driver=ili9486,bgr=1
   ```
   Speichern (Strg+O, Enter, Strg+X), herunterfahren, Display aufstecken, neu starten — der Desktop erscheint auf dem kleinen Display. Ist das Bild falsch herum, den Wert bei `rotate=` ändern (0/90/180/270).
4. **Falls der Desktop nicht auf dem LCD erscheint:** `sudo raspi-config` → *Advanced Options* → *Wayland* → **X11** wählen und neu starten — manche Setups brauchen das noch. ⚠️ **Nicht** die alten Installations-Skripte aus der verlinkten Waveshare-Anleitung bzw. „LCD-show" ausführen: Auf neueren Pis (4/5) und aktuellem OS können die das System unbrauchbar machen. Die eine config.txt-Zeile ersetzt sie komplett.
5. **Touch prüfen:** Sind bei diesem Display die Achsen vertauscht (man tippt rechts unten, der Klick landet links oben — bekanntes Verhalten bei diesen Panels), an die dtoverlay-Zeile `,swapxy=1` anhängen; feinjustieren geht mit `,invx=1` bzw. `,invy=1`. Nach jeder Änderung neu starten.
6. **Bibliotheken installieren** (im Terminal):
   ```bash
   sudo apt install -y python3-pygame python3-requests python3-serial
   ```
7. **Foto-Ordner anlegen:** Ordner `/home/erik/Fotos` erstellen und ein paar Fotos von Eriks Kamera-SD-Karte hineinkopieren (JPG oder PNG).
8. **Programme aufs Pi holen** (im Terminal): `git clone https://github.com/flblumeroth/erik-pi-werkstatt.git` — danach liegen dieses Tutorial und alle fertigen Programme unter `/home/erik/erik-pi-werkstatt/`, die Musterlösungen im Unterordner `code/`. Die Wetter-Koordinaten sind schon auf Schwieberdingen eingestellt.

**Plan B, falls es gar nicht will:** Mit dem Image „Raspberry Pi OS (Legacy)" (Bullseye) und der Waveshare-/LCD-show-Anleitung laufen diese Displays klassisch — das ist aber wirklich nur die Notlösung. Und: Entwickeln geht jederzeit auch am HDMI-Monitor — das kleine Display ist nur die Bühne für das fertige Projekt.

**Optional — Autostart des Foto-Rahmens:** Wenn alles läuft, trägst du in die Datei `/etc/xdg/lxsession/LXDE-pi/autostart` diese Zeile ein: `@python3 /home/erik/erik-pi-werkstatt/code/fotoanzeige.py` — dann startet der Bilderrahmen beim Einschalten von selbst.

---

# 👋 Hallo Erik!

Du kennst schon MakeCode-Blöcke — super! Auf deinem Raspberry Pi schreibst du dieselben Ideen jetzt als **Text**. Das ist wie Blöcke tippen statt ziehen. Alle fertigen Programme aus diesem Tutorial findest du im Ordner `code/` — erst selbst probieren, dann vergleichen! Hier ist dein Spickzettel:

| In MakeCode (Block) | In Python (Text) |
|---|---|
| „zeige Text *Hallo*" | `print("Hallo")` |
| „setze *zahl* auf 5" | `zahl = 5` |
| „wenn … dann" | `if zahl > 3:` |
| „dauerhaft / wiederhole endlos" | `while True:` |
| „pausiere 1000 ms" | `time.sleep(1)` |

**Drei Regeln, die Python streng nimmt:**

1. Nach `if`, `while` und `def` kommt ein **Doppelpunkt `:`**
2. Alles, was „im Block drinsteckt", wird **eingerückt** (4 Leerzeichen — Thonny macht das automatisch)
3. Text steht immer in **Anführungszeichen** `"so"`

Wenn etwas nicht klappt: **Fehlermeldungen sind Hinweise, keine Strafe!** Lies die letzte Zeile — dort steht meistens die Zeilennummer, in der Python gestolpert ist.

---

## Kapitel 1 — Dein erstes Python-Programm (5 Minuten)

Öffne **Thonny** (Himbeere-Menü → Entwicklung → Thonny). Tippe oben ins große Feld:

```python
name = "Erik"
print("Hallo " + name + "!")
print("Du programmierst jetzt einen echten Computer.")
```

Klicke auf den **grünen Pfeil** (oder F5), speichere als `hallo.py`. Unten erscheint deine Ausgabe. Das war dein erstes echtes Python-Programm! 🎉

---

## Kapitel 2 — Malen auf dem Bildschirm (10 Minuten)

Für Bilder benutzen wir **pygame**. Stell dir den Bildschirm als Blatt Kästchenpapier vor: **480 Kästchen breit, 320 hoch**. Oben links ist (0, 0), unten rechts (480, 320).

Neue Datei, speichere sie als `malen.py`:

```python
import pygame

pygame.init()
bildschirm = pygame.display.set_mode((480, 320))

bildschirm.fill((25, 70, 130))                              # Himmel
pygame.draw.circle(bildschirm, (255, 210, 0), (240, 120), 50)  # Sonne
pygame.display.flip()                                       # zeig alles an!

# Warten, bis du das Fenster schliesst oder ESC drueckst
laeuft = True
while laeuft:
    for ereignis in pygame.event.get():
        if ereignis.type == pygame.QUIT:
            laeuft = False
        if ereignis.type == pygame.KEYDOWN and ereignis.key == pygame.K_ESCAPE:
            laeuft = False

pygame.quit()
```

Die drei Zahlen bei den Farben sind **Rot, Grün, Blau** (je 0 bis 255). Probier aus:

* Ändere die Farbe der Sonne
* Verschieb die Sonne: `(240, 120)` sind ihre x- und y-Position
* Mal ein Rechteck als Wiese dazu: `pygame.draw.rect(bildschirm, (60, 160, 60), (0, 260, 480, 60))`

---

## Kapitel 3 — Projekt A: Die Wetterstation ⛅

### Schritt 1: Das Wetter aus dem Internet holen

Im Internet gibt es Wetter-Auskünfte für Computer, sogenannte **APIs**. Wir fragen „Open-Meteo" — die antwortet mit Zahlen für deinen Ort. Neue Datei `wetter_test.py`:

```python
import requests

url = ("https://api.open-meteo.com/v1/forecast"
       "?latitude=48.88&longitude=9.07"
       "&current=temperature_2m,weather_code,wind_speed_10m")

antwort = requests.get(url)
daten = antwort.json()

print(daten["current"]["temperature_2m"], "Grad")
print("Wind:", daten["current"]["wind_speed_10m"], "km/h")
```

Starte es — du siehst die **echte Temperatur in Schwieberdingen, genau jetzt**. Die Antwort ist wie ein Schrank mit Schubladen: `daten["current"]["temperature_2m"]` heißt „öffne die Schublade *current*, darin die Schublade *temperature_2m*".

Es gibt auch eine Schublade `weather_code` — eine Nummer für das Wetter: **0 = sonnig, 3 = bewölkt, 61 = Regen, 71 = Schnee, 95 = Gewitter.** Lass sie dir mit `print` ausgeben!

### Schritt 2: Groß und schön anzeigen

Jetzt kombinieren wir Kapitel 2 und Schritt 1: Wetter holen **und** mit pygame malen. Dafür brauchst du Schrift:

```python
schrift = pygame.font.SysFont(None, 120)          # 120 = riesig
text = schrift.render("21" + "\u00b0", True, (255, 255, 255))
bildschirm.blit(text, (30, 90))                   # an Position x=30, y=90 kleben
```

`render` malt den Text auf einen unsichtbaren Zettel, `blit` klebt den Zettel auf den Bildschirm.

### Schritt 3: Wettersymbole selbst malen

Statt fertiger Bildchen malen wir die Symbole aus Formen — wie in Kapitel 2:

* **Sonne** = Kreis + 8 Striche als Strahlen
* **Wolke** = drei Kreise + ein Rechteck darunter
* **Regen** = Wolke + drei schräge blaue Striche
* **Gewitter** = Wolke + gelbes Zickzack (`pygame.draw.polygon`)

Und mit `if` entscheidet dein Programm, welches Symbol dran ist:

```python
if code == 0:
    sonne_malen(bildschirm, 360, 130)
elif code <= 3:
    wolke_malen(bildschirm, 360, 130)
```

### Schritt 4: Alles zusammen

Die fertige Wetterstation steht in der Datei **`wetterstation.py`** — öffne sie in Thonny und starte sie. Sie holt alle 10 Minuten neues Wetter, und wenn du auf den Bildschirm **tippst**, sofort. Lies sie einmal von oben nach unten durch: Du wirst fast alles wiedererkennen. Ändere etwas! Zum Beispiel die Hintergrundfarbe, oder bei `NEU_LADEN_ALLE` die 10 Minuten.

---

## Kapitel 4 — Projekt B: Dein Foto-Rahmen 📷

### Schritt 1: Ein Foto anzeigen

Deine Kamerafotos liegen im Ordner `/home/erik/Fotos`. Neue Datei `foto_test.py`:

```python
import pygame

pygame.init()
bildschirm = pygame.display.set_mode((480, 320))

bild = pygame.image.load("/home/erik/Fotos/mein_foto.jpg")   # Namen anpassen!
bild = pygame.transform.smoothscale(bild, (480, 320))        # passend machen
bildschirm.blit(bild, (0, 0))
pygame.display.flip()

laeuft = True
while laeuft:
    for ereignis in pygame.event.get():
        if ereignis.type == pygame.QUIT:
            laeuft = False

pygame.quit()
```

Fällt dir was auf? Das Foto sieht vielleicht **gequetscht** aus, weil Kamerafotos ein anderes Format haben als der Bildschirm. Im fertigen Programm rechnen wir deshalb aus, wie groß das Foto sein darf, **ohne** verzerrt zu werden:

```python
faktor = min(480 / breite, 320 / hoehe)
```

`min` nimmt die kleinere der beiden Zahlen — so passt das Foto garantiert komplett aufs Display.

### Schritt 2: Blättern und Diashow

Das fertige Programm steht in **`fotoanzeige.py`**. Es kann:

* alle Fotos aus dem Ordner finden (`os.listdir`)
* rechts tippen → nächstes Foto, links tippen → zurück
* nach 10 Sekunden automatisch weiterblättern
* nach dem letzten Foto wieder von vorn anfangen — der Trick dafür ist `nummer % len(fotos)` (der Rest beim Teilen: nach Foto 7 von 7 kommt wieder Foto 0)

Starte es, tippe dich durch deine Fotos — und dann bau es um: Ändere `WECHSEL_NACH` auf 3 Sekunden. Schaffst du es, dass beim Tippen **oben** am Bildschirm das Programm zur Wetterstation wechselt? (Tipp: `ereignis.pos[1]` ist die y-Position deines Fingers.)

---

## Bonus-Kapitel — Dein micro:bit wird Wettersensor 🌡️

Jetzt verbindest du deine MakeCode-Blöcke mit deinem neuen Python: Das micro:bit misst die **echte Temperatur in deinem Zimmer** und schickt sie durchs USB-Kabel an den Pi — und deine Wetterstation zeigt sie an. Blöcke fürs Messen, Python fürs Anzeigen!

### Schritt 1: Das micro:bit programmieren (in MakeCode!)

Öffne auf dem Pi den Browser (Chromium) und gehe wie gewohnt auf makecode.microbit.org. Baue dieses Mini-Programm:

* Block **„dauerhaft"**
* Hinein den Block **„schreibe seriell Wert"** (versteckt unter *Fortgeschritten → Serielle Kommunikation*): Als Namen `zimmer` eintippen, als Wert den Block **„Temperatur (°C)"** aus *Eingabe* einsetzen
* Darunter **„pausiere (ms) 5000"**

In JavaScript sieht dasselbe so aus:

```javascript
basic.forever(function () {
    serial.writeValue("zimmer", input.temperature())
    basic.pause(5000)
})
```

Übertrage es aufs micro:bit — das geht direkt vom Pi aus — und lass das micro:bit danach per USB am Pi eingesteckt. Es schickt jetzt alle 5 Sekunden eine Nachricht wie `zimmer:23` durchs Kabel.

### Schritt 2: Auf dem Pi lauschen

Starte in Thonny das Programm **`zimmertemperatur_test.py`**. Unten sollte erscheinen:

```
micro:bit sagt: zimmer:23
```

Halte einen Finger auf den Prozessor des micro:bit — die Zahl steigt! (Das micro:bit misst nämlich die Temperatur seines eigenen Chips.)

Der neue Baustein heißt `serial` — er liest, was durchs USB-Kabel ankommt. Das Kabel meldet sich am Pi unter dem Namen `/dev/ttyACM0`. Kommt eine Fehlermeldung mit „Permission denied", muss Papa einmal `sudo usermod -a -G dialout erik` ausführen und du meldest dich neu an.

### Schritt 3: In die Wetterstation einbauen

Die fertige Kombi-Version heißt **`wetterstation_mit_microbit.py`**. Sie ist fast identisch mit deiner Wetterstation — vergleiche die beiden Dateien und finde die Unterschiede! Es sind nur drei Stellen (alle mit `NEU` markiert):

1. Oben: `import serial` und die Verbindung zum micro:bit öffnen
2. In der Schleife: nachschauen, ob eine neue `zimmer:`-Nachricht angekommen ist
3. Beim Malen: die Zimmertemperatur in Gelb unter den Stadtnamen schreiben

Das Beste: Ist gerade **kein** micro:bit angesteckt, läuft die Wetterstation trotzdem ganz normal — dafür sorgt das `try:` beim Verbinden („versuch es, und wenn's nicht klappt, mach einfach ohne weiter").

---

## Ideen zum Weiterbauen 💡

Wenn beide Projekte laufen, bist du offiziell Raspberry-Pi-Programmierer. Nächste Stufen:

1. **Uhr im Foto-Rahmen:** Uhrzeit klein in die Ecke der Fotos schreiben (`time.strftime("%H:%M")`)
2. **Oma-Wetter:** Zweite Stadt anzeigen — einfach andere Koordinaten in die URL
3. **Zufalls-Diashow:** `import random` und `random.shuffle(fotos)`
4. **Vorhersage:** Open-Meteo kann auch die nächsten Tage — Schubladen `daily`
5. **Noch mehr Sensoren:** Dein micro:bit misst schon die Zimmertemperatur (Bonus-Kapitel) — ein BME280-Sensor kann zusätzlich Luftdruck und Luftfeuchtigkeit messen, dann ist es eine komplette Wetterstation (Projekt für den nächsten Geburtstag 😉)

---

## Wenn etwas nicht klappt 🔧

| Problem | Wahrscheinliche Ursache |
|---|---|
| `SyntaxError` | Doppelpunkt vergessen oder Anführungszeichen nicht geschlossen |
| `IndentationError` | Einrückung stimmt nicht — alles im Block gleich weit einrücken |
| `NameError` | Tippfehler in einem Namen (`bildscrm` statt `bildschirm`) |
| Programm friert ein / Wetter kommt nicht | Kein Internet — WLAN prüfen |
| „Keine Fotos gefunden" | Ordnername prüfen: genau `/home/erik/Fotos`, Fotos als JPG/PNG |
| Display bleibt weiß/schwarz | config.txt-Zeile fehlt oder Tippfehler darin → Papa fragen (Teil 0) |
| Tippen landet an der falschen Stelle | Touch-Achsen vertauscht → `swapxy=1` (Teil 0, Schritt 5) |
| micro:bit wird nicht gefunden | USB-Kabel prüfen (manche Kabel können nur laden, keine Daten!), micro:bit neu einstecken, bei „Permission denied" → Papa fragen (Bonus-Kapitel) |

Viel Spaß beim Bauen! 🚀
