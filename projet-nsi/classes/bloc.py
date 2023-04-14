import pygame
from classes.objet import Obj

class Bloc(Obj):
    def __init__(self, couleur, img, rect, identifiant):
        """ Instancie un objet de la classe Bloc

        Arguments :
            couleur : type Tuple[Int] => La couleur du bloc
            img : type pygame.Surface => Le bloc en tant que surface
            rect : type pygame.Rect => Le bloc en tant que rectangle
            identifiant : type Int => L'identifiant du bloc
        """
        super().__init__(img, rect, "bloc", couleur)
        self.personnageDessus = [] # Personnages sur le bloc à l'instant t
        self.personnageDessusAvant = [] # Personnages sur le bloc à l'état d'avant (t-1)

        self.sol = True # Le bloc est au sol
        self.force = 0 # Un entier relatif qui fait descendre le bloc s'il est dans le vide (appartient à ]-infini; 0])
        
        self.identifiant = identifiant 
    
        self.statut = [False, False] # Le mouvement à gauche statut[0] à droite statut[1]

    def gere_collision(self, personnages):
        """ Gère les collisions entre le bloc et un personage

        personnages: type tuple[classes.personnage.Personnage]
        """
        self.statut = [False, False] # Le bloc est à l'état initial donc il ne bouge pas

        # On récupère les informations du rectangle
        bloc_rec = self.get_rect()
        bloc_coordInfDroit = bloc_rec.bottomright
        bloc_coordInfGauche = bloc_rec.bottomleft


        for personnage in personnages:
    
            personnage_rect = personnage.get_rect()
            collision_rect = pygame.Rect(personnage_rect.topleft[0]+8, personnage_rect.topleft[1], 20, 58) # On prend le rectangle de collision
            personnage_coordBasDroite = personnage_rect.bottomright
            personnage_coordBasGauche = personnage_rect.bottomleft

            
            # Si le personnage est au-dessus du bloc
            if personnage_coordBasGauche[1] <= bloc_rec.topleft[1]+3 :

                # Si le personnage est en collision avec le bloc ET que le personnage descend
                if bloc_rec.colliderect(collision_rect) and personnage.get_valeurSaut() < 0:
                    personnage.set_fin_saut()

                    # On ne touche pas à son abcisse mais on met son ordonnée à celle du bloc
                    personnage.set_coordBasGauche((personnage_coordBasGauche[0], bloc_rec.topleft[1]))

            # On vérifie si le bloc doit être poussé vers la droite 
            # 1. Si le bord inférieur droit est en collision avec le bloc => Le bloc va vers la droite
            elif bloc_rec.collidepoint((personnage_coordBasDroite[0]-10, personnage_coordBasDroite[1]-1)):                
                self.statut[1] = personnage

            # 2. Si le bord inférieur gauche est en collision avec le bloc => Le bloc va vers la gauche
            elif bloc_rec.collidepoint((personnage_coordBasGauche[0]+10, personnage_coordBasGauche[1]-1)):                
                self.statut[0] = personnage

            self.gere_composants(collision_rect, personnage)


        
        # Si le bloc doit aller vers la gauche
        if self.statut[0] :

            # Si le bloc doit aller vers la droite
            if self.statut[1]:
                # Dans ce cas le bloc ne doit pas traverser les personnages 
                # Et les personnages ne doivent pas traverser le bloc
                # Donc, ni le bloc, ni les personnages ne bougent
                self.statut[0].avance[0] = False            
                self.statut[1].avance[1] = False

            else:
                # Le bloc va vers la droite
                x = self.statut[0].get_rect().bottomleft[0]-10

                # On évite de bloquer le bloc
                if x > 41:
                    self.set_coordBasGauche((x, bloc_coordInfGauche[1]))

        elif self.statut[1]:
            # Le bloc va vers la gauche
            x = self.statut[1].get_rect().bottomright[0]-10

            # On évite de bloquer le bloc
            if x < 1120:
                self.set_coordBasGauche((self.statut[1].get_rect().bottomright[0]-10, bloc_coordInfDroit[1]))
            


    

    def get_personnageSur(self, personnage_collision, personnage):
        """ Récupère les personnages qui sont sur le bloc

        Arguments :
            personnage_collision : type pygame.Rect => Le rectangle qui définit la "hitbox" du personnage
            personnage: type classes.personnage.Personnage

        Valeur de retour
            sortie : type list => Tous les personnages qui sont sur le bloc
        """

        res = []
        bloc_rec = self.get_rect()
        if bloc_rec.colliderect(personnage_collision): 
            res.append(personnage)
        return res
        
    
    
    def gere_composants(self, rectangle_collision, personnage):
        """ On gère les composants lorsqu'il y a sortie et entrée sur le bloc

        Arguments :
            rectangle_collision : type pygame.Rect => hibox du personnage
            personnage : type classes.personnage.Personnage
        """

        # On récupère la liste des personnages qui sont sur le bloc à l'instant t
        personnageSurInstant = self.get_personnageSur(rectangle_collision, personnage)

        # S'il n'y a pas de personnage
        if len(personnageSurInstant) != 0 : 

            # Si le personnage vient d'arriver
            if personnageSurInstant[0] not in self.personnageDessus : 

                # On ajoute ce personnage à l'instant t-1
                self.personnageDessus = self.personnageDessus + personnageSurInstant
        else:
            # S'il n'y a pas de collision à l'instant MAIS qu'il y en avait une à l'instant t-1
            if personnage in self.personnageDessus:

                # On l'enlève de l'instant t-1
                self.personnageDessus.remove(personnage)
                if not personnage.get_saut():
                    # S'il ne saute pas et qu'il a une abcisse qui ne fait pas partie du bloc alors on dit que ce personnage est dans le vide
                    personnage.set_vide()
    
    def est_sur_sol(self):
        """ Renvoie si le personne est sur le sol (True) ou s'il est en l'air (False)

        sortie: type bool => Le personnage est sur le sol ?
        """
        return self.sol

    def dans_le_vide(self):
        """ Gère le cas où le bloc est dans le vide
        """
        self.sol = False

    def aller_sol(self, sol):
        """ Permet au bloc d'atteindre le sol le plus proche

        Argument :
            sol: type Int => ordonnée du sol le plus proche
        """

        valeur_force = self.force+1
        bloc_y = self.get_rect().bottomleft[1]

        # Si à t+1 le bloc sera en dessous du sol
        if bloc_y + valeur_force >= sol:
            self.ajouter_coordSupGauche((0, sol - bloc_y))
            self.sol = True
            self.force = 0
        else: 
            self.force = valeur_force
            self.ajouter_coordSupGauche((0,self.force))