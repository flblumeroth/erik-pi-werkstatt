# =====================================================
#  WANDUHR  -  fuer Erik
#  Dein erstes eigenes Python-Projekt!
#  Zeigt Uhrzeit und Datum gross auf dem Display,
#  unten waechst ein gelber Sekunden-Balken.
#  Beenden: ESC-Taste (oder Fenster schliessen).
# =====================================================

import pygame
import time

pygame.init()
bildschirm = pygame.display.set_mode((480, 320))
pygame.display.set_caption("Wanduhr")

schrift_gross = pygame.font.SysFont(None, 100)
schrift_klein = pygame.font.SysFont(None, 44)

laeuft = True
while laeuft:

    # Will jemand das Programm beenden?
    for ereignis in pygame.event.get():
        if ereignis.type == pygame.QUIT:
            laeuft = False
        if ereignis.type == pygame.KEYDOWN and ereignis.key == pygame.K_ESCAPE:
            laeuft = False

    # Wie spaet ist es gerade?
    uhrzeit = time.strftime("%H:%M:%S")
    datum = time.strftime("%d.%m.%Y")
    sekunde = int(time.strftime("%S"))

    # Alles malen
    bildschirm.fill((25, 70, 130))

    bild1 = schrift_gross.render(uhrzeit, True, (255, 255, 255))
    bildschirm.blit(bild1, (70, 90))

    bild2 = schrift_klein.render(datum, True, (220, 228, 245))
    bildschirm.blit(bild2, (150, 205))

    pygame.draw.rect(bildschirm, (255, 210, 0), (0, 306, sekunde * 8, 14))

    pygame.display.flip()
    pygame.time.wait(200)

pygame.quit()
