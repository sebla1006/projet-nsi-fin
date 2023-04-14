from classes.objet import Obj

class JeuBouton(Obj):
    def __init__(self, couleur, img, rect, action, identifiant, nbbloc):
        """ Instancie un objet de la classe JeuBouton

        Arguments : 
            couleur: type Tuple[int] | None => La couleur en tuple de couleurs (rouge, vert, bleu) du bouton
            img: type pygame.Surface => L'ascenseur en tant que surface
            rect: type pygame.Rect   => Le rectangle associé à l'ascenseur
            action: type classes.ascenseur.Ascenseur => L'ascenseur à lever ou baisser quand le bouton est appuyé/relâché
            identifiant: type Int => L'identifiant de l'ascenseur à lever ou baisser
            nbbloc: type Int => Le nombre total de bloc présent dans le niveau
        """
        super().__init__(img, rect, "bouton", couleur)
        self.action = action
        self.id = identifiant
        self.statut_actuel = [False, False] + [False for i in range(nbbloc)] # L'état actuel selon les personnages et blocs 
        


    #####################################################################################################################
    #                                                                                                                   #
    #                                                                                                                   #
    #                                                 GETTERS                                                           #
    #                                                                                                                   #
    #                                                                                                                   #
    #####################################################################################################################


    def get_id(self):
        """ Renvoie l'identifiant de l'ascenseur associé au bouton
        """
        return self.id
    
    def get_action(self):
        """ Renvoie l'instance de l'ascenseur associé au bouton
        """
        return self.action

    def get_etat_actuel(self):
        """ Renvoie l'état actuel du bouton True = appuyé, False = relâché
        """
        return True in self.statut_actuel

    
    #####################################################################################################################
    #                                                                                                                   #
    #                                                                                                                   #
    #                                                 SETTERS                                                           #
    #                                                                                                                   #
    #                                                                                                                   #
    #####################################################################################################################


    def set_etat(self, etat, index):
        """ Met l'état d'un composant comme bouton appuyé ou relâché

            Arguments :
                etat : type Bool => Le nouvel état du bouton
                index : type Int => L'indice du composant dans la liste bloc.statut_actuel
        """
        self.statut_actuel[index] = etat


    #####################################################################################################################
    #                                                                                                                   #
    #                                                                                                                   #
    #                                                 ACTIONS                                                           #
    #                                                                                                                   #
    #                                                                                                                   #
    #####################################################################################################################


    def bouton_presse(self, personnages, blocs):
        """ Gère le cas où le bouton est appuyé

            Arguments :
                personnages : type List[Personnage] => La liste de tous les personnages
                blocs : type List[Bloc] => La liste de tous les blocs
        """
        elevator = self.action
        elevator.monter(personnages, blocs)
        

    def bouton_relache(self, personnages, blocs):
        """ Gère le cas où le bouton est appuyé

            Arguments :
                personnages : type List[Personnage] => La liste de tous les personnages
                blocs : type List[Bloc] => La liste de tous les blocs
        """
        elevator = self.action
        elevator.descendre(personnages, blocs)