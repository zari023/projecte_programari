def afegir_contacte(usuari):
# Afegir contacte
        nom = input("Introdueix el nom del contacte: ")
        telefon = input("Introdueix el telèfon (opcional): ")
        correu = input("Introdueix el correu (opcional): ")
        
        # Inicialitzar el diccionari de contactes si no existeix
        if "contactes" not in usuari.xarxes_socials:
            usuari.xarxes_socials["contactes"] = {}
        
        # Afegir contacte
        usuari.xarxes_socials["contactes"][nom] = {
            "telefon": telefon,
            "correu": correu,
            "xats": []  # Historial de xats amb aquest contacte
        }
        print(f"Contacte {nom} afegit!")
        
def veure_xats(usuari):
    """Mostra els xats de l'usuari."""
    print("\n--- Els teus Xats ---")
    if not usuari.xarxes_socials["xats"]:
        print("No tens cap xat.")
        while True:
            res = input("Vols afegir un contacte?(Sí/No)").lower() #Falta restringir opció
            if res == "si":
                afegir_contacte(usuari)
            if res == "no":
                break
            print("Opció incorrecte")
        

    for contacte, missatges in usuari.xarxes_socials["xats"].items():
        print(f"\nXat amb {contacte}:")
        for missatge in missatges:
            print(missatge)

    # Opció per enviar nou missatge
    while True:
        print("\n1. Enviar missatge")
        print("2. Tornar")
        opcio = input("Selecciona una opció: ")

        if opcio == "1":
            # Seleccionar contacte
            contactes = list(usuari.xarxes_socials["xats"].keys()) if usuari.xarxes_socials["xats"] else []
            contactes.append("Nou contacte")
            
            print("\nSelecciona un contacte:")
            for i, contacte in enumerate(contactes, 1):
                print(f"{i}. {contacte}")
            
            try:
                seleccio = int(input("Número de contacte: "))
                if 1 <= seleccio <= len(contactes):
                    contacte = contactes[seleccio - 1]
                    
                    if contacte == "Nou contacte":
                        contacte = input("Introdueix el nom del contacte: ")
                        if contacte not in usuari.xarxes_socials["xats"]:
                            usuari.xarxes_socials["xats"][contacte] = []
                    
                    missatge = input(f"Missatge per {contacte}: ")
                    usuari.xarxes_socials["xats"][contacte].append(f"Tu: {missatge}")
                    print("Missatge enviat!")
                else:
                    print("Selecció no vàlida.")
            except (ValueError, IndexError):
                print("Selecció no vàlida.")
        
        elif opcio == "2":
            break
        else:
            print("Opció no vàlida.")

def veure_trucades(usuari):
    """Mostra l'historial de trucades de l'usuari."""
    print("\n--- Historial de Trucades ---")
    if not usuari.xarxes_socials["trucades"]:
        print("No hi ha cap registre de trucades.")
        return

    for trucada in usuari.xarxes_socials["trucades"]:
        print(trucada)

    # Opció per fer una nova trucada
    while True:
        print("\n1. Fer nova trucada")
        print("2. Tornar")
        opcio = input("Selecciona una opció: ")

        if opcio == "1":
            contacte = input("Introdueix el nom del contacte: ")
            tipus_trucada = input("Tipus de trucada (veu/video): ")
            durada = input("Durada de la trucada (minuts): ")
            
            nova_trucada = f"Trucada a {contacte} - Tipus: {tipus_trucada}, Durada: {durada} minuts"
            usuari.xarxes_socials["trucades"].append(nova_trucada)
            print("Trucada registrada!")
        
        elif opcio == "2":
            break
        else:
            print("Opció no vàlida.")

def crear_grup(usuari, nom_grup):
    """Crear un nou grup de xat."""
    if nom_grup in usuari.xarxes_socials["grups"]:
        print(f"El grup {nom_grup} ja existeix.")
        return

    usuari.xarxes_socials["grups"][nom_grup] = {
        "participants": [usuari.nom],  # L'usuari és sempre el primer participant
        "missatges": []
    }
    print(f"Grup {nom_grup} creat!")

def afegir_participant_grup(usuari, nom_grup, participant):
    """Afegir un participant a un grup."""
    if nom_grup not in usuari.xarxes_socials["grups"]:
        print(f"El grup {nom_grup} no existeix.")
        return

    if participant in usuari.xarxes_socials["grups"][nom_grup]["participants"]:
        print(f"{participant} ja és al grup.")
        return

    usuari.xarxes_socials["grups"][nom_grup]["participants"].append(participant)
    print(f"{participant} afegit al grup {nom_grup}!")

def enviar_missatge_grup(usuari, nom_grup, missatge):
    """Enviar un missatge a un grup."""
    if nom_grup not in usuari.xarxes_socials["grups"]:
        print(f"El grup {nom_grup} no existeix.")
        return

    usuari.xarxes_socials["grups"][nom_grup]["missatges"].append(f"{usuari.nom}: {missatge}")
    print(f"Missatge enviat al grup {nom_grup}!")
