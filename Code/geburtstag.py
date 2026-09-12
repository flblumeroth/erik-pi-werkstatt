# =====================================================
#  GEBURTSTAGS-GRUSS  -  die allererste Anzeige!
#  Zeigt "Hallo Erik, herzlichen Glueckwunsch zum
#  Geburtstag" mit Konfetti auf dem Display.
#  Tippen auf den Bildschirm = extra Konfetti!
#  Beenden: ESC-Taste druecken.
# =====================================================

import pygame
import random

pygame.init()
bildschirm = pygame.display.set_mode((480, 320), pygame.FULLSCREEN)
pygame.mouse.set_visible(False)
takt = pygame.time.Clock()

HIMMEL = (25, 70, 130)
WEISS = (255, 255, 255)
GELB = (255, 210, 0)
FARBEN = [(255, 210, 0), (227, 11, 92), (76, 198, 110),
          (120, 180, 255), (255, 140, 0), (255, 255, 255)]

schrift_gross = pygame.font.SysFont(None, 64)
schrift_mittel = pygame.font.SysFont(None, 44)
schrift_klein = pygame.font.SysFont(None, 26)


def mittig(text, schrift, y, farbe):
    """Schreibt einen Text genau in die Mitte des Bildschirms."""
    bild = schrift.render(text, True, farbe)
    bildschirm.blit(bild, (240 - bild.get_width() // 2, y))


def neues_konfetti(x, y, anzahl):
    """Laesst an einer Stelle neues Konfetti entstehen."""
    for _ in range(anzahl):
        konfetti.append({
            "x": x + random.randint(-50, 50),
            "y": y + random.randint(-40, 10),
            "tempo": random.uniform(1.0, 4.0),
            "farbe": random.choice(FARBEN),
        })


# Zum Start regnet es schon von oben
konfetti = []
for _ in range(120):
    neues_konfetti(random.randint(0, 480), random.randint(-320, 0), 1)

laeuft = True
try:
    while laeuft:

        # 1) Tasten und Beruehrungen pruefen
        for ereignis in pygame.event.get():
            if ereignis.type == pygame.QUIT:
                laeuft = False
            if ereignis.type == pygame.KEYDOWN and ereignis.key == pygame.K_ESCAPE:
                laeuft = False
            if ereignis.type == pygame.MOUSEBUTTONDOWN:
                neues_konfetti(ereignis.pos[0], ereignis.pos[1], 40)

        # 2) Konfetti fallen lassen
        for stueck in konfetti:
            stueck["y"] = stueck["y"] + stueck["tempo"]
            if stueck["y"] > 320:                 # unten raus?
                stueck["y"] = random.randint(-40, -5)   # oben wieder rein!
                stueck["x"] = random.randint(0, 480)

        # 3) Alles malen
        bildschirm.fill(HIMMEL)
        for stueck in konfetti:
            pygame.draw.rect(bildschirm, stueck["farbe"],
                             (stueck["x"], stueck["y"], 6, 10))

        mittig("Hallo Erik,", schrift_gross, 70, GELB)
        mittig("herzlichen Gl\u00fcckwunsch", schrift_mittel, 140, WEISS)
        mittig("zum Geburtstag!", schrift_mittel, 180, WEISS)
        mittig("Tipp mal auf den Bildschirm ...", schrift_klein, 280, WEISS)

        pygame.display.flip()
        takt.tick(30)   # 30 Bilder pro Sekunde

except KeyboardInterrupt:
    pass    # Strg+C in der Konsole = auch ein sauberes Ende

pygame.quit()
