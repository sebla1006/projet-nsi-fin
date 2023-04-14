import pygame
from classes.objet import Obj

class Personnage(Obj):
    def __init__(self, couleur, img, rect):
        """ Instancie un objet de la classe Personnage

        Arguments : 
            couleur: type Tuple[int] => La couleur en tuple de couleurs (rouge, vert, bleu) du personnage
            img: type pygame.Surface => Le personnage en tant que surface 
            rect: type pygame.Rect   => Le rectangle associé au personnage
        """
        super().__init__(img, rect, "perso", couleur)
        self.pos = 0                 # L'orientation du personnage (1 vers la droite, -1 vers la gauche)
        self.saut = False            # Le personnage est en train de sauter ? saut = int si oui, sinon saut = False
        self.vide = False            # Si le personnage est dans le vide
        self.avance = [True, True]   # Si le personnage peut avancer [vers la gauche, vers la droite]



    #####################################################################################################################
    #                                                                                                                   #
    #                                                                                                                   #
    #                                                 GETTERS                                                           #
    #                                                                                                                   #
    #                                                                                                                   #
    #####################################################################################################################


    def get_orientation(self):
        """ Renvoie l'orientation du personnage (-1 : le personnage va à gauche, 1 : le personnage va à droite)

        sortie: type int
        """
        return self.pos
    
    def get_saut(self):
        """ Renvoie si le personnage saute ou s'il est au sol. True s'il saute, False dans le cas contraire

        sortie: type bool
        """
        return not isinstance(self.saut, bool) # On évite l'erreur 0 = False
    
    def get_valeurSaut(self):
        """ Renvoie l'intensité du saut actuel

        sortie: typle Int | Bool
        """
        return self.saut

    # ! On modifie la fonction get_y de la classe Obj afin qu'elle renvoie l'ordonnée du bord inférieur gauche et non celle du bord supérieur !
    def get_y(self):
        """ Renvoie la valeur de y du rectangle associé à l'objet

        sortie: type int 
        """
        return self.rect.bottomleft[1]
    
    def personnageSurSol(self):
        """ Renvoie si le personnage n'est pas sur une surface, autrement dit s'il est dans le vide

        sortie: type bool
        """
        return self.vide

    def deplacement_possible(self, sens):
        """ Renvoie si le déplacement est possible

        Argument :
            sens: type int => 1 droite -1 gauche
        """

        return self.avance[1 if sens == 1 else 0]
    

    #####################################################################################################################
    #                                                                                                                   #
    #                                                                                                                   #
    #                                                 SETTERS                                                           #
    #                                                                                                                   #
    #                                                                                                                   #
    #####################################################################################################################


    def set_posImg(self):
        """ Modifie l'orientation du personnage. (effectue ainsi une symétrie d'axe verticale)
        """
        self.set_img(pygame.transform.flip(self.get_img(), True, False)) # On change l'orientation de l'image
        self.pos = -1 if self.pos == 1 else 1 # On change l'orientation dans la classe
    

    def set_saut_debut(self):
        """ Donne l'impulsion au persnnage pour qu'il effectue son saut
        """
        self.saut = 7
    

    def set_fin_saut(self):
        """ Termine le saut du joueur
        """
        self.saut = False


    def set_vide(self):
        """ Permet d'actualiser l'état du personnage en indiquant que ce dernier est dans le vide
        """
        self.vide = True

    
    #####################################################################################################################
    #                                                                                                                   #
    #                                                                                                                   #
    #                                                  AUTRES                                                           #
    #                                                                                                                   #
    #                                                                                                                   #
    #####################################################################################################################
    
    
    def ajoutCoordBordHautGauche(self, sens, x=0, y=0):
        """ Ajoute aux coordonnées du rectangle associé au personnage les valeurs entrées

        Arguments :
            sens: type int => Si x doit être incrémenté (vers la droite (sens = 1)) ou décrémenté (vers la gauche (sens = -1))
            x: type int
            y: type int
        """
        # On vérifie si l'on doit modifier l'orientation du personnage
        if self.get_orientation() != sens:
            self.set_posImg()

        # On effectue la modification des coordonnées selon les paramètres
        self.set_coordBasGauche((self.get_x()+x, self.get_y()+y)) 

        # On évite que les personnages touchent les bords
        if self.get_x() < 19 : # Il atteint le bord gauche
            self.avance[0] = False
        elif self.get_x() > 1141: # Il atteint le bord droit
            self.avance[1] = False



    def gere_deplacement_impossible(self, sens):
        """ Gère la légalité des déplacement latéraux du joueur
        
        Argument :
            sens: type int => 1 droite -1 gauche
        """

        if sens == -1 : 
            # Le personnage va à gauche
            if not self.avance[0]: 
                # Le personnage s'est déplacé vers la gauche sans y être autorisé
                # On le remet à ses coordonnées initiales
                self.set_coordBasGauche((self.get_x()+5, self.get_y()))
                self.avance[0] = True

        else : 
            # Le personnage va à droite
            if not self.avance[1]: 
                # Le personnage s'est déplacé vers la droite sans y être autorisé
                # On le remet à ses coordonnées initiales
                self.set_coordBasGauche((self.get_x()-5, self.get_y())) 
                self.avance[1] = True



    def saute(self, floors):
        """ Agis sur le personnage quand il saute et termine son saut en cas de sol touché
        
        Argument :
            sols: type List[Int] => La liste contenant l'ordonnée de chaque sol du niveau
        """

        y_pos = self.get_rect().bottomleft[1] # L'ordonnée du personnage
        sol_a_atteindre = self.sol_a_atteindre(floors, y_pos) # L'ordonnée du sol le plus proche du personnage

        # Si le personnage atteindra le sol à l'instant suivant
        if sol_a_atteindre+self.saut <= y_pos:
            rect = self.get_rect()
            self.set_coordBasGauche((rect.bottomleft[0], sol_a_atteindre)) # On met le personnage au sol
            self.set_fin_saut()
            
        else: 
            # Le personnage n'atteint pas de sol à l'instant t+1
            self.ajoutCoordBordHautGauche(self.pos, 0, - self.saut)
            self.saut -= 1
        
    
    
    def personnage_dans_vide(self, sols):
        """ Permet au personnage qui est dans le vide de redescendre au sol le plus proche

        Argument :
            sols: type List[Int] => La liste contenant l'ordonnée de chaque sol du niveau
        """
        sol = self.sol_a_atteindre(sols, self.get_y()) # sol le plus proche

        # Si le personnage est sur le sol
        if self.get_y() >= sol:
            self.set_coordBasGauche((self.get_x(), sol))
            self.vide = False
        else: 
            self.saut-=1