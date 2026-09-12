# =====================================================
#  WETTERSTATION MIT MICRO:BIT  -  fuer Erik
#  Wie wetterstation.py, aber zusaetzlich zeigt sie
#  die echte Zimmertemperatur von deinem micro:bit an.
#  Alle Unterschiede sind mit "NEU" markiert.
#  Starten: in Thonny auf den gruenen Pfeil klicken.
#  Beenden: ESC-Taste druecken.
# =====================================================

import pygame     # zum Malen auf dem Bildschirm
import requests   # zum Holen von Daten aus dem Internet
import time       # fuer Uhrzeit und Warten
import serial     # NEU: spricht mit dem USB-Kabel zum micro:bit

# ---------- Einstellungen ----------------------------
STADT = "Schwieberdingen"
BREITENGRAD = 48.88
LAENGENGRAD = 9.07
NEU_LADEN_ALLE = 10 * 60      # alle 10 Minuten neues Wetter holen (in Sekunden)

URL = ("https://api.open-meteo.com/v1/forecast"
       "?latitude=" + str(BREITENGRAD) +
       "&longitude=" + str(LAENGENGRAD) +
       "&current=temperature_2m,weather_code,wind_speed_10m"
       "&daily=temperature_2m_max,temperature_2m_min"
       "&timezone=auto")

# ---------- Farben (Rot, Gruen, Blau: je 0 bis 255) --
HIMMEL   = (25, 70, 130)
WEISS    = (255, 255, 255)
GELB     = (255, 210, 0)
HELLGRAU = (225, 225, 235)
GRAU     = (150, 150, 165)
BLAU     = (120, 180, 255)


def wetter_holen():
    """Fragt den Wetterdienst im Internet und packt die Antwort aus."""
    antwort = requests.get(URL, timeout=10)
    daten = antwort.json()
    return {
        "temperatur": daten["current"]["temperature_2m"],
        "wind":       daten["current"]["wind_speed_10m"],
        "code":       daten["current"]["weather_code"],
        "max":        daten["daily"]["temperature_2m_max"][0],
        "min":        daten["daily"]["temperature_2m_min"][0],
    }


def wetter_wort(code):
    """Macht aus der Wetter-Nummer ein Wort."""
    if code == 0:
        return "Sonnig"
    if code <= 2:
        return "Leicht bewoelkt"
    if code == 3:
        return "Bewoelkt"
    if code <= 48:
        return "Nebel"
    if code <= 67 or (80 <= code <= 82):
        return "Regen"
    if code <= 77 or code in (85, 86):
        return "Schnee"
    return "Gewitter"


# ---------- Wetter-Symbole zum Malen -----------------

def sonne_malen(bildschirm, x, y):
    """Malt eine Sonne: ein Kreis mit 8 Strahlen."""
    strahlen = [(0, -1), (0, 1), (-1, 0), (1, 0),
                (-0.7, -0.7), (0.7, -0.7), (-0.7, 0.7), (0.7, 0.7)]
    for (dx, dy) in strahlen:
        start = (x + dx * 45, y + dy * 45)
        ende = (x + dx * 62, y + dy * 62)
        pygame.draw.line(bildschirm, GELB, start, ende, 6)
    pygame.draw.circle(bildschirm, GELB, (x, y), 38)


def wolke_malen(bildschirm, x, y, farbe):
    """Malt eine Wolke aus drei Kreisen und einem Rechteck."""
    pygame.draw.circle(bildschirm, farbe, (x - 30, y), 24)
    pygame.draw.circle(bildschirm, farbe, (x + 5, y - 16), 30)
    pygame.draw.circle(bildschirm, farbe, (x + 34, y), 22)
    pygame.draw.rect(bildschirm, farbe, (x - 30, y - 2, 64, 26))


def regen_malen(bildschirm, x, y):
    wolke_malen(bildschirm, x, y, HELLGRAU)
    for dx in (-24, 0, 24):
        pygame.draw.line(bildschirm, BLAU,
                         (x + dx, y + 30), (x + dx - 8, y + 52), 5)


def schnee_malen(bildschirm, x, y):
    wolke_malen(bildschirm, x, y, HELLGRAU)
    for dx in (-24, 0, 24):
        pygame.draw.circle(bildschirm, WEISS, (x + dx, y + 42), 6)


def blitz_malen(bildschirm, x, y):
    wolke_malen(bildschirm, x, y, GRAU)
    punkte = [(x + 6, y + 26), (x - 10, y + 54), (x, y + 54),
              (x - 8, y + 82), (x + 16, y + 48), (x + 5, y + 48),
              (x + 14, y + 26)]
    pygame.draw.polygon(bildschirm, GELB, punkte)


def symbol_malen(bildschirm, code, x, y):
    """Sucht das passende Symbol zur Wetter-Nummer aus."""
    if code == 0:
        sonne_malen(bildschirm, x, y)
    elif code <= 3:
        sonne_malen(bildschirm, x - 20, y - 20)
        wolke_malen(bildschirm, x + 10, y + 15, WEISS)
    elif code <= 48:
        wolke_malen(bildschirm, x, y, GRAU)
    elif code <= 67 or (80 <= code <= 82):
        regen_malen(bildschirm, x, y)
    elif code <= 77 or code in (85, 86):
        schnee_malen(bildschirm, x, y)
    else:
        blitz_malen(bildschirm, x, y)


# ---------- Los geht's! ------------------------------
pygame.init()
bildschirm = pygame.display.set_mode((480, 320))
# Tipp: Auf dem kleinen Display sieht es ohne Fensterrahmen besser aus.
# Dazu die Zeile oben loeschen und diese hier benutzen:
# bildschirm = pygame.display.set_mode((480, 320), pygame.FULLSCREEN)
pygame.display.set_caption("Wetterstation mit micro:bit")
pygame.mouse.set_visible(False)

schrift_riesig = pygame.font.SysFont(None, 120)
schrift_gross = pygame.font.SysFont(None, 44)
schrift_klein = pygame.font.SysFont(None, 30)

# NEU: Verbindung zum micro:bit oeffnen (wenn eins da ist)
try:
    microbit = serial.Serial("/dev/ttyACM0", 115200, timeout=1)
except Exception:
    microbit = None       # kein micro:bit angesteckt? Macht nichts!
zimmer_temp = None        # zuletzt empfangene Zimmertemperatur

wetter = None          # hier merken wir uns das Wetter
zuletzt_geholt = 0     # wann haben wir zuletzt gefragt?

laeuft = True
while laeuft:

    # 1) Tasten und Beruehrungen pruefen
    for ereignis in pygame.event.get():
        if ereignis.type == pygame.QUIT:
            laeuft = False
        if ereignis.type == pygame.KEYDOWN and ereignis.key == pygame.K_ESCAPE:
            laeuft = False
        if ereignis.type == pygame.MOUSEBUTTONDOWN:
            zuletzt_geholt = 0    # Tippen = sofort neues Wetter holen

    # 2) Ab und zu neues Wetter aus dem Internet holen
    if time.time() - zuletzt_geholt > NEU_LADEN_ALLE:
        try:
            wetter = wetter_holen()
        except Exception:
            pass                  # kein Internet? Dann alte Daten behalten.
        zuletzt_geholt = time.time()

    # 2b) NEU: Nachschauen, ob das micro:bit etwas geschickt hat
    if microbit is not None and microbit.in_waiting > 0:
        zeile = microbit.readline().decode("utf-8", "ignore").strip()
        if zeile.startswith("zimmer:"):
            zimmer_temp = float(zeile.split(":")[1])

    # 3) Alles malen
    bildschirm.fill(HIMMEL)

    if wetter is None:
        text = schrift_gross.render("Hole das Wetter...", True, WEISS)
        bildschirm.blit(text, (110, 140))
    else:
        # Stadt und Uhrzeit oben
        stadt_text = schrift_klein.render(STADT, True, WEISS)
        bildschirm.blit(stadt_text, (20, 15))
        uhr_text = schrift_klein.render(time.strftime("%H:%M"), True, WEISS)
        bildschirm.blit(uhr_text, (410, 15))

        # NEU: Zimmertemperatur vom micro:bit (in Gelb, unter dem Stadtnamen)
        if zimmer_temp is not None:
            zimmer_text = schrift_klein.render(
                "Zimmer: " + str(round(zimmer_temp)) + "\u00b0", True, GELB)
            bildschirm.blit(zimmer_text, (20, 45))

        # Temperatur gross links
        grad = str(round(wetter["temperatur"])) + "\u00b0"
        grad_text = schrift_riesig.render(grad, True, WEISS)
        bildschirm.blit(grad_text, (30, 90))

        # Wetter-Symbol rechts
        symbol_malen(bildschirm, wetter["code"], 360, 130)

        # Wetter-Wort darunter
        wort_text = schrift_gross.render(wetter_wort(wetter["code"]), True, WEISS)
        bildschirm.blit(wort_text, (30, 200))

        # Unten: hoechste und tiefste Temperatur + Wind
        unten = ("Heute: " + str(round(wetter["min"])) + "\u00b0 bis "
                 + str(round(wetter["max"])) + "\u00b0   |   Wind: "
                 + str(round(wetter["wind"])) + " km/h")
        unten_text = schrift_klein.render(unten, True, HELLGRAU)
        bildschirm.blit(unten_text, (30, 270))

    pygame.display.flip()
    pygame.time.wait(200)   # kurz warten, damit der Pi nicht schwitzt

pygame.quit()
