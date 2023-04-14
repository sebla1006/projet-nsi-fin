import pygame
from Fonctions.affichage_composants import *
from pygame.locals import *
from actions import *
from Fonctions.collisions_objet import *
from classes.niveau import Niveau
import time

class Jeu():
    def __init__(self):
        """ Instancie un objet de la classe Jeu
        """
        self.fenetre = pygame.display.set_mode((1200, 675)) # type pygame.Surface => La fenêtre où seront affichés les composants
        self.composants = [] # Tous les composants dans la fenêtre
        self.touches_pressees = {K_RIGHT: False, K_LEFT: False, K_UP: False, K_d: False, K_q: False, K_z: False}
        self.boutons = []
        self.fonctions_boutons = []

        self.fonction_dessin = self.affiche_menu_principal # self.fonction_dessin() affiche à l'écran les composants
        self.niveau = None # Le numéro du niveau que l'utilisateur est en train de faire
        self.joueur_veut_jouer = True # False seulement si l'utilisateur veut quitter



    #####################################################################################################################
    #                                                                                                                   #
    #                                                                                                                   #
    #                                                AFFICHAGE                                                          #
    #                                                                                                                   #
    #                                                                                                                   #
    #####################################################################################################################


    def affiche_menu_principal(self):
        """ Permet d'afficher l'integralité du menu principal 
        """
        self.effacer_variables()

        self.fenetre.fill((94,68,37)) # On remplit l'arrière d'un fond marron

        # Dessine les boutons et leur label
        dessine_text(self.fenetre, [{"police": None, "label": "Menu Principal", "taille": 70, "couleur": (255, 255, 255), "position": (600, 50)}])
        boutons_collision = dessine_bouton(
            self.fenetre,
            {
                "rect": [
                    [pygame.Rect(500, 300, 200, 50), pygame.Rect(500, 400, 200, 50)], (78,51,20) 
                ],
                "textes": [
                        {
                            "label": "Jouer", 
                            "police": "Arial", 
                            "taille": 20, 
                            "couleur": (255,255,255)
                        },
                        {
                            "label": "Quitter", 
                            "police": "Arial", 
                            "taille": 20, 
                            "couleur": (255,255,255)
                        }
                    ],
                "action": [jouer_bouton, quitter_bouton]
            }
        )
        self.boutons = boutons_collision
        
    
    def affiche_menu_niveau(self):
        """ Affiche le menu avec tous les niveaux
        """
        self.effacer_variables()
        
        # On crée tous les boutons qui correspondent aux niveaux
        boutons_collision = dessine_bouton(
            self.fenetre,
            {
                "rect": [
                    [pygame.Rect(140, 100, 929, 90), pygame.Rect(140, 210, 929, 90), pygame.Rect(140, 323, 929, 90), pygame.Rect(140, 435, 929, 90), pygame.Rect(140, 545, 929, 90)], (0,0,0) 
                ],
                "action": [test_bouton, test_bouton, test_bouton, test_bouton, test_bouton]
            }
        )

        # On affiche l'arrière plan
        affiche_surface(self.fenetre, "./Graphique/Niveaux.png", (1200, 675), (0,0))
        
        self.boutons = boutons_collision

    def afficher_un_niveau(self):
        """ Affiche le niveau passé en paramètre.
        """
        self.effacer_variables()
        self.niveau.afficher_composants()


    #####################################################################################################################
    #                                                                                                                   #
    #                                                                                                                   #
    #                                                    AUTRE                                                          #
    #                                                                                                                   #
    #                                                                                                                   #
    #####################################################################################################################

    
    def creer_classe_niveau(self, numero_niveau):
        """ Créer les classes asocciés aux composants d'un niveau (bloc, ascenseur, porte, etc...)

        Argument :
            numero_niveau: type Int => L'indice du niveau (/!\ SURTOUT PAS LE NUMERO DU NIVEAU !!!!!)
        
        sortie: type classes.niveau.Niveau => Une instance de la classe classes.niveau.Niveau
        """
        niveau_classe = Niveau(numero_niveau, self.fenetre, self)
        niveau_classe.creer_classes_composants()
        
        return niveau_classe

    
    def boucle_principale(self):
        """ Récupère les évènements clavier, souris et fenêtre.
        """
        # On affiche les modifications précédentes
        self.fonction_dessin()
        pygame.display.update()

        while self.joueur_veut_jouer:

            # On récupère les évènements clavier, souris et fenêtre (croix)
            for event in pygame.event.get():
                if event.type == QUIT: # Clique sur la croix
                    self.joueur_veut_jouer = False

                elif event.type == KEYDOWN: # Touche pressée
                    self.touches_pressees[event.key] = True

                elif event.type == KEYUP: # Touche relâchée
                    self.touches_pressees[event.key] = False

                elif event.type == pygame.MOUSEBUTTONUP and event.button == 1: # Clique gauche appuyé
                    bouton = gere_collisions_souris(event.pos, self.boutons)
                    if bouton: # Si la souris est sur un bouton on exécute la fonction liée au bouton
                        self.fonction_dessin = bouton.bouton_presse(self)

            # On affiche les modfication à l'écran
            self.fonction_dessin()
            pygame.display.update()
            time.sleep(.009) # On évite que les mouvements soient sacadés et on allège légèrement les tâches du processeur
    
    def effacer_variables(self):
        """ Efface toutes les variables du jeu
        """
        self.composants = []
        self.boutons = []
        self.fonctions_boutons = []