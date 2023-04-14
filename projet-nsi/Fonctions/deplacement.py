from pygame.locals import *
def deplacement(persos, touchesPressees, sols): 
    """ Déplace un personnage selon les touches pressées

    Arguments :
        persos: type List[Personnage] => Liste contenant les deux personnages du jeu
        touchesPressees: type Dict[Int, Bool] => Dictionnaire avec en clé les valeurs (ex. K_UP) des touches et en valeur si elles sont appuyées  
        sols: type List[Int] => La liste des ordonnées des différents sols qui composent le niveau

    sortie: type List[Personnage] => Renvoie les personnages qui se sont déplacés pendant l'exécution de la fonction
    
    """
    personnages = [False, False]
    # Pour chaque touche pressée on assigne à un évènement
    cle = ((K_RIGHT, K_LEFT, K_UP), (K_d, K_q, K_z)) # Désigne les touches requises pour bouger le personnage (droite, gauche, saut)
    i=0
    for combinaison in cle:

        # Déplacement à droite
        if touchesPressees[combinaison[0]]:
            persos[i].ajoutCoordBordHautGauche(1, 5) # On ajoute 5 aux coordonnées du personnage donc il va vers la droite
            persos[i].gere_deplacement_impossible(1) # On vérifie la légalité du déplacement
            personnages[i] = True
        
        # Déplacement à gauche
        if touchesPressees[combinaison[1]] == True:
            persos[i].ajoutCoordBordHautGauche(-1, -5) # On retire 5 aux coordonnées du personnage donc il va vers la gauche
            persos[i].gere_deplacement_impossible(-1) # On vérifie la légalité du déplacement
            personnages[i] = True

        

        # Le personnage saute
        if persos[i].get_saut(): # S'il saute actuellement déjà
            personnages[i] = True
            persos[i].saute(sols)
        elif touchesPressees[combinaison[2]] == True: # S'il ne saute pas mais qu'il appuie sur la touche pour sauter
                personnages[i] = True
                persos[i].set_saut_debut()
        
        i+=1
    
    return [persos[i] for i in range(2) if personnages[i]]