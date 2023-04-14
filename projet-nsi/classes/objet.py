import pygame
class Obj:
    def __init__(self, img, rect, type_obj, couleur = None):
        """ Instancie un objet de la classe Obj

        Arguments : 
            img:        type pygame.Surface     => L'objet en tant que surface 
            rect:       type pygame.Rect        => Le rectangle associé à l'objet
            type_obj:   type Str                => Type de l'objet
            couleur:      type Tuple[int] | None  => La couleur en tuple de couleurs (rouge, vert, bleu) de l'Obj
        """
        self.couleur = couleur
        self.rect = rect
        self.img = img
        self.type_obj = type_obj
    


    #####################################################################################################################
    #                                                                                                                   #
    #                                                                                                                   #
    #                                                 GETTERS                                                           #
    #                                                                                                                   #
    #                                                                                                                   #
    #####################################################################################################################


    def get_couleur(self):
        """ Renvoie la couleur de l'objet

        sortie: type Tuple[Int] => La couleur en tuple de couleurs (rouge, vert, bleu)
        """
        return self.couleur
    
    def get_img(self):
        """ Renvoie la surface de l'objet

        sortie: type pygame.Surface
        """
        return self.img

    def get_type_obj(self):
        """ Renvoie le type de l'objet

        sortie: type Str
        """
        return self.type_obj

    def get_coordBordSupGauche(self):
        """ Renvoie les coordonnées du bord supérieur gauche du rectangle associé à l'objet

        sortie: type Tuple[Int]
        """
        return (self.rect.x, self.rect.y)
    
    def get_coordBordBasGauche(self):
        """ Renvoie les coordonnées du bord inférieur gauche du rectangle associé à l'objet
        
        sortie: type Tuple[Int]
        """
        return self.rect.bottomleft
    
    def get_x(self):
        """ Renvoie la valeur de x du rectangle associé à l'objet

        sortie: type Int 
        """
        return self.rect.x
    
    def get_y(self):
        """ Renvoie la valeur de y du rectangle associé à l'objet

        sortie: type Int 
        """
        return self.rect.y
    
    def get_rect(self):
        """ Renvoie l'instance du rectangle associé à l'objet de la classe pygame.Rect

        sortie: type pygame.Rect
        """
        return self.rect
    

    #####################################################################################################################
    #                                                                                                                   #
    #                                                                                                                   #
    #                                                 SETTERS                                                           #
    #                                                                                                                   #
    #                                                                                                                   #
    #####################################################################################################################
    

    def set_img(self, obj):
        """ Modifie la surface de l'objet

        Argument :
            obj: type pygame.Surface
        """
        self.img = obj
    
    def set_coordSupGauche(self, coord):
        """ Modifie les coordonnées du bord supérieur gauche du rectangle associé à l'objet

        Argument :
            coord: type Tuple[Int]
        """
        self.rect.topleft = coord
    
    def set_coordBasGauche(self, coord):
        """ Modifie les coordonnées du bord inférieur gauche du rectangle associé à l'objet

        Argument :
            coord: type Tuple[Int]
        """
        self.rect.bottomleft = coord
    

    #####################################################################################################################
    #                                                                                                                   #
    #                                                                                                                   #
    #                                                  AUTRES                                                           #
    #                                                                                                                   #
    #                                                                                                                   #
    #####################################################################################################################


    def ajouter_coordSupGauche(self, coord):
        """ Modifie les coordonnées en ajoutant les entiers passés paramètre

        Argument :
            coord:  type tuple => Le tuple (x, y) tel que les coordonnées du personnages seront personnage.x + x et personnage.y + y

        Exemples :
        >>> objet = Obj(...) # coordonnées d'objet sont (0,0)
        >>> objet.ajouter_coordSupGauche((3, 2)) # Nouvelles coordonnées : (3, 2)
        >>> objet.ajouter_coordSupGauche((1, 3)) # Nouvelles coordonnées : (4, 5)
        >>> objet.ajouter_coordSupGauche((0, -1)) # Nouvelles coordonnées : (4, 4)
        """
        self.set_coordSupGauche((self.get_x()+coord[0], self.get_y()+coord[1]))
    
    def sol_a_atteindre(self, sols, y_pos):
        """ Renvoie l'ordonnée du sol le plus proche
        
        Arguments :
            sols: type List[Int] => La liste contenant l'ordonnée de chaque sol du niveau
            y_pos: type Int => L'ordonnée du personnage
        
        sortie: type Int
        """
        res = sols[0]
        # On vérifie pour chaque sol si le sol est en dessous de l'objet
        # Si oui, c'est le sol le plus proche
        for i in range(1,len(sols)):
            if sols[i] >= y_pos:
                res = sols[i]
            
        return res