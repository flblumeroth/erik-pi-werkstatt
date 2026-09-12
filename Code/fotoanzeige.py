# =====================================================
#  FOTO-RAHMEN  -  fuer Erik
#  Zeigt deine Kamera-Fotos auf dem Display an.
#  Rechts tippen  = naechstes Foto
#  Links tippen   = ein Foto zurueck
#  Beenden: ESC-Taste druecken.
# =====================================================

import pygame
import os
import time

# ---------- Einstellungen ----------------------------
FOTO_ORDNER = "/home/erik/Fotos"   # in diesem Ordner liegen die Fotos
WECHSEL_NACH = 10                  # Sekunden bis zum naechsten Foto

pygame.init()
bildschirm = pygame.display.set_mode((480, 320))
# Tipp: Auf dem kleinen Display sieht es ohne Fensterrahmen besser aus.
# Dazu die Zeile oben loeschen und diese hier benutzen:
# bildschirm = pygame.display.set_mode((480, 320), pygame.FULLSCREEN)
pygame.display.set_caption("Foto-Rahmen")
pygame.mouse.set_visible(False)
schrift = pygame.font.SysFont(None, 36)


def fotos_finden():
    """Sammelt alle Bilddateien aus dem Foto-Ordner."""
    liste = []
    for name in sorted(os.listdir(FOTO_ORDNER)):
        if name.lower().endswith((".jpg", ".jpeg", ".png")):
            liste.append(FOTO_ORDNER + "/" + name)
    return liste


def foto_laden(pfad):
    """Laedt ein Foto und macht es passend fuer den Bildschirm."""
    bild = pygame.image.load(pfad)
    bild = bild.convert()          # macht das Anzeigen schneller
    breite = bild.get_width()
    hoehe = bild.get_height()
    # so gross wie moeglich, ohne das Foto zu verzerren:
    faktor = min(480 / breite, 320 / hoehe)
    neue_breite = int(breite * faktor)
    neue_hoehe = int(hoehe * faktor)
    return pygame.transform.smoothscale(bild, (neue_breite, neue_hoehe))


try:
    fotos = fotos_finden()
except FileNotFoundError:
    fotos = []                     # den Ordner gibt es noch gar nicht

nummer = 0
aktuelles_foto = None
zuletzt_gewechselt = time.time()

if len(fotos) > 0:
    aktuelles_foto = foto_laden(fotos[nummer])

laeuft = True
while laeuft:

    neues_foto = False

    # 1) Tasten und Beruehrungen pruefen
    for ereignis in pygame.event.get():
        if ereignis.type == pygame.QUIT:
            laeuft = False
        if ereignis.type == pygame.KEYDOWN and ereignis.key == pygame.K_ESCAPE:
            laeuft = False
        if ereignis.type == pygame.MOUSEBUTTONDOWN and len(fotos) > 0:
            x = ereignis.pos[0]
            if x > 240:
                nummer = nummer + 1    # rechte Haelfte: vor
            else:
                nummer = nummer - 1    # linke Haelfte: zurueck
            neues_foto = True

    # 2) Nach ein paar Sekunden automatisch weiterblaettern
    if len(fotos) > 0 and time.time() - zuletzt_gewechselt > WECHSEL_NACH:
        nummer = nummer + 1
        neues_foto = True

    # 3) Wenn noetig, das naechste Foto laden
    if neues_foto:
        nummer = nummer % len(fotos)   # nach dem letzten Foto wieder von vorn
        aktuelles_foto = foto_laden(fotos[nummer])
        zuletzt_gewechselt = time.time()

    # 4) Malen
    bildschirm.fill((0, 0, 0))         # schwarzer Hintergrund
    if aktuelles_foto is None:
        text = schrift.render("Keine Fotos im Ordner gefunden!", True,
                              (255, 255, 255))
        bildschirm.blit(text, (60, 145))
    else:
        # Foto genau in die Mitte setzen
        x = (480 - aktuelles_foto.get_width()) // 2
        y = (320 - aktuelles_foto.get_height()) // 2
        bildschirm.blit(aktuelles_foto, (x, y))

    pygame.display.flip()
    pygame.time.wait(50)

pygame.quit()
