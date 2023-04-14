import pygame
from classes.objet import Obj

class Porte(Obj):
    def __init__(self, couleur, img, rect):
        """ Instancie un objet de la classe Porte

        Arguments:
            couleur: type Tuple[int] => La couleur en tuple de couleurs (rouge, vert, bleu) de la porte
            img: type pygame.Surface => La porte en tant que surface 
            rect: type pygame.Rect => Le rectangle associé à la Porte
        """
        super().__init__(img, rect, "porte", couleur)
        self.etat = 0 # 0 = fermée, 1 = ouvert
        


    #####################################################################################################################
    #                                                                                                                   #
    #                                                                                                                   #
    #                                                 GETTERS                                                           #
    #                                                                                                                   #
    #                                                                                                                   #
    #####################################################################################################################


    def get_statut(self):
        """ Renvoie le statut de la porte

        sortie: type int => 0 = fermée, 1 = ouvert
        """
        return self.etat
    

    #####################################################################################################################
    #                                                                                                                   #
    #                                                                                                                   #
    #                                                 SETTERS                                                           #
    #                                                                                                                   #
    #                                                                                                                   #
    #####################################################################################################################


    def changer_etat(self, etat):
        """ Change l'état actuel de la porte

        Argument :
            etat: type int => 0 = fermée, 1 = ouvert
        """
        self.etat = etat


    #####################################################################################################################
    #                                                                                                                   #
    #                                                                                                                   #
    #                                                  AUTRES                                                           #
    #                                                                                                                   #
    #                                                                                                                   #
    #####################################################################################################################    


    def ouvrir(self, fen):
        """ Met une diode verte pour dire que le personne est bien à sa porte

        Arguments :
            fen: type pygame.Surface => La fenêtre sur lequel la diode verte sera affichée
        """
        
        # On crée un cercle de couleur verte, de rayon 10 et de centre l'intersection des diagonales du rectangle associé à la porte
        pygame.draw.circle(fen, (0, 255, 0), (self.get_x()+42, self.get_y()+50), 10)
        pygame.display.flip()
    
    def fermer(self, fen):
        """ Met une diode rouge pour dire que la porte est fermée

        Arguments :
            fen: type pygame.Surface => La fenêtre sur lequel la diode rouge sera affichée
        """

        # On crée un cercle de couleur rouge, de rayon 10 et de centre l'intersection des diagonales du rectangle associé à la porte
        pygame.draw.circle(fen, (255, 0, 0), (self.get_x()+42, self.get_y()+50), 10)
        pygame.display.flip()