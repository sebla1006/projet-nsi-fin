import pygame
from Fonctions.jsonfonctions import get_json_file
from classes.personnage import Personnage
from classes.objet import Obj
from classes.ascenseur import Ascenseur
from classes.jeu_bouton import JeuBouton
from classes.bloc import Bloc
from classes.bouton_fenetre import Bouton
from classes.porte import Porte
from actions import *
from Fonctions.affichage_composants import *
from Fonctions.collisions_objet import *
from Fonctions.deplacement import deplacement
from time import time

class Niveau():
    def __init__(self, identifiant, fenetre, partie):
        """ Instancie un objet de la classe Porte

        Arguments : 
            identifiant: type Str => Le numéro du niveau
            fenetre: type pygame.Surface => La fenêtre où les composants sont affichés
            partie: type classes.jeu.Jeu => La classe principale
        """

        # On récupère toutes les informations liées aux niveaux
        niveau_informations = get_json_file("./Niveaux/levels.json")
        niveau_details = niveau_informations["levels"][identifiant]


        # Les informations liés à UN niveau
        self.identifiant = identifiant # L'identifiant du niveau
        self.composants  = niveau_details["components"] # Tous les composants qui constituent le niveau
        self.sols = niveau_details["floors"] # Tous les sols du niveau
        self.nom = niveau_details["name"] # Nom du niveau
        self.nbgemme = niveau_details["contraintes"]["gemme"] # Nombre de gemme à atteindre pour obtenir la distinction "gemme"
        self.temps_fini = niveau_details["contraintes"]["temps"] # Le temps en seconde à ne pas dépasser pour obtenir la distinction "temps"


        # Les informations de la fenêtre
        self.fenetre = fenetre # La Surface sur lequel le programme va afficher les composants
        self.partie = partie # L'objet Jeu où une instance de cette classe a été créée
        self.pause = False # Si le jeu est en pause
        self.stop = False # Si le joueur perd la partie
        self.gagne = False # Si le joueur a gagné



        # Ici on stocke toutes les composants du niveau
        self.personnages = [None, None]
        self.boutons = [] # Tous les boutons reliés aux ascenseurs du niveau (!= boutons cliquables)
        self.ascenseurs = [] 
        self.liquides = []
        self.blocs = [] 
        self.gemmes = []
        self.portes = [] 

        self.fenetre_composant = [] # Tous les composants sont stockés dans cette variable (boutons, ascenseurs, liquides, ...)
        self.fenetre_texte_composant = [] # Tous les objets qui sont de type texte sont stockés ici


        # Le temps
        self.debut_niveau = time() # L'heure du début du niveau (sous forme de secondes écoulées depuis le 1er janvier 1970)
        self.temps = 0 # Le temps écoulé depuis le début du niveau
        self.seconde = 0 # Le nombre de seconde écoulées



    def get_id(self):
        """ Renvoie l'identifiant du niveau

        sortie: type Int => Le numéro du niveau
        """
        return self.identifiant
    
    
    #####################################################################################################################
    #                                                                                                                   #
    #                                                                                                                   #
    #                                              INITIALISATION                                                       #
    #                                                                                                                   #
    #                                                                                                                   #
    #####################################################################################################################    
    

    def creer_classes_composants(self):
        """ Créer les classes des composants pour que les informations du niveau soient mis à jour 
        """
        couleurs = ["vert", "violet", "noir"]
        

        #########################################################
        #                                                       #
        #                                                       #
        #                        Sols                           #
        #                                                       #
        #                                                       #
        #########################################################

        sol_i = 0
        for sol_y in self.sols:
            if sol_y != 653:
                
                sol = init_Obj("./Graphique/plat.png", (1073, 20)) 
                sol = Obj(sol, sol.get_rect(), "sol")
                if sol_i % 2 == 0:
                    sol.set_coordSupGauche((18, sol_y))
                else: 
                    sol.set_coordSupGauche((107, sol_y))
                self.fenetre_composant.append(sol)
                sol_i+=1

        
        #########################################################
        #                                                       #
        #                                                       #
        #                      Portes                           #
        #                                                       #
        #                                                       #
        #########################################################

        i = 0
        # On ajoute les portes aux composants à afficher
        for porte in self.composants["portes"]:
            porte_id = porte["index"]
            port = init_Obj(f"./Graphique/porte{porte_id}.png", (84, 100)) # On crée une surface
            port = Porte(couleurs[i], port, port.get_rect())               # On crée une instance de classe Porte
            port.set_coordBasGauche(porte["position"])                     # On ajuste ses coordoonées
            self.portes.append(port)                                       
            self.fenetre_composant.append(port)
            i+=1


        #########################################################
        #                                                       #
        #                                                       #
        #                   Personnages                         #
        #                                                       #
        #                                                       #
        #########################################################

        for i in range(2):
            self.personnages[i] = init_Obj(f"./Graphique/perso{i+1}.png", (40, 57))                             # On initialise l'objet
            self.personnages[i] = Personnage(couleurs[i], self.personnages[i], self.personnages[i].get_rect())  # On crée la Classe personnage 
            self.personnages[i].set_coordBasGauche((20, 653))                                                   # On met le personnage en bas de l'écran   
            self.personnages[i].set_posImg()                                                                    # On le met dans le bon sens
            self.fenetre_composant.append(self.personnages[i])                                                  # Personnage fait partie des éléments de la fenêtre


        #########################################################
        #                                                       #
        #                                                       #
        #                     Liquides                          #
        #                                                       #
        #                                                       #
        #########################################################

        for elm in self.composants["liquide"]:
            col = elm["id"]
            liquide = init_Obj(f"./Graphique/liquide{col}.png", (50,31))                   # On crée une surface
            liquide = Obj(liquide, liquide.get_rect(), "liquid", couleurs[int(col)-1])     # On crée la Classe Obj
            liquide.set_coordSupGauche(elm["position"])                                    # On ajuste ses coordoonées
            self.fenetre_composant.append(liquide)
            self.liquides.append(liquide)


        #########################################################
        #                                                       #
        #                                                       #
        #                     Ascenseur                         #
        #                                                       #
        #                                                       #
        #########################################################
        
        for elm in self.composants["elevator"]:
            elevator = init_Obj("./Graphique/elevateur.png", (89, 18)) # On crée une surface
            elevator = Ascenseur(None, elevator, elevator.get_rect(), elm["position"], elm["highPos"]) # On crée la Classe Ascenseur
            elevator.set_coordSupGauche(elm["position"]) # On ajuste ses coordoonées
            self.fenetre_composant.append(elevator)
            self.ascenseurs.append(elevator)
        


        #########################################################
        #                                                       #
        #                                                       #
        #                        Blocs                          #
        #                                                       #
        #                                                       #
        #########################################################

        index = 2
        for elm in self.composants["bloc"]:
            bloc = init_Obj("./Graphique/bloc.png", (25, 25)) # On crée une surface
            bloc = Bloc(None, bloc, bloc.get_rect(), index) # On crée la Classe Bloc
            bloc.set_coordBasGauche(elm["position"]) # On ajuste ses coordoonées
            self.fenetre_composant.append(bloc)
            self.blocs.append(bloc)
            index+=1


        #########################################################
        #                                                       #
        #                                                       #
        #                      Bouton                           #
        #                                                       #
        #                                                       #
        #########################################################

        index = 0
        nbbloc = len(self.blocs)
        for elm in self.composants["button"]:
            bouton = init_Obj("./Graphique/bouton.png", (27, 11)) # On crée une surface
            bouton = JeuBouton(None, bouton, bouton.get_rect(), self.ascenseurs[index], index, nbbloc) # On crée la Classe JeuBouton
            bouton.set_coordSupGauche(elm["position"]) # On ajuste ses coordoonées
            self.fenetre_composant.append(bouton)
            self.boutons.append(bouton)
            index+=1


        #########################################################
        #                                                       #
        #                                                       #
        #                       Gemme                           #
        #                                                       #
        #                                                       #
        #########################################################

        for gemme in self.composants["gemme"]:
            iden = gemme["id"]
            gem = init_Obj(f"./Graphique/gemme{iden+1}.png", (23,20)) # On crée une surface
            gem = Obj(gem, gem.get_rect(), "gemme", couleurs[iden]) # On crée la Classe Obj
            gem.set_coordSupGauche(gemme["position"]) # On ajuste ses coordoonées
            self.gemmes.append(gem)
        self.fenetre_composant = self.fenetre_composant + self.gemmes


        #########################################################
        #                                                       #
        #                                                       #
        #                     Textes                            #
        #                                                       #
        #                                                       #
        #########################################################

        position = [72, 100] # Ordonnée des textes
        # Affichage des informations gemmes au haut à droite
        for i in range(1,3):
            gem = init_Obj(f"./Graphique/gemme{i}.png", (23,20)) # On crée une surface
            gem = Obj(gem, gem.get_rect(), None) # On crée la Classe Obj
            gem.set_coordSupGauche((1092, position[i-1])) # On ajuste ses coordoonées
            self.fenetre_composant.append(gem)

            text = {
                "label": str(self.nbgemme[i-1]),
                "police": None,
                "taille": 30,
                "couleur": (153,202,60),
                "position": (1132, position[i-1]+10)
            }

            self.fenetre_texte_composant.append(text)

        text = {
                "label": "00:00",
                "police": None,
                "taille": 30,
                "couleur": (153,202,60),
                "position": (1120, 50)
            }

        self.fenetre_texte_composant.append(text)


    #####################################################################################################################
    #                                                                                                                   #
    #                                                                                                                   #
    #                                                AFFICHAGE                                                          #
    #                                                                                                                   #
    #                                                                                                                   #
    #####################################################################################################################


    def afficher_arriere_plan(self):
        """ Affiche l'arrière plan du niveau
        """
        affiche_surface(self.fenetre, "./Graphique/background.png", (1200, 675), (0, 0))
    
    
    def afficher_composants_jeu(self):
        """ On affiche tous les composants qui appartienent au jeu (personnages, liquides, blocs, ascenseurs, etc..)
        """
        for composants in self.fenetre_composant:
            self.fenetre.blit(composants.get_img(), composants.get_coordBordSupGauche())
        
        dessine_text(self.fenetre, self.fenetre_texte_composant)


    def afficher_composants(self):
        """ Affiche tous les éléments qu'ils soient amovibles ou non
        """

        # Si le jeu est en pause ou si le joueur a perdu
        if self.pause or self.stop : 
            self.afficher_menu_pause()
        else:

            # S'il n'a pas gagné
            if not self.gagne:

                # On affiche d'abord tous les éléments du décors
                self.afficher_arriere_plan()
                self.affiche_bouton_pause()
                self.afficher_composants_jeu()
                self.afficher_temps()


                # On gère les déplacements du ou des personnage(s)
                personnag = deplacement(self.personnages, self.partie.touches_pressees, self.sols)

                # On gère les collisions du ou des personnage/s qui est/sont en mouvement
                for perso in personnag:
                    self.gere_collision_personnage_mouvement(perso)

                # On gère les collisions qui ne dépendent pas du mouvement du personnage
                self.gere_collision()
                
            else:
                self.fin_de_partie()

    

    def afficher_menu_pause(self):
        """ Affiche le menu pause ou le menu quand l'utilisateur a perdu
        """
        self.partie.effacer_variables()

        # On crée le rectangle principal qui est au milieu de l'écran
        creer_rectangle_centrer(self.fenetre, 500, 300, (94,68,37))

        # On crée et affiche le texte "Partie en pause"
        dessine_text(
            self.fenetre,
            [{
                "label":"Partie en pause" if self.pause else "Perdu !",
                "police": None,
                "taille": 72,
                "couleur": (255,255,255),
                "position": (600, 287)
            }]
        )

        inf = {
                "rect": [
                    [ pygame.Rect(373, 365, 205, 44), pygame.Rect(613, 365, 224, 44)], (78,51,20)
                ],
                "textes": [
                    {
                        "label": "Recommencer",
                        "police": "Arial",
                        "taille": 36,
                        "couleur": (255, 255, 255),
                    },
                    {
                        "label": "Retour au menu",
                        "police": "Arial",
                        "taille": 36,
                        "couleur": (255, 255, 255),
                    }
                ],
                "action": [recommencer, retour_au_menu]
            }

        # Si il a cliqué sur pause, il peut alors reprendre sa progression
        # Sinon, il a perdu alors il n'est pas légal de reprendre !
        if self.pause:
            inf["rect"][0].append(pygame.Rect(519, 415, 162, 45))
            inf["textes"].append({"label": "Reprendre","police": "Arial","taille": 36,"couleur": (255, 255, 255),})
            inf["action"].append(reprendre)
    

        self.partie.boutons = dessine_bouton(self.fenetre, inf)
    

    def affiche_bouton_pause(self):
        """ Créer et affiche le bouton pause
        """
        # On crée une instance de la classe Bouton
        self.partie.boutons.append(Bouton(pygame.Rect(28, 40, 40, 40), "", pause, None))
        
        # On dessine les deux rectangles
        pygame.draw.rect(self.fenetre, (255, 255, 255), (28, 40, 15, 40))
        pygame.draw.rect(self.fenetre, (255, 255, 255), (53, 40, 15, 40))

    
    def afficher_temps(self):
        """ Affiche les informations de gemmes en haut à droite
        """

        temps = time() # Le temps actuel (sous forme de secondes écoulées depuis le 1er janvier 1970)

        temps_seconde = int(str(self.temps).split(".")[0]) # Le temps affiché en seconde

        # Si le temps en seconde a changé
        if temps_seconde != self.seconde:
            # On affiche la modification
            self.seconde = temps_seconde
            self.fenetre_texte_composant[2]["label"] = str(self.seconde//60).zfill(2) + ":" + str(self.seconde%60).zfill(2)
        
        # On actualise les variables de temps
        self.temps = temps - self.debut_niveau + self.temps
        self.debut_niveau = temps    
    

    #####################################################################################################################
    #                                                                                                                   #
    #                                                                                                                   #
    #                                               COLLISIONS                                                          #
    #                                                                                                                   #
    #                                                                                                                   #
    #####################################################################################################################


    def gere_collision_personnage_mouvement(self, personnage_en_mouvement):
        """ Appel les fonctions qui gèrent les collisions lorsqu'un personnage est en mouvement

        Argument :
            personnage_en_mouvement : type classes.personnage.Personnage => Le personnage en mouvement
        """
        self.gere_collision_liquide(personnage_en_mouvement)
        self.gere_collision_gemme(personnage_en_mouvement)
        self.gere_collision_portes(personnage_en_mouvement)
        self.gere_collision_bouton(personnage_en_mouvement)
        self.gere_collision_bloc()

    def gere_collision_liquide(self, personnage):
        """ Gère les collisons entre un liquide et un personnage

        Argument :
            personnage : type classes.personnage.Personnage => Le personnage en mouvement
        """
        
        
        personnage_en_mouvement_collision_pied = pygame.Rect(personnage.get_x()+12, personnage.get_rect().topleft[1], 16, 57) # Le rectangle de collision du personnage
        rect_liquide_collision = gere_collisions_rectangles(personnage_en_mouvement_collision_pied, self.liquides)
        
        # On vérifie s'il y a collision entre le personnage et un liquide et si la couleur du liquide n'est pas la même que celle du personnage
        if rect_liquide_collision and personnage.get_couleur() != rect_liquide_collision.get_couleur():
            # Si la condition est vérifiée la partie est perdue
            self.afficher_menu_pause()
            self.stop = True


    def gere_collision_bloc(self):
        """ Gère les collisions entre un bloc et un personnage
        """
        for bloc in self.blocs:
            bloc.gere_collision(self.personnages)


    def gere_collision_gemme(self, personnage):
        """ Gère les collisions entre une gemme et un personnage

        Argument :
            personnage : type classes.personnage.Personnage => Le personnage en mouvement    
        """
        rect_gemme_collision = gere_collisions_rectangles(personnage.get_rect(), self.gemmes)

        # On vérifie s'il y a collision entre une gemme et le personnage et si la couleur de la gemme est la même que celle du personnage
        if rect_gemme_collision and personnage.get_couleur() == rect_gemme_collision.get_couleur():
            # Si c'est le cas, la gemme est récupérée 

            # Ainsi, on l'enlève des composants à afficher
            self.gemmes.remove(rect_gemme_collision)
            self.fenetre_composant.remove(rect_gemme_collision) 

            # On retire une gemme en mémoire
            couleurs = ["vert", "violet"]
            perso_index = couleurs.index(personnage.get_couleur())
            self.nbgemme[perso_index]-=1
            # On retire une gemme à l'écran
            self.fenetre_texte_composant[perso_index]["label"] = str(int(self.fenetre_texte_composant[perso_index]["label"])-1)
        

    def gere_collision_bouton(self, personnage):
        """ Gère les collisions entre un bouton et un personnage

        Argument :
            personnage : type classes.personnage.Personnage => Le personnage en mouvement
        """
        personnage_en_mouvement_collision_pied = pygame.Rect(personnage.get_x()+12, personnage.get_rect().topleft[1], 16, 57)
        personnage_index = self.personnages.index(personnage)
        for bouton in self.boutons:

                if gere_collisions_rectangles(personnage_en_mouvement_collision_pied, [bouton]): # Si le bouton n'est pas déjà appuyé
                    bouton.set_etat(True, personnage_index)

                else: # Si le bouton n'est pas appuyé par le personnage
                    bouton.set_etat(False, personnage_index)

                # On vérifie les collisions entre un bloc et le bouton de la même manière que pour le personnage
                for bloc in self.blocs:
                    if gere_collisions_rectangles(bloc.get_rect(), [bouton]):
                        bouton.set_etat(True, bloc.identifiant)
                    else:
                        bouton.set_etat(False, bloc.identifiant)


    def gere_collision_portes(self, personnage):
        """ Gère les collisions entre une porte et un personnage

        Argument :
            personnage : type classes.personnage.Personnage => Le personnage en mouvement
        """ 
        victoire = 0
        for porte in self.portes:

            # Si la couleur du personnage correspond à la couleur de la porte
            if porte.get_couleur() == personnage.get_couleur():
                porte_collision = gere_collisions_rectangles(personnage, [porte])
                if porte_collision: # Si il y a collison, on change l'état de la porte
                    porte.changer_etat(1) 
                    victoire+=1
                else:
                    porte.changer_etat(0)
                
            elif porte.get_statut():
                victoire+=1
        
        # Les deux portes sont ouvertes si, et seulement si, victoire = 2
        if victoire == 2:
            self.fin_de_partie()



    def gere_collision(self):
        """ Gère les collisions et les évènements qui doivent être vérifiés à tout moment de la partie
        """

        # On vérifie si les boutons sont relâchés ou appuyés
        for bouton in self.boutons: 
            if bouton.get_etat_actuel():
                bouton.bouton_presse(self.personnages, self.blocs)
            else:
                bouton.bouton_relache(self.personnages, self.blocs)
        
        # On vérifie si tous les blocs sont bien sur le sol
        for bloc in self.blocs:
            # Si un bloc est en l'air, on le met dans le vide
            if not bloc.est_sur_sol():
                sol = bloc.sol_a_atteindre(self.sols, bloc.get_coordBordBasGauche()[1])
                bloc.aller_sol(sol)
        
        # On vérifie si les personnages sont bien sur le sol
        for personnage in self.personnages:
            # On les met dans le vide s'ils ne respetent pas cette condition
            if personnage.personnageSurSol():
                personnage.personnage_dans_vide(self.sols)
        
        # On vérifie si les portes sont ouvertes ou fermées
        for porte in self.portes:
            if porte.get_statut():
                porte.ouvrir(self.fenetre)
            else:
                porte.fermer(self.fenetre)


    #####################################################################################################################
    #                                                                                                                   #
    #                                                                                                                   #
    #                                                  AUTRES                                                           #
    #                                                                                                                   #
    #                                                                                                                   #
    #####################################################################################################################
    
    def fin_de_partie(self):
        """ Gère le cas où l'utilisateur remporte la partie
        """
        self.gagne = True
        self.partie.effacer_variables()

        # On crée le rectangle principal qui est au milieu de l'écran
        creer_rectangle_centrer(self.fenetre, 500, 300, (94,68,37))

        # On affiche les différents textes
        dessine_text(
            self.fenetre,
            [{
                "label": "Victoire !",
                "police": None,
                "taille": 72,
                "couleur": (255,255,255),
                "position": (600, 230)
            },
            {
                "label": "Temps",
                "police": None,
                "taille": 25,
                "couleur": (255,255,255),
                "position": (450, 300)
            },
            {
                "label": "Gemme",
                "police": None,
                "taille": 25,
                "couleur": (255,255,255),
                "position": (600, 300)
            },
            {
                "label": "Niveau",
                "police": None,
                "taille": 25,
                "couleur": (255,255,255),
                "position": (750, 300)
            },


            {
                "label": str(self.seconde//60).zfill(2) + ":" + str(self.seconde%60).zfill(2),
                "police": None,
                "taille": 25,
                "couleur": (0,255,0) if self.seconde < self.temps_fini else (255, 0, 0),
                "position": (450, 340)
            },
            {
                "label": str(self.nbgemme[0] + self.nbgemme[1]),
                "police": None,
                "taille": 25,
                "couleur": (0,255,0) if self.nbgemme[0] + self.nbgemme[1] == 0 else (255,0,0),
                "position": (600, 340)
            },
            {
                "label": "Oui",
                "police": None,
                "taille": 25,
                "couleur": (0,255,0),
                "position": (750, 340)
            },
             
             
            ]
        )


        # On crée le bouton cliquable
        inf = {
                "rect": [
                    [pygame.Rect(500, 400, 224, 44)], (78,51,20)
                ],
                "textes": [
                    {
                        "label": "Retour au menu",
                        "police": "Arial",
                        "taille": 36,
                        "couleur": (255, 255, 255),
                    }
               ],
               "action": [retour_au_menu]
            }

        self.partie.boutons = dessine_bouton(self.fenetre, inf)



    def enlever_composants(self):
        """ Enlève tous les composants des listes de niveau
        """
        self.personnages = [None, None]
        self.boutons = []
        self.ascenseurs = []
        self.liquides = []
        self.blocs = []
        self.fenetre_composant = []


def init_Obj(chemin, taille):
    """ Convertit une image en objet pygame.Surface

    Arguments :
        chemin: type Str => Le chemin d'accès relatif à l'image
        taille: type Tuple[Int] => La taille de l'image à l'écran

    sortie: type pygame.Surface
    """
    obj = pygame.image.load(chemin)            # On charge l'image
    obj = pygame.transform.scale(obj, taille)  # On l'adapte à la taille de l'écran
    return obj