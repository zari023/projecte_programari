grupos_cerca =  {
        "Fitness Club": {
            "nom": "Fitness Club",
            "categoria": "Salut",
            "subcategoria": "Exercici",
            "descripcio": "Un grup per a amants de l'exercici físic i el fitness.",
            "participants": [],
            "missatges": []
        },
        "Lectors Entusiastes": {
            "nom": "Lectors Entusiastes",
            "categoria": "Interessos",
            "subcategoria": "Literatura",
            "descripcio": "Un lloc per compartir llibres i recomanacions literàries.",
            "participants": [],
            "missatges": []
        },
        "Suport Emocional": {
            "nom": "Suport Emocional",
            "categoria": "Suport",
            "subcategoria": "Salut Mental",
            "descripcio": "Un espai per compartir experiències i donar suport emocional.",
            "participants": [],
            "missatges": []
        },
    }


from datetime import datetime
def fer_trucada(usuari):
    """Funcionalitat completa de trucades."""
    # Verificar si hi ha contactes
    contactes = usuari.xarxes_socials.get("contactes", {})
    if not contactes:
        print("No tens contactes. Primer afegeix contactes.")
        return

    print("\n--- Fer Trucada ---")
    print("Contactes:")
    llista_contactes = list(contactes.keys())
    for i, contacte in enumerate(llista_contactes, 1):
        print(f"{i}. {contacte}")
    
    try:
        seleccio = int(input("Selecciona un contacte per trucar: "))
        if 1 <= seleccio <= len(llista_contactes):
            contacte = llista_contactes[seleccio - 1]
            
            # Seleccionar tipus de trucada
            print("\nTipus de trucada:")
            print("1. Trucada de veu")
            print("2. Trucada de vídeo")
            tipus = input("Selecciona el tipus de trucada: ")
            tipus_text = "Veu" if tipus == "1" else "Vídeo"
            
            # Registrar trucada
            trucada = {
                "contacte": contacte,
                "tipus": tipus_text,
                "data": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            
            # Afegir a l'historial de trucades
            if "trucades" not in usuari.xarxes_socials:
                usuari.xarxes_socials["trucades"] = []
            usuari.xarxes_socials["trucades"].append(trucada)
            
            print(f"Trucada a {contacte} ({tipus_text}) registrada!")
        else:
            print("Selecció no vàlida.")
    except (ValueError, IndexError):
        print("Selecció no vàlida.")

def gestionar_grups(usuari):
    """Gestió avançada de grups amb exploració i funcionalitats millorades."""
    # Definició de categories de grups predeterminades
    categories_grups = {
        "Salut": ["Salut Mental", "Nutrició", "Exercici", "Malalties Cròniques"],
        "Interessos": ["Tecnologia", "Esports", "Arts", "Literatura", "Música"],
        "Suport": ["Famílies", "Pacients", "Cuidadors", "Adults Grans"]
    }

    while True:
        print("\n--- Gestió de Grups ---")
        print("1. Crear nou grup")
        print("2. Explorar grups")
        print("3. Els meus grups")
        print("4. Sortir")
        
        opcio = input("Selecciona una opció: ")
        
        if opcio == "1":
            # Crear nou grup
            print("\n--- Crear Nou Grup ---")
            print("Categories disponibles:")
            for categoria, subcategories in categories_grups.items():
                print(f"{categoria}: {', '.join(subcategories)}")
            
            categoria = input("Selecciona una categoria principal: ").lower()
            if categoria not in categories_grups:
                print("Categoria no vàlida.")
                continue
            
            subcategoria = input("Selecciona una subcategoria: ").lower()
            if subcategoria not in categories_grups[categoria]:
                print("Subcategoria no vàlida.")
                continue
            
            nom_grup = input("Introdueix un nom específic per al grup: ")
            descripcio = input("Introdueix una descripció del grup: ")
            
            # Verificar estructura de grups
            if "grups" not in usuari.xarxes_socials:
                usuari.xarxes_socials["grups"] = {}
            
            # Crear estructura del grup
            nou_grup = {
                "nom": nom_grup,
                "categoria": categoria,
                "subcategoria": subcategoria,
                "descripcio": descripcio,
                "participants": [usuari.nom],
                "missatges": []
            }
            
            usuari.xarxes_socials["grups"][nom_grup] = nou_grup
            print(f"Grup {nom_grup} creat amb èxit!")
        
        elif opcio == "2":
            # Explorar grups
            print("\n--- Explorar Grups ---")
            print("Filtres de cerca:")
            print("1. Per categoria")
            print("2. Per subcategoria")
            print("3. Paraula clau")
            
            filtre = input("Selecciona un mètode de cerca: ")
            
            grups_disponibles = []
            if filtre == "1":
                # Seleccionar categoria
                categories = set(grup["categoria"] for grup in grupos_cerca.values())
                categories = sorted(categories)  # Ordenar categories
                print("Categories disponibles:")
                for idx, categoria in enumerate(categories, 1):
                    print(f"{idx}. {categoria}")
                try:
                    seleccio_categoria = int(input("Selecciona una categoria: "))
                    if 1 <= seleccio_categoria <= len(categories):
                        categoria_cerca = categories[seleccio_categoria - 1]
                        grups_disponibles = [
                            grup for grup in grupos_cerca.values() 
                            if grup["categoria"] == categoria_cerca
                        ]
                except (ValueError, IndexError):
                    print("Selecció no vàlida.")
                    continue
            
            elif filtre == "2":
                # Seleccionar subcategoria
                subcategories = set(grup["subcategoria"] for grup in grupos_cerca.values())
                subcategories = sorted(subcategories)  # Ordenar subcategories
                print("Subcategories disponibles:")
                for idx, subcategoria in enumerate(subcategories, 1):
                    print(f"{idx}. {subcategoria}")
                try:
                    seleccio_subcategoria = int(input("Selecciona una subcategoria: "))
                    if 1 <= seleccio_subcategoria <= len(subcategories):
                        subcategoria_cerca = subcategories[seleccio_subcategoria - 1]
                        grups_disponibles = [
                            grup for grup in grupos_cerca.values() 
                            if grup["subcategoria"] == subcategoria_cerca
                        ]
                except (ValueError, IndexError):
                    print("Selecció no vàlida.")
                    continue
            
            elif filtre == "3":
                paraula_clau = input("Introdueix una paraula clau: ").lower()
                grups_disponibles = [
                    grup for grup in grupos_cerca.values() 
                    if paraula_clau in grup["nom"].lower() or paraula_clau in grup["descripcio"].lower()
                ]
            
            else:
                print("Filtre no vàlid.")
                continue
            
            # Mostrar grups disponibles
            if not grups_disponibles:
                print("No s'han trobat grups.")
            else:
                print("\nGrups disponibles:")
                for idx, grup in enumerate(grups_disponibles, 1):
                    print(f"{idx}. {grup['nom']} - {grup['categoria']}/{grup['subcategoria']}")
                    print(f"   Descripció: {grup['descripcio']}")
                
                try:
                    seleccio = int(input("Selecciona un grup per unir-te (0 per cancel·lar): "))
                    if 1 <= seleccio <= len(grups_disponibles):
                        grup_seleccionat = grups_disponibles[seleccio - 1]
                        
                        # Verificar si ja és participant
                        if "grups" not in usuari.xarxes_socials:
                            usuari.xarxes_socials["grups"] = {}
                        if usuari.nom in grup_seleccionat["participants"]:
                            print(f"Ja ets membre del grup {grup_seleccionat['nom']}.")
                        else:
                            grup_seleccionat["participants"].append(usuari.nom)
                            usuari.xarxes_socials["grups"][grup_seleccionat["nom"]] = grup_seleccionat
                            print(f"T'has unit al grup {grup_seleccionat['nom']}!")
                except (ValueError, IndexError):
                    print("Selecció no vàlida.")
        
        elif opcio == "3":
            # Els meus grups
            print("\n--- Els Meus Grups ---")
            if not usuari.xarxes_socials.get("grups"):
                print("No tens cap grup.")
                continue

            # Llistar els grups
            grups_disponibles = list(usuari.xarxes_socials["grups"].keys())
            print("\nGrups:")
            for idx, nom_grup in enumerate(grups_disponibles, 1):
                detalls_grup = usuari.xarxes_socials["grups"][nom_grup]
                print(f"{idx}. {nom_grup}")
            # Seleccionar un grup
            try:
                seleccio = int(input("Selecciona un grup pel número (0 per tornar enrere): "))
                if seleccio == 0:
                    continue  # Tornar al menú principal
                if 1 <= seleccio <= len(grups_disponibles):
                    nom_grup_seleccionat = grups_disponibles[seleccio - 1]
                    detalls_grup = usuari.xarxes_socials["grups"][nom_grup_seleccionat]
                else:
                    print("Selecció no vàlida.")
                    continue
            except ValueError:
                print("Entrada no vàlida. Torna-ho a provar.")
                continue

            # Mostrar opcions per al grup seleccionat
            while True:
                print(f"\n--- Opcions per al grup: {nom_grup_seleccionat} ---")
                print("1. Enviar missatge")
                print("2. Afegir participant")
                print("3. Sortir del grup")
                print("4. Tornar enrere")

                opcio_grup = input("Selecciona una acció: ")

                if opcio_grup == "1":
                    # Enviar missatge
                    missatge = input("Missatge: ")
                    detalls_grup["missatges"].append(f"{usuari.nom}: {missatge}")
                    print("Missatge enviat!")

                elif opcio_grup == "2":
                    # Afegir participant
                    contactes = usuari.xarxes_socials.get("contactes", {})
                    if not contactes:
                        print("No tens contactes. Primer afegeix contactes.")
                        return
                    contactes = list(usuari.xarxes_socials["contactes"].keys())
                    print("\nSelecciona un contacte per iniciar un xat:")
                
                    for i, contacte in enumerate(contactes, 1):
                        print(f"{i}. {contacte}")

                    try:
                        seleccio = int(input("Número de contacte: "))
                        if 1 <= seleccio <= len(contactes):
                            contacte = contactes[seleccio - 1]
                            if contacte not in detalls_grup["participants"]:
                                detalls_grup["participants"].append(contacte)
                                print(f"{contacte} afegit al grup.")
                            else:
                                print("Participant ja és al grup.")
                    except ValueError:
                        print("Entrada no vàlida. Si us plau, selecciona un número.")

                elif opcio_grup == "3":
                    # Sortir del grup
                    if usuari.nom in detalls_grup["participants"]:
                        detalls_grup["participants"].remove(usuari.nom)
                        del usuari.xarxes_socials["grups"][nom_grup_seleccionat]
                        print(f"Has sortit del grup {nom_grup_seleccionat}.")
                        break  # Sortir del menú del grup
                    else:
                        print("No ets membre d'aquest grup.")

                elif opcio_grup == "4":
                    break  # Tornar al menú principal

                else:
                    print("Opció no vàlida.")

                
        elif opcio == "4":
            break
        
        else:
            print("Opció no vàlida.")
