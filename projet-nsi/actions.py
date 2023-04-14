def jouer_bouton(partie, bouton):
    return partie.affiche_menu_niveau

def quitter_bouton(partie, bouton):
    partie.joueur_veut_jouer = False
    return partie.affiche_menu_principal

def test_bouton(partie, bouton):
    partie.niveau = partie.creer_classe_niveau(bouton.get_id())
    return partie.afficher_un_niveau

def pause(partie, bouton):
    partie.niveau.pause = True
    return partie.afficher_un_niveau

def recommencer(partie, bouton):
    partie.niveau = partie.creer_classe_niveau(partie.niveau.get_id())
    return partie.afficher_un_niveau

def retour_au_menu(partie, bouton):
    return partie.affiche_menu_principal

def reprendre(partie, bouton):
    partie.niveau.pause = False
    return partie.afficher_un_niveau