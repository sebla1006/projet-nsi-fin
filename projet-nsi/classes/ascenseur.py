from classes.objet import Obj

class Ascenseur(Obj):
    def __init__(self, couleur, img, rect, pos_basse, pos_haute):
        """ Instancie un objet de la classe Ascenseur

        Arguments : 
            couleur: type Tuple[int] => La couleur en tuple de couleurs (rouge, vert, bleu) de l'ascenseur
            img: type pygame.Surface => L'ascenseur en tant que surface
            rect: type pygame.Rect   => Le rectangle associé à l'ascenseur
            pos_basse: type Tuple[Int] => Les coordonnées de la position basse de l'ascenseur
            pos_haut: type Tuple[Int] => Les coordonnées de la position haute de l'ascenseur
        """

        super().__init__(img, rect, "ascenseur", couleur)
        self.pos_basse = pos_basse      # La position dite "basse" i.e. la position initale de l'ascenseur 
        self.pos_haute = pos_haute      # La position dite "haute" i.e. la position quand un bouton relié à cet ascenseur est actionné
        self.statut = "bas"             # L'état actuel de l'ascenseur (levé ou baissé)
        self.composantsAvantDessus = [] # Les composants sur l'ascenseur à l'instant t-1



    #####################################################################################################################
    #                                                                                                                   #
    #                                                                                                                   #
    #                                                 GETTERS                                                           #
    #                                                                                                                   #
    #                                                                                                                   #
    #####################################################################################################################


    def get_pos_haute(self):
        """ Renvoie la position haute de l'ascenseur
        """
        return self.pos_haute
    
    def get_pos_basse(self):
        """ Renvoie la position basse de l'ascenseur
        """
        return self.pos_basse

    def get_statut(self):
        """ Renvoie le statut de l'ascenseur (bas, haut, vers haut, vers bas)
        """
        return self.statut

    def get_composantsAvantDessus(self):
        """ Renvoie les composants présents à l'instant t-1
        """
        return self.composantsAvantDessus
    

    #####################################################################################################################
    #                                                                                                                   #
    #                                                                                                                   #
    #                                                 SETTERS                                                           #
    #                                                                                                                   #
    #                                                                                                                   #
    #####################################################################################################################


    def set_statut(self, statut):  
        """ Modifie le statut de l'ascenseur
         
        Argument :
            statut: type Str => Le statut de l'ascenseur
        """
        self.statut = statut

    
    #####################################################################################################################
    #                                                                                                                   #
    #                                                                                                                   #
    #                                             DEPLACEMENT                                                           #
    #                                                                                                                   #
    #                                                                                                                   #
    #####################################################################################################################
    
    def monter(self, personnages, blocs):
        """ Fait monter l'ascenseur

        Arguments :
           personnages: type List[classes.personnage.Personnage] => La liste de tous les personnages
           bloc: type List[classes.bloc.Bloc] => La liste de tous les blocs qui composent le niveau
        """

        # Si l'ascenseur n'est pas déjà en position haute 
        if self.get_statut() != "haut":

            # On déplace l'ascenseur
            self.statut = "vers haut"
            self.ajouter_coordSupGauche((0,-5))

            # On déplace tous les composants sur l'ascenseur
            composantsSur = self.get_composantSur(personnages, blocs)
            self.deplace_composants(composantsSur, self.get_composantsAvantDessus(), +5)


            # Si l'ascenseur vient d'atteindre sa position haute
            if self.get_pos_haute()[1] >= self.get_y():
                self.set_statut("haut")

    def descendre(self, personnages, blocs):
        """ Fait descendre l'ascenseur

            Arguments :
                personnages: type List[classes.personnage.Personnage] => La liste de tous les personnages
                bloc: type List[classes.bloc.Bloc] => La liste de tous les blocs qui composent le niveau
        """
        
        # L'ascenseur ne va pas descendre si 
        # 1. Il y a des composants sous l'ascenseur
        # 2. L'ascenseur est déjà dans sa position basse 
        composants_sous_ascenseur = self.get_composantsSous(personnages + blocs)
        if len(composants_sous_ascenseur) == 0 and  self.get_statut() != "bas":

            # On déplace l'ascenseur
            self.statut = "vers bas"
            self.ajouter_coordSupGauche((0,5))

            # On déplace tous les composants sur l'ascenseur
            componentsOn = self.get_composantSur(personnages, blocs)
            self.deplace_composants(componentsOn, self.get_composantsAvantDessus(), -5)
            
            
            # Si l'ascenseur vient d'atteindre sa position basse
            if self.get_pos_basse()[1] <= self.get_y():
                self.set_statut("bas")

    def deplace_composants(self, composants, composantsDebutDessus, coeff=0):
        """ Déplace les composants qui sont sur l'ascenseur

            Arguments :
                composants : type List[Obj] => La liste de tous les objets sur l'ascenseur à l'instant t
                blocs : type List[Obj] => La liste de tous les objets sur l'ascenseur à l'instant t-1
                coeff : type int => L'oppposé du coefficient de poussé (0 si l'ascenseur ne bouge pas, -1 vers la DROITE, 1 vers la GAUCHE)
        """

        # On gère le cas où l'on doit ajouter un composant à la liste 
        if len(composants) > len(composantsDebutDessus):

            # On récupère tous les éléments présents dans composants mais pas dans composantsDebutDessus
            for composant in self.get_ext_l2(composants, composantsDebutDessus):
                y_composant = composant.get_rect().bottomleft[1]
                y_ascenseur = self.get_y()+coeff

                # On vérifie si le personnage est distant au minmum de 5 pixels de l'ascenseur
                if y_ascenseur >= y_composant and y_ascenseur >= y_composant-5: 
                    if composant.get_type_obj() == "perso":
                        composant.set_fin_saut()
                    composantsDebutDessus.append(composant)


        
        index = 0
        for composant in composantsDebutDessus:
            if composant in composants: # Si le composant était là et est là
                # On met ses coordonnées aux coordonnées de l'ascenseur
                
                    if composant.get_type_obj() == 'perso' :
                        composant.set_coordBasGauche((composant.get_rect().bottomleft[0], self.get_rect().topleft[1]))
                    else:
                        composant.set_coordBasGauche((composant.get_rect().bottomleft[0], self.get_rect().topleft[1]))


            else:

                # On gère le cas où l'on doit retirer un composant de la liste
                if composant.get_type_obj() == "perso" :

                    if not composant.get_saut():
                        composant.set_vide()

                else:

                    composant.dans_le_vide()

                del(composantsDebutDessus[index])
            index+=1
        
        
                
            
    def get_ext_l2(self, list1, list2):
        """ Renvoie la liste des éléments qui sont dans list1 mais pas dans list2
        list1 : type List
        list2 : type List

        sortie : type List
        """
        res = []
        for element in list1:
            if element not in list2:
                res.append(element)
        return res
    

    #####################################################################################################################
    #                                                                                                                   #
    #                                                                                                                   #
    #                                              COLLISIONS                                                           #
    #                                                                                                                   #
    #                                                                                                                   #
    #####################################################################################################################


    def get_composantsSous(self, composants):
        """ Renvoie la liste des éléments qui sont au dessous de l'ascenseur
        composant: type List[Obj]

        sortie: type List[Obj]
        """
        componentsUnder = []
        ascenseur_rectangle = self.get_rect()
        for composant in composants:

            # On note les informations du rectangles
            component_rec = composant.get_rect()
            component_coordSupGauche = component_rec.topleft
            component_coordInfDroit = component_rec.topright

            # S'il y a collision en dessous de l'ascenseur
            if ascenseur_rectangle.collidepoint((component_coordSupGauche[0]+3, component_coordSupGauche[1])) or ascenseur_rectangle.collidepoint((component_coordInfDroit[0]-3, component_coordInfDroit[1])):
                componentsUnder.append(composant)

        return componentsUnder

    def get_composantSur(self, personnages, blocs):
        """ Renvoie la liste des composants qui sont sur l'ascenseur

            Arguments :
                personnages : type List[Personnage] => La liste de tous les personnages
                blocs : type List[Bloc] => La liste de tous les blocs
        """

        composantSur = []

        # Les coordonnées de l'ascenseur
        asc_bord_gauche = self.get_rect().topleft[0]
        asc_bord_droit = self.get_rect().topright[0]

        for personnage in personnages:
            perso_bord_gauche = personnage.get_rect().topleft[0]+12
            perso_bord_droit = personnage.get_rect().topright[0]-12

            # On vérifie, ici, les collisions
            if asc_bord_gauche < perso_bord_droit and asc_bord_droit > perso_bord_gauche:
                composantSur.append(personnage)

        for bloc in blocs:
            bloc_bord_gauche = bloc.get_rect().topleft[0]
            bloc_bord_droit = bloc.get_rect().topright[0]

            # On vérifie s'il y a collision entre un bloc et un personnage
            if asc_bord_gauche < bloc_bord_droit and asc_bord_droit > bloc_bord_gauche:
                composantSur.append(bloc)

        return composantSur