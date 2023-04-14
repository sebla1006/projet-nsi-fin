import pygame
from classes.jeu import Jeu
pygame.init() # Importe tous les modules nécessaires au fonctionnement de pygame
g = Jeu()
g.boucle_principale()
pygame.quit()