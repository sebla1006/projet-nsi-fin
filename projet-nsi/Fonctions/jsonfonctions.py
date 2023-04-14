import json

def get_json_file(fichier):
    """ Renvoie le contenu d'un fichier d'extension JSON

    Argument:
        fichier : type Str => Le chemin d'accès relatif
    
    sortie: type Dict[str, any]
    """
    with open(fichier, 'r') as file:
        data = json.load(file)
    
    return data