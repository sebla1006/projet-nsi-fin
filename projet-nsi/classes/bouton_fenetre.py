class Bouton():
    def __init__(self, rect, label, action, identifiant):
        """ Instancie un objet de la classe Bouton

        Arguments :
            rect: type pygame.Rect => Le rectangle associé au bouton
            label: type Str => Le texte qui est inscrit sur le bouton
            action: type Function => La fonction qui sera exécuté lorsque le bouton sera pressé
            identifiant: type Int => L'identifiant du bouton        
        """
        self.rect = rect
        self.label = label
        self.action = action
        self.identifiant = identifiant


    
    #####################################################################################################################
    #                                                                                                                   #
    #                                                                                                                   #
    #                                                 GETTERS                                                           #
    #                                                                                                                   #
    #                                                                                                                   #
    #####################################################################################################################


    def get_rect(self):
        """ Renvoie le rectangle associé au bouton
        
        sortie: type pygame.Rect
        """
        return self.rect

    def get_label(self):
        """ Renvoie l'inscription qui se trouve sur le bouton

        sortie: type Str
        """
        return self.label

    def get_id(self):
        """ Renvoie l'identifiant du bouton 

        sortie: type Int
        """
        return self.identifiant    
    
    
    #####################################################################################################################
    #                                                                                                                   #
    #                                                                                                                   #
    #                                                  ACTION                                                           #
    #                                                                                                                   #
    #                                                                                                                   #
    #####################################################################################################################


    def bouton_presse(self, partie):
        """ Exécute l'action à réalisé lorsque le bouton est pressé

        Argument :
            partie: type classes.jeu.Jeu
        
        sortie: type Function => La nouvelle fonction de dessin
        """
        return self.action(partie, self)
    
