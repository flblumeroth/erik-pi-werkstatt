# =====================================================
#  WANDUHR  -  fuer Erik
#  Dein erstes eigenes Python-Projekt!
#  Stoppen: roter Stopp-Knopf in Thonny.
# =====================================================

import pygame
import time

pygame.init()
bildschirm = pygame.display.set_mode((480, 320))
schrift_gross = pygame.font.SysFont(None, 100)
schrift_klein = pygame.font.SysFont(None, 44)

while True:
    pygame.event.pump()                     # haelt das Fenster wach

    uhrzeit = time.strftime("%H:%M:%S")     # z. B. 15:42:33
    datum = time.strftime("%d.%m.%Y")       # z. B. 12.09.2026
    sekunde = int(time.strftime("%S"))      # 0 bis 59, als Zahl

    bildschirm.fill((25, 70, 130))          # blauer Hintergrund

    bild1 = schrift_gross.render(uhrzeit, True, (255, 255, 255))
    bildschirm.blit(bild1, (70, 100))

    bild2 = schrift_klein.render(datum, True, (220, 228, 245))
    bildschirm.blit(bild2, (150, 200))

    pygame.draw.rect(bildschirm, (255, 210, 0), (0, 306, sekunde * 8, 14))

    pygame.display.flip()                   # jetzt alles anzeigen!
    time.sleep(0.2)                         # kurze Pause, dann von vorn
