def gere_collisions_souris(souris_coord, boutons):
    """
    Renvoie le bouton où la souris est situé (False si la souris n'est sur aucun bouton). 

    Arguments :
        souris_coord: type Tuple[Int] => Les coordonnées de la souris
        boutons: type List[classes.bouton.Bouton] => Les boutons dont on veut vérifier la collision
    
    sortie: type Bool | pygame.Rect

    Exemples :
        >>> gere_collisions_souris( (100, 100), [Bouton(pygame.Rect(50, 50, 100, 100), "Jouer")] )
        Bouton(pygame.Rect(50, 50, 100, 100), "Jouer"))
        >>> gere_collisions_souris( (100, 100), [Bouton(pygame.Rect(120, 120, 100, 100)), "Jouer"])
        False
    """

    for bouton in boutons:
        # Si collision entre le bouton et la souris
        if bouton.get_rect().collidepoint(souris_coord):
            return bouton
        
    return False

def gere_collisions_rectangles(rectangle, rectangles):
    """ Vérifie si un rectangle est en collision avec un rectangle de la liste de rectangle passée en paramètre.

    Arguments:
        rectangle : type pygame.Rect => Le rectangle qui sera analysé avec tous les autres rectangles
        rectangles : type List[Pygame.Rect] => La liste de rectangle où tous les objets seront comparés avec l'objet rectangle

    sortie: type Bool | pygame.Rect => False si pas de collision, sinon le rectangle de la liste avec lequel le rectangle est en collision
    """

    for rect in rectangles:
        # Collision entre un rectangle (rect) et le rectangle (rectangle)
        if rect.get_rect().colliderect(rectangle):
            return rect
    
    return False