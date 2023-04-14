import pygame
from classes.bouton_fenetre import Bouton


#####################################################################################################################
#                                                                                                                   #
#                                                                                                                   #
#                                                  DESSIN                                                           #
#                                                                                                                   #
#                                                                                                                   #
#####################################################################################################################


def dessine_rects(fenetre, rects, couleur):
    """
    Dessine la liste des rectangles spécifiés.

    Arguments :
        fenetre: type pygame.Surface =>  La surface où les rectangles seront affichés
        rects: type List[pygame.Rect] => La liste des rectangles que l'on veut dessiner à l'écran.
        couleur: type tuple[Int] | List[tuple[Int]] => La liste des couleurs en tuple de couleurs (rouge, vert, bleu) des rectangles spécifiés ou une même couleur pour tous.
    
    Exemples :
        >>> rectangle = pygame.Rect(10, 10, 10, 10)
        >>> rectangle2 = pygame.Rect(10, 20, 30, 40)
        >>> dessine_rects(fen, rectangle, (255, 0, 0)) # Dessine un rectangle de couleur rouge 
        >>> dessine_rects(fen, [rectangle, rectangle2], (255, 0, 0)) # Dessine deux rectangles de couleur rouge
        >>> dessine_rects(fen, [rectangle, rectangle2], [(255, 0, 0), (0, 255, 0)]) # Dessine deux rectangles de couleur rouge pour le premier et bleu pour le deuxième
    """

    # On gère le cas où les rectangles ont tous la même couleur
    if type(couleur[0]) != tuple: 
        couleur = [couleur] * len(rects)

    # Affichage des rectangles
    for i in range(len(rects)):
        pygame.draw.rect(fenetre, couleur[i], rects[i])


def dessine_text(fenetre, inf):
    """ 
    Dessine la liste des textes spécifiés.

    Arguments :
        fenetre: type pygame.Surface => La surface où les rectangles seront affichés
        inf: type List[any] => La liste des paramètres qui définissent les textes. (clés: label, police, taille, couleur, position)
    
    Exemple d'argument inf :
        >>> inf = [
            {
                "label": "Un bouton",
                "police": None,
                "taille": 32,
                "couleur": (255, 0, 1),
                "position": (10, 54)
            },
            {
                "label": "Bouton 2",
                "police": "Arial,
                "taille": 64,
                "couleur": (255, 32, 1),
                "position": (10, 53)
            }
        ]
    """

    for texte_information in inf:
        # Informations du texte (police et label)
        police = pygame.font.SysFont(texte_information["police"], texte_information["taille"])
        texte = police.render(texte_information["label"], True, texte_information["couleur"])

        # Rectangle où le texte sera inséré
        texte_rec = texte.get_rect()
        texte_rec.center = (texte_information["position"])

        fenetre.blit(texte, texte_rec) # Affichage du texte à l'écran


def dessine_bouton(fenetre, inf):
    """ 
    Dessine les boutons spécifiés, (un bouton est constitué d'un texte et d'un rectangle) et instancies des objets boutons.
    On notera que la position des textes est calculé dans la fonction.

    Arguments :
        fenetre: type pygame.Surface => La surface où les rectangles seront affichés
        inf: tpye Dict => La liste des paramètres qui définissent les boutons. (clés: rect, textes, action)
    
    sortie: type List

    Exemple d'argument inf :
    >>> inf = {
                "rect": [
                    [play_button, quit_button], (78,51,20) 
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
                "action": [
                    jouer_bouton, 
                    quitter_bouton
                ]    
            }

    """

    liste_bouton = []

    # On dessine d'abord les rectangles à l'écran
    rectangles = inf["rect"][0]
    dessine_rects(fenetre, rectangles, inf["rect"][1])

    # On gère les boutons qui ont un label
    if "textes" in inf.keys():
        # On calcule la position des textes pour qu'ils soient centrés dans le rectangle
        for i in range(len(rectangles)):
            rect = rectangles[i]
        
            # Calcul de la position
            inf["textes"][i]["position"] = (rect.width//2 + rect.x, rect.height//2 + rect.y)

            # Ajout du bouton dans la liste
            liste_bouton.append(Bouton(rect, inf["textes"][i]["label"], inf["action"][i], None))

        dessine_text(fenetre, inf["textes"])
    else:

        # Les boutons n'ont pas de label, on crée donc un bouton SANS label
        for i in range(len(rectangles)):
            rect = rectangles[i]
            liste_bouton.append(Bouton(rect, "", inf["action"][i], i))

    return liste_bouton


#####################################################################################################################
#                                                                                                                   #
#                                                                                                                   #
#                                                CREATION                                                           #
#                                                                                                                   #
#                                                                                                                   #
#####################################################################################################################


def creer_rectangle_centrer(fen, largueur, hauteur, couleur):
    """ Créer un rectangle de taille défini dans les paramètres qui est centré à l'écran de manière automatique

    Arguments :
        fen: type pygame.Surface => La Surface où le rectangle sera inséré
        largueur: type Int
        hauteur: type Int
        couleur: type Tuple[Int] => La couleur en tuple de couleurs (rouge, vert, bleu) du rectangle

    Exemple:
        >>> creer_rectangle_centrer(pygame.display.set_mode((1200, 675)), 100, 100, (255, 255, 255)) # Affiche un rectangle de 100px par 100px de couleur blanche 
    """

    # Calcul des coordonnées du centre de l'écran
    center_x = fen.get_width() / 2
    center_y = fen.get_height() / 2

    # Calcul des coordonnées du coin supérieur gauche du rectangle
    rect_x = center_x - (largueur / 2)
    rect_y = center_y - (hauteur / 2)

    # Dessin du rectangle
    rect = pygame.Rect(rect_x, rect_y, largueur, hauteur)
    pygame.draw.rect(fen, couleur, rect)



def affiche_surface(fen, chemin, taille, coord):
    """ Affiche un élément à l'écran selon des paramètres définis

    Arguments :
        fen: type pygame.Surface => La fenêtre initialisé
        chemin: type Str  => Le chemin relatif pour accéder au fichier
        taille: type Tuple[Int] => La taille de l'image
        coord:  type Tuple[Int]  => Les coordonnées de l'image

    sortie : pygame.Surface => Renvoie la surface créée par la fonction 
    """

    image = pygame.image.load(chemin).convert()     # On importe l'image d'arrière plan
    image = pygame.transform.scale(image, taille)   # On met l'arrière plan à la taille de l'écran
    fen.blit(image, coord)                          # On affiche à l'écran la surface selon ses coordonnées
    return image