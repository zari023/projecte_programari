import re
from datetime import datetime
import random
from classes import *
import json

def generar_id_usuari(usuaris):
    while True:
        idd = random.randint(1000, 9999)
        if not any(usuari.get_id == idd for usuari in usuaris):
            return idd

def generar_id_cita():
    with open("cites.json", "r", encoding="utf-8") as file:
        citas = json.load(file)
    ids_existents = {cita["idVisita"] for cita in citas}
    while True:
        nou = random.randint(10000, 99999)
        if nou not in ids_existents:
            return nou

def carregar_metges(file_path):
    metges = []
    with open(file_path, mode='r', encoding='utf-8') as file:
        dades = json.load(file)
        for row in dades:
            metge = Metge(
                DNI=row['DNI'],
                nom=row['nom'],
                cognom1=row['cognom1'],
                cognom2=row['cognom2'],
                telefon=row['telefon'],
                hospital=row['hospital'],
                numColegiat=row['numColegiat'],
                especialitat=row['especialitat'],
                disponibilitat=[]
            )
            metges.append(metge)
    return metges

def carregar_disponibilitat(nom_arxiu, llista_metges):
    try:
        with open(nom_arxiu, 'r', encoding='utf-8') as arxiu:
            dades = json.load(arxiu)
        
        # Assignar disponibilitat als metges corresponents
        for metge_dades in dades:
            dni = metge_dades["dniMetge"]
            disponibilitat = metge_dades.get("disponibilitat", [])
            
            # Buscar metge amb el mateix dni
            for metge in llista_metges:
                if metge.get_DNI == dni:
                    metge.set_disponibilitat(disponibilitat)
                    break

        print("Disponibilitat carregada correctament.")
    except FileNotFoundError:
        print(f"Error: No s'ha trobat l'arxiu {nom_arxiu}.")
    except json.JSONDecodeError:
        print("Error: L'arxiu no té un format JSON vàlid.")

def carregar_dades_mediques(ruta_json, id_usuari):
    try:
        with open(ruta_json, 'r', encoding='utf-8') as file:
            dades = json.load(file)
        # Filtrar dades per ID_Usuari
        for row in dades:
            if int(row["ID_Usuari"]) == int(id_usuari):
                return DadesMediques(row["ID_Usuari"], row['Malalties'], row["Medicacions"], row["Altura"], row["Pes"], row["Alergies"])
            
        return DadesMediques(id_usuari)  
        # Retorna None si no es troben dades per aquest usuari
        return None
    except FileNotFoundError:
        print(f"Error: No s'ha trobat el fitxer {ruta_json}.")
        return None
    except json.JSONDecodeError:
        print("Error: Format JSON invàlid.")
        return None
    
def carregar_xarxes(idUsuari, nomUsuari):
    xarxes = []
    xarxa = XarxesSocials(idUsuari, nomUsuari)
    with open('xarxes.json', mode='r', encoding='utf-8') as file:
        dades = json.load(file)
        for row in dades:
            if str(row['idUsuari']) == str(idUsuari):
                xarxa = XarxesSocials(row['idUsuari'], nomUsuari)
                xarxa.contactes = row.get('contactes', {})
                xarxa.xats = row.get('xats', {})
                xarxa.trucades = row.get('trucades', [])
                xarxa.grups = row.get('grups', {})
                xarxes.append(xarxa)
    return xarxa

def carregar_cites(file_path, idUsuari):
    cites = []
    with open(file_path, mode='r', encoding='utf-8') as file:
        dades = json.load(file)
        for row in dades:
            print(str(row['idUsuari']) == str(idUsuari))
            if str(row['idUsuari']) == str(idUsuari):
                cites.append(Cita(
                    idVisita=row['idVisita'],
                    data=row['data'],
                    tipusVisita=row['tipusVisita'],
                    prescripcions=row['prescripcions'],
                    idUsuari=row['idUsuari'],
                    DNI_metge=row['DNI_metge'],
                    cognomMetge=row['cognomMetge']
                ))
    return cites

def carregar_usuaris(file_path, metges):
    usuaris = []
    with open(file_path, mode='r', encoding='utf-8') as file:
        dades = json.load(file)
        for row in dades:
            usuari = Usuari(
                id=row['ID'],
                telefon=row['Telefon'],
                sexe=row['Sexe'],
                nom=row['Nom'],
                cognom1=row['Cognom1'],
                cognom2=row['Cognom2'],
                dia=row['Dia'],
                mes=row['Mes'],
                anyy=row['Any'],
                correu=row['Correu'],
                password=row['Password'],
                registre_medic_complet=bool(int(row['Registre_Medic'])),
                dades_mediques = {},
                notificacions = {},
                monitoratge = metges[int(row['ID'])%len(metges)],
                xarxes_socials = {}
            )
            usuaris.append(usuari)
    return usuaris

def guardar_cites(cita):
    file_path = 'cites.json'
    try:
        # Leer el contenido actual del archivo
        current_data = []
        with open(file_path, 'r', encoding='utf-8') as file:
            current_data = json.load(file)
        cita_dict = cita.to_dict()
        for i, existing_cita in enumerate(current_data):
            if existing_cita.get("idVisita") == cita_dict["idVisita"]:
                current_data[i] = cita_dict  # Actualizar cita existente
        else:
            current_data.append(cita_dict)  # Añadir nueva cita si no existe

        # Escribir los datos actualizados en el archivo
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(current_data, file, ensure_ascii=False, indent=4)

        print(f"Dades guardades correctament a {file_path}.")

    except Exception as e:
        print(f"Error al guardar l'arxiu {file_path}: {e}")

def tipus_usuari():
    opciones = {1: "Persona Gran", 2: "Familiar", 3: "Amic", 4: "Personal Sanitari", 5: "Admin"}
    while True:
        print("\nSelecciona el tipus d'usuari:")
        for key, value in opciones.items():
            print(f"{key}. {value}")
        try:
            seleccion = int(input("Introduïu el número corresponent: "))
            if seleccion in opciones:
                es_persona_gran = (seleccion == 1)
                return es_persona_gran, seleccion
            else:
                print("Valor incorrecte. Si us plau, selecciona un número del 1 al 5.")
        except ValueError:
            print("Entrada invàlida. Si us plau, introdueix un número.")

def actualizar_disponibilidad(file_path, dni_metge, fecha_seleccionada):
    try:
        # Leer el archivo de disponibilidad
        with open(file_path, 'r', encoding='utf-8') as file:
            disponibilitat_data = json.load(file)

        # Buscar al médico y actualizar la disponibilidad
        for medico in disponibilitat_data:
            if medico["dniMetge"] == dni_metge:
                if fecha_seleccionada in medico["disponibilitat"]:
                    medico["disponibilitat"].remove(fecha_seleccionada)
                    print(f"Data {fecha_seleccionada} eliminada de la disponibilitat del Dr. {dni_metge}")
                else:
                    print(f"Error: La data {fecha_seleccionada} no es troba disponible.")
                break
        else:
            print(f"Error: No existeix cap metge amb DNI {dni_metge}.")

        # Escribir los datos actualizados de nuevo en el archivo
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(disponibilitat_data, file, ensure_ascii=False, indent=4)

        print("Disponibilitat actualitzada correctament.")
    except Exception as e:
        print(f"Error al actualitzar la disponibilitat: {e}")

def editar_altura(usuari):
    while True:
        try:
            nova_altura = float(input("Introdueix nova altura (en cm): "))
            if 50 <= nova_altura <= 320:  # Rang raonable per a l'alçada en cm
                usuari.get_dades_mediques.set_altura(nova_altura)
                print("Altura actualitzada.")
                break
            else:
                print("L'alçada ha d'estar entre 50 i 320 cm.")
        except ValueError:
            print("Si us plau, introdueix un valor vàlid per a l'alçada.")

def editar_pes(usuari):
    """Función para editar el peso de un usuario."""
    while True:
        try:
            nou_pes = float(input("Introdueix nou pes (en kg): "))
            if 10 <= nou_pes <= 300:  # Rang raonable per al pes en kg
                usuari.get_dades_mediques.set_pes(nou_pes)
                print("Pes actualitzat.")
                break
            else:
                print("El pes ha d'estar entre 10 i 300 kg.")
        except ValueError:
            print("Si us plau, introdueix un valor vàlid per al pes.")

def guardar_usuari(file_path, usuari):
    """
    Añade o actualiza un usuario en el archivo JSON.
    
    :param file_path: Ruta del archivo JSON donde se guardarán los datos.
    :param usuari: Objeto con los datos del usuario a guardar.
    """
    # Leer los datos existentes en el archivo (o inicializar una lista vacía si el archivo no existe)
    try:
        with open(file_path, mode='r', encoding='utf-8') as file:
            dades = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        dades = []

    # Crear el nuevo usuario en el formato JSON especificado
    nou_usuari = {
        "ID": int(usuari.get_id),
        "Telefon": list(usuari.get_telefon),
        "Sexe": str(usuari.get_sexe),
        "Nom": str(usuari.get_nom),
        "Cognom1": str(usuari.get_cognom1),
        "Cognom2": str(usuari.get_cognom2),
        "Dia": int(usuari.get_dia),
        "Mes": str(usuari.get_mes),
        "Any": int(usuari.get_anyy),
        "Correu": str(usuari.get_correu),
        "Password": str(usuari.get_password),
        "Registre_Medic": int(usuari.get_registre_medic_complet)
    }

    # Buscar si el usuario ya existe por su ID
    user_exists = False
    for i, existing_user in enumerate(dades):
        if existing_user["ID"] == nou_usuari["ID"]:
            # Si el usuario ya existe, se actualizan los datos
            dades[i] = nou_usuari
            print(dades[i], nou_usuari)
            user_exists = True
            break

    if not user_exists:
        # Si el usuario no existe, se añade al final
        dades.append(nou_usuari)

    # Guardar los datos actualizados en el archivo JSON
    with open(file_path, mode='w', encoding='utf-8') as file:
        json.dump(dades, file, indent=4, ensure_ascii=False)

def guardar_dades_mediques(id, dades_med):
    try:
        with open("dades_mediques.json", mode='r', encoding='utf-8') as file:
            dades = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        dades = []

    # Crear el nuevo objeto con los datos médicos en el formato JSON
    nou_dades_med = {
        "ID_Usuari": int(id),
        "Malalties": list(dades_med.get_malalties),
        "Medicacions": list(dades_med.get_medicacions),
        "Altura": int(dades_med.get_altura),
        "Pes": int(dades_med.get_pes),
        "Alergies": list(dades_med.get_alergies)
    }

    # Buscar si los datos médicos ya existen para el usuario por su ID
    dades_med_exists = False
    for i, existing_dades_med in enumerate(dades):
        if existing_dades_med["ID_Usuari"] == nou_dades_med["ID_Usuari"]:
            # Si los datos médicos ya existen para el usuario, se actualizan los datos
            dades[i] = nou_dades_med
            dades_med_exists = True
            break

    if not dades_med_exists:
        # Si los datos médicos no existen, se añade al final
        dades.append(nou_dades_med)

    # Guardar los datos actualizados en el archivo JSON
    with open("dades_mediques.json", mode='w', encoding='utf-8') as file:
        json.dump(dades, file, indent=4, ensure_ascii=False)

def guardar_xarxes(id, xarxa):
    try:
        with open("xarxes.json", mode='r', encoding='utf-8') as file:
            dades = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        dades = []

    # Crear el nuevo objeto en el formato JSON especificado
    nou_xarxa = {
        "idUsuari": int(id),
        "contactes": dict(xarxa.contactes),
        "xats": dict(xarxa.xats),
        "trucades": list(xarxa.trucades),
        "grups": dict(xarxa.grups)
    }

    # Buscar si la red social ya existe para el usuario por su ID
    xarxa_exists = False
    for i, existing_xarxa in enumerate(dades):
        if existing_xarxa["idUsuari"] == nou_xarxa["idUsuari"]:
            # Si la red social ya existe para el usuario, se actualizan los datos
            dades[i] = nou_xarxa
            print("Red social actualizada:", dades[i])
            xarxa_exists = True
            break

    if not xarxa_exists:
        # Si la red social no existe, se añade al final
        dades.append(nou_xarxa)

    # Guardar los datos actualizados en el archivo JSON
    with open("xarxes.json", mode='w', encoding='utf-8') as file:
        json.dump(dades, file, indent=4, ensure_ascii=False)
        
def introduir_medicaments():
    medicaments = []  

    while True:
        # Demanem el nom del medicament
        nom = input("Introdueix el nom del medicament (o 'fi' per acabar): ").strip()

        if nom.lower() == 'fi':
            break  # Si l'usuari escriu 'fi', acabem el bucle

        # Demanem la quantitat/dosi
        quantitat = input(f"Introdueix la quantitat/dosi de {nom}: ").strip()

        # Comprovem que la dosi no estigui buida
        if not quantitat:
            print("La dosi no pot estar buida. Prova-ho de nou.")
            continue  # Si no s'introdueix una dosi, continuem amb el bucle

        # Guardem el medicament com una tupla (nom, quantitat)
        medicaments.append((nom, quantitat))

    return medicaments

def introduir_malalties():
    malalties = []  

    while True:
        # Demanem el nom del medicament
        nom = input("Introdueix el nom de la malaltia (o 'fi' per acabar): ").strip()

        if nom.lower() == 'fi':
            break  # Si l'usuari escriu 'fi', acabem el bucle

        malalties.append(nom)

    return malalties

def gestio_dades_mediques(usuari):
    while True:
        print("\n--- Dades Mèdiques ---")
        print("1. Visualitzar Dades Mèdiques")
        print("2. Editar Dades Mèdiques")
        print("3. Tornar enrrera")
        
        opcio = input("Selecciona una opció: ")
        
        if opcio == "1":
            # Visualitzar dades mèdiques
            print(usuari.get_dades_mediques)
        
        elif opcio == "2":
            # Editar dades mèdiques
            while True:
                print("\nQuè vols editar?")
                print("1. Malalties")
                print("2. Medicacions")
                print("3. Altura")
                print("4. Pes")
                print("5. Al·lèrgies")
                print("6. Tornar")
                
                subOpcio = input("Selecciona una opció: ")
                
                if subOpcio == "1":
                    # Editar malalties
                    print("Malalties actuals:", usuari.get_dades_mediques.get_malalties)
                    malalties = introduir_malalties()
                    usuari.get_dades_mediques.set_malalties(malalties)
                    print("Mlalaties actualitzades.")

                elif subOpcio == "2":
                    # Editar medicacions
                    #POTSER ESTARIA GUAY DONAR OPCIÓ PER AFEGIR MEDICACIONS
                    print("Medicacions actuals:", usuari.get_dades_mediques.get_medicacions)
                    medicacions = introduir_medicaments()
                    usuari.get_dades_mediques.set_medicacions(medicacions)
                    print("Medicacions actualitzades.")
                
                elif subOpcio == "3":
                    editar_altura(usuari)
                elif subOpcio == "4":
                    editar_pes(usuari)
                elif subOpcio == "5":
                    # Editar al·lèrgies
                    print("Al·lèrgies actuals:", usuari.get_dades_mediques.get_alergies)
                    noves_alergies = input("Introdueix noves al·lèrgies (separades per ;): ")
                    alergies = noves_alergies.split(';')
                    usuari.get_dades_mediques.set_alergies(alergies)
                    print("Al·lèrgies actualitzades.")
                
                elif subOpcio == "6":
                    break
                
                else:
                    print("Opció no vàlida. Si us plau, tria una opció del menú.")
        
        elif opcio == "3":
            break
        
        else:
            print("Opció no vàlida. Si us plau, tria una opció del menú.")
    guardar_dades_mediques(usuari.get_id, usuari.get_dades_mediques)

def validar_correu(correu):
    return re.match(r"[^@]+@[^@]+\.[^@]+", correu) is not None

def validar_data(dia, mes, anyy):
    mesos_valids = ["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"]
    dies_per_mes = {
        "jan": 31, "feb": 28, "mar": 31, "apr": 30, "may": 31, "jun": 30,
        "jul": 31, "aug": 31, "sep": 30, "oct": 31, "nov": 30, "dec": 31
    }
    try:
        dia = int(dia)
        anyy = int(anyy)
        mes = mes.lower()
        if mes not in mesos_valids:
            raise ValueError("Mes no válido.")
        if mes == "feb" and ((anyy % 4 == 0 and anyy % 100 != 0) or (anyy % 400 == 0)):
            dies_per_mes["feb"] = 29
        if dia < 1 or dia > dies_per_mes[mes]:
            raise ValueError("Día no válido para el mes especificado.")
        return True
    except ValueError:
        return False

def validar_telefon(tel):
    if len(tel) != 9 or type(tel)!=int:
        print("Número de telèfon incorrecte")
        return False
    return True

def introduir_telefon():
    while True:
        tel = input("Introdueix el teu telèfon:")
        res = validar_telefon(tel)
        if res:
            return tel

def introduir_sexe():
    while True:
        res = input("Introdueix el nou sexe (home/dona): ").lower()
        if res == "home" or res == "dona":
            return res
        
def mostrar_notificacions(usuari):
    print("\n--- Notificacions ---")
    for categoria, notificacions in usuari.get_notificacions.items():
        if notificacions:
            print(f"{categoria.capitalize()}:")
            for notificacio in notificacions:
                print(f"  - {notificacio}")
        else:
            print(f"{categoria.capitalize()}: No hi ha notificacions.")

def completar_registre_medic(usuari, medics):
    print("\n--- Completar el Registre Mèdic ---")
    
    malalties = input("Introdueix les teves malalties prèvies (separades per comes, o pressiona Enter si no tens cap): ")
    malalties_llista = malalties.split(",") if malalties != "" else []
    usuari.get_dades_mediques.set_malalties(malalties_llista)
    
    # Al·lèrgies
    al_lergies = input("Introdueix les teves al·lèrgies (separades per comes, o pressiona Enter si no tens cap): ")
    alergies_llista = al_lergies.split(",") if al_lergies else []
    usuari.get_dades_mediques.set_alergies(alergies_llista)
    
    editar_altura(usuari)
    editar_pes(usuari)

    
    # Medicació
    medicacions = []
    while True:
        medicacio = input("Introdueix el nom de la medicació que estàs prenent (o pressiona Enter per acabar): ")
        if medicacio == "":
            break
        
        dosi = input(f"Introdueix la dosi de {medicacio}: ")
        medicacions.append((medicacio, dosi))
    
    # Actualitzar medicacions a la classe DadesMediques
    usuari.get_dades_mediques.set_medicacions(tuple(medicacions))
    demanar_cita(usuari, medics, True)
    guardar_usuari('usuaris.json', usuari)

def demanar_cita(usuari, medics, registre=False):
    print("\n--- Completar registre mèdic ---")
    print("Metges disponibles:")
    for i, medic in enumerate(medics):
        print(f"{i + 1}. Dr {medic.get_cognom1} - Especialitat: {medic.get_especialitat}")
    
    # Selección del médico
    while True:
        try:
            seleccion = int(input("Seleccioni un metge pel seu número: ")) - 1
            if 0 <= seleccion < len(medics):
                medico_seleccionado = medics[seleccion]
                break
            else:
                print("Valor invàlid")
        except ValueError:
            print("Valor invàlid")
    
    # Mostrar las fechas y horas disponibles del médico
    if not medico_seleccionado.get_disponibilitat:
        print(f"El metge {medico_seleccionado.get_nom} no te dates disponibles.")
        return
    
    print(f"\nDates disponibles per {medico_seleccionado.get_nom}:")
    for i, fecha in enumerate(medico_seleccionado.get_disponibilitat):
        print(f"{i + 1}. {fecha}")
    
    # Selección de la fecha
    while True:
        try:
            fecha_seleccionada = int(input("Seleccioni una data pel seu número: ")) - 1
            if 0 <= fecha_seleccionada < len(medico_seleccionado.get_disponibilitat):
                disp = medico_seleccionado.get_disponibilitat
                fecha_elegida = disp.pop(fecha_seleccionada) 
                medico_seleccionado.set_disponibilitat(disp)
                print(f"Ha seleccionat la data i hora: {fecha_elegida}")
                break
            else:
                print("Valor invàlid")
        except ValueError:
            print("Valor invàlid")
    
    # Llamar a la función para actualizar la disponibilidad en el archivo JSON
    actualizar_disponibilidad("disponibilitat.json", medico_seleccionado.get_DNI, fecha_elegida)

    # Selección del tipo de visita
    while True:
        tipus_visita = input("\nSelecciona el tipus de visita (online/presencial): ").lower()
        if tipus_visita == "online" or tipus_visita == "presencial":
            break
        print("Opció incorrecte")
    
    # Crear la cita y añadir notificación al usuario
    cita = Cita(generar_id_cita(), fecha_elegida, tipus_visita, "", usuari.get_id, medico_seleccionado.get_DNI, medico_seleccionado.get_cognom1)
    notis = usuari.get_notificacions
    notis["cites"].append(cita)
    usuari.set_notificacions(notis)
    if registre:
        usuari.set_monitoratge(medico_seleccionado)
    guardar_cites(cita)
    print("Registre mèdic completat i cita concertada!")
    return cita

def monitoratge(usuari, actiu):
    print("\n--- Configuració de Monitoratge ---")
    if not usuari.get_registre_medic_complet:
        print("No tens el registre mèdic completat. No es pot monitoritzar fins que no ho facis.")
    else:
        while True:
            if not actiu:
                print("El monitoratge està desactivat")
                print("1. Activar monitoratge")
                print("2. Tornar")
                opcio_monitoratge = input("Selecciona una opció: ")
                if opcio_monitoratge == "1":
                    actiu = True
                elif opcio_monitoratge == "2":
                    return
                else:
                    print("Opció no disponible")
            else:
                print(f"Monitoratge activat amb el metge {usuari.get_monitoratge}.")
                print("Dispositius: Cap")
                print("1. Desactivar monitoratge")
                print("2. Tornar")
                opcio_monitoratge = input("Selecciona una opció: ")
                if opcio_monitoratge == "1":
                    actiu = False
                elif opcio_monitoratge == "2":
                    return
                else:
                    print("Opció no disponible")

def menu_app(usuari, metges, des_de_registre):
    actiu = True
    while True:
        print("\n--- Menú Principal ---")
        mostrar_notificacions(usuari)
        if not usuari.get_registre_medic_complet:
            print("1. Completar el registre mèdic")
        else:
            print("1. Menú mèdic")
        print("2. Xarxes socials")
        print("3. Perfil")
        print("4. Emergència")
        print("5. Sortir")
        opcio = input("Selecciona una opció: ")
        if opcio == "1":
            if not usuari.get_registre_medic_complet:
                cita = completar_registre_medic(usuari, metges)
                print(f"Cita concertada: {cita}")
                usuari.set_registre_medic_complet(1)
            else:
                while True:
                    print("\n--- Menú Mèdic ---")
                    print("1. Dades Mèdiques")
                    print("2. Pastilles ")
                    print("3. Activitat Física")
                    print("4. Cites")
                    print("5. Tornar enrrera")
                    opcio_medic = input("Selecciona una opció: ")
                    if opcio_medic == "1":
                        gestio_dades_mediques(usuari)
                    elif opcio_medic == "2":
                        while True:    
                                print("\n--- Pastilles ---")
                                print("Aquesta funcionalitat s'implementarà de cara al futur...")
                                break
                    elif opcio_medic == "3":
                        while True:    
                                print("\n--- Activitat Física ---")
                                print("Aquesta funcionalitat s'implementarà de cara al futur...")
                                break
                    elif opcio_medic == "4":
                        while True:    
                                print("\n--- Cites ---")
                                print("1. Programar una cita amb el metge")
                                print("2. Tornar enrrera")
                                opcio = input("Selecciona una opció: ")
                                
                                if opcio == "1":
                                    cita = demanar_cita(usuari, metges)
                                    print(f"Cita concertada: {cita}")
                                elif opcio == "2":
                                    break
                                else:
                                    print("Opció no vàlida")
                    elif opcio_medic == "5":
                        break
                    else:
                        print("Opció no vàlida")
                    
        elif opcio == "2":
            while True:
                xarxes = usuari.get_xarxes_socials
                print("\n--- Xarxes Socials ---")
                print("1. Xats")
                print("2. Trucades")
                print("3. Grups")
                print("4. Contactes")
                print("5. Tornar al Menú Principal")
                opcio_socials = input("Selecciona una opció: ")

                if opcio_socials == "1":
                    xarxes.gestionar_xats()

                elif opcio_socials == "2":
                    while True:
                        print("\n--- Trucades ---")
                        print("1. Trucar")
                        print("2. Registre Trucades")
                        print("3. Tornar a Xarxes Socials") ##quito xarxes socials?
                        opcio_trucada = input("Selecciona una opció: ")
                        if opcio_trucada == "1":
                            xarxes.fer_trucada()
                        elif opcio_trucada == "2":
                            xarxes.mostrar_registre_trucades()
                        elif opcio_trucada == "3":
                            break
                        else:
                            print("Opció no vàlida")

                elif opcio_socials == "3":
                    xarxes.gestionar_grups()
                elif opcio_socials == "4":
                    xarxes.gestionar_contactes()
                elif opcio_socials == "5":
                    break

                else:
                    print("Opció no vàlida.")
            guardar_xarxes(usuari.get_id, usuari.get_xarxes_socials)


        elif opcio == "3":
            while True:
                print("\n--- Perfil ---")
                print(usuari)
                print("1. Modificar perfil")
                print("2. Configuració de monitoratge")
                print("3. Tornar al menú principal")
                opcio = input("Selecciona una opció: ")

                if opcio == "1":
                    print("\n--- Modificar perfil ---")
                    while True:
                        print("\nQuè vols editar?")
                        print("1. Telèfon")
                        print("2. Sexe")
                        print("3. Correu")
                        print("4. Tornar")
                        sel = input("Selecciona una opció: ")
                        if sel == "1":
                            nouTelf = introduir_telefon()
                            telfs = usuari.get_telefon
                            if nouTelf not in telfs:
                                telfs.append(nouTelf)
                            usuari.set_telefon = telfs
                        if sel == "2":
                            nouSex = introduir_sexe()
                            usuari.set_sexe(nouSex)
                        if sel == "3":
                            correu = input("Introdueix el nou correu electrònic: ")
                            while not validar_correu(correu):
                                print("Correu electrònic no vàlid.")
                                correu = input("Introdueix un correu electrònic vàlid: ")
                            usuari.set_correu(correu)
                        if sel == "4":
                            break
                        else:
                            print('Opció no vàlida')



                elif opcio == "2":
                    actiu = monitoratge(usuari, actiu)
                elif opcio == "3":
                    break

        elif opcio == "4":
            print("\n--- Emergència ---")
            print("S'ha enviat un avís als serveis d'emergència. Estem tractant la teva situació.")

        elif opcio == "5":  # Emergència
            print("Sortint de l'aplicació...")
            break

        else:
            print("Opció no vàlida. Torna-ho a intentar.")

def other_main(val):
    if val == 2:  # Familiar
        print("\n--- Dades del Familiar ---")
        nom = input("Nom: ")
        telefon = introduir_telefon()
        parentiu = input("Parentiu: ")
        dia = input("Introdueix el dia en que vas nèixer: ")
        mes = input("Introdueix el mes en que vas nèixer (Les 3 primeres lletres. Ex: Jan): ")
        anyy = input("Introdueix l'any en que vas nèixer: ")
        while not validar_data(dia, mes, anyy):
            print("Format no vàlid.")
            dia = input("Introdueix el dia en que vas nèixer: ")
            mes = input("Introdueix el mes en que vas nèixer (Les 3 primeres lletres. Ex: Jan): ")
            anyy = input("Introdueix l'any en que vas nèixer: ")
        genere = introduir_sexe()
        adreca = input("Adreça: ")

        print(f"\nDades del familiar:\nNom: {nom}\nNúmero: {telefon}\nParentiu: {parentiu}\nData de naixement: {dia, mes, any}\nGènere: {genere}\nAdreça: {adreca}")
        while True:
            print("\n--- Menú Familiar ---")
            print("1. Xats")
            print("2. Trucades")
            print("3. Grups")
            print("4. Contactes")
            print("5. Tornar al Menú Principal")
            try:
                opcio = int(input("Selecciona una opció: "))
                if opcio == 5:
                    return
                elif 1 <= opcio <= 4:
                    print("Aquesta funcionalitat s'implementarà de cara al futur...")
                else:
                    print("Opció no vàlida. Introdueix un número entre 1 i 5.")
            except ValueError:
                print("Entrada no vàlida. Si us plau, introdueix un número.")

    elif val == 3:  # Amic
        print("\n--- Dades de l'Amic ---")
        nom = input("Nom: ")
        while True:
            dni = input("DNI (9 caràcters): ")
            if len(dni) == 9:
                break
            print("El DNI ha de tenir 9 caràcters.")
        telefon = introduir_telefon()
        genere = introduir_sexe()
        dia = input("Introdueix el dia en que vas nèixer: ")
        mes = input("Introdueix el mes en que vas nèixer (Les 3 primeres lletres. Ex: Jan): ")
        anyy = input("Introdueix l'any en que vas nèixer: ")
        while not validar_data(dia, mes, anyy):
            print("Format no vàlid.")
            dia = input("Introdueix el dia en que vas nèixer: ")
            mes = input("Introdueix el mes en que vas nèixer (Les 3 primeres lletres. Ex: Jan): ")
            anyy = input("Introdueix l'any en que vas nèixer: ")
        adreca = input("Adreça: ")
        
        hobbies = []
        print("Introdueix els hobbies. Escriu 'fi' per acabar.")
        while True:
            hobbie = input("Hobbie: ")
            if hobbie.lower() == "fi":
                break
            hobbies.append(hobbie)

        print(f"\nDades de l'amic:\nNom: {nom}\nDNI: {dni}\nTelèfon: {telefon}\nGènere: {genere}\nData de naixement: {dia, mes, any}\nAdreça: {adreca}\nHobbies: {', '.join(hobbies)}")
        while True:
            print("\n--- Menú Amic ---")
            print("1. Xats")
            print("2. Trucades")
            print("3. Grups")
            print("4. Contactes")
            print("5. Tornar al Menú Principal")
            try:
                opcio = int(input("Selecciona una opció: "))
                if opcio == 5:
                    return
                elif 1 <= opcio <= 4:
                    print("Aquesta funcionalitat s'implementarà de cara al futur...")
                else:
                    print("Opció no vàlida. Introdueix un número entre 1 i 5.")
            except ValueError:
                print("Entrada no vàlida. Si us plau, introdueix un número.")

    elif val == 4:  # Personal Sanitari
        print("\n--- Dades del Personal Sanitari ---")
        
        while True:
            print("1. Metge")
            print("2. Enfermer")
            try:
                tipus_personal = int(input("Selecciona el tipus de personal (1 per Metge, 2 per Enfermer): "))
                if tipus_personal in [1, 2]:
                    break
                else:
                    print("Opció no vàlida. Si us plau, introdueix 1 o 2.")
            except ValueError:
                print("Entrada no vàlida. Si us plau, introdueix un número.")

        if tipus_personal == 1:  # Metge
            nom = input("Nom: ")
            while True:
                dni = input("DNI (9 caràcters): ")
                if len(dni) == 9:
                    break
                print("El DNI ha de tenir 9 caràcters.")
            telefon = introduir_telefon()
            hospital = input("Hospital on treballa: ")
            num_colegiat = input("Número de col·legiat: ")
            especialitat = input("Especialitat: ")
            
            print(f"\nDades del Metge:\nNom: {nom}\nDNI: {dni}\nTelèfon: {telefon}\nHospital: {hospital}\nNúmero de col·legiat: {num_colegiat}\nEspecialitat: {especialitat}")
        
        elif tipus_personal == 2:  # Enfermer
            nom = input("Nom: ")
            while True:
                dni = input("DNI (9 caràcters): ")
                if len(dni) == 9:
                    break
                print("El DNI ha de tenir 9 caràcters.")
            telefon = introduir_telefon()
            hospital = input("Hospital on treballa: ")
            while True:
                assistencia_domicili = input("Assistència a domicili (si/no): ").lower()
                if assistencia_domicili in ["si", "no"]:
                    break
                print("Entrada no vàlida. Si us plau, introdueix 'si' o 'no'.")
            
            print(f"\nDades de l'Enfermer:\nNom: {nom}\nDNI: {dni}\nTelèfon: {telefon}\nHospital: {hospital}\nAssistència a domicili: {assistencia_domicili}")

        # Mostrar el menú
        while True:
            print("\n--- Menú Personal Sanitari ---")
            print("1. Cites pendents")
            print("2. Solicitar cita pacient")
            print("3. Consultar constants pacient")
            print("4. Tornar")
            try:
                opcio = int(input("Selecciona una opció: "))
                if opcio == 4:
                    return
                elif opcio in [1, 2, 3]:
                    print("Dades no disponibles.")
                else:
                    print("Opció no vàlida. Introdueix un número entre 1 i 4.")
            except ValueError:
                print("Entrada no vàlida. Si us plau, introdueix un número.")

    elif val == 5:  # Admin
        print("\n--- Dades de l'Admin ---")
        nom = input("Nom: ")
        while True:
            dni = input("DNI: ")
            if len(dni) == 9:
                break
            print("El DNI ha de tenir 9 caràcters.")
        correu = input("Introdueix el teu correu electrònic: ")
        while not validar_correu(correu):
            print("Correu electrònic no vàlid.")
            correu = input("Introdueix un correu electrònic vàlid: ")
        password = input("Contrasenya: ")

        print(f"\nDades de l'Admin:\nNom: {nom}\nMail: {correu}")
        while True:
            print("\n--- Menú Admin ---")
            print("1. Temps d'us persones grans")
            print("2. Temps d'us familiars")
            print("3. Temps d'us amics")
            print("4. Temps d'us personal sanitari")
            print("5. Funcionalitats més usades")
            print("6. Interacció amb anuncis")
            print("7. Sortir")
            try:
                opcio = int(input("Selecciona una opció: "))
                if opcio == 7:
                    return
                elif 1 <= opcio <= 6:
                    print("No hi ha dades suficients per mostrar.")
                else:
                    print("Opció no vàlida. Introdueix un número entre 1 i 7.")
            except ValueError:
                print("Entrada no vàlida. Si us plau, introdueix un número.")

def main():
    metges = carregar_metges('metges.json')
    usuaris = carregar_usuaris('usuaris.json', metges)
    carregar_disponibilitat('disponibilitat.json', metges)
    print("\n** Benvingut al sistema **")

    while True:
        print("\n1. Iniciar sessió")
        print("2. Registrar-se")
        print("3. Sortir")
        opcio = input("Selecciona una opció: ")

        if opcio == "1":
            correu = input("Introdueix el teu correu electrònic: ")
            password = input("Introdueix la contrasenya: ")
            usuari = next((u for u in usuaris if u.get_correu == correu and u.get_password == password), None)

            if usuari:
                print(f"Benvingut, {usuari.get_nom}!")

                # Carregar dades mediques i cites del usuari
                dades_mediques = carregar_dades_mediques('dades_mediques.json', usuari.get_id)
                cites = carregar_cites('cites.json', usuari.get_id)
                xarxes_socials = carregar_xarxes(usuari.get_id, usuari.get_nom)
                notis = usuari.get_notificacions
                notis['cites'] = cites
                usuari.set_notificacions(notis)
                usuari.set_dades_mediques(dades_mediques)
                usuari.set_xarxes_socials(xarxes_socials)

                print(usuari.get_registre_medic_complet)
                menu_app(usuari, metges, des_de_registre=False)
                guardar_usuari('usuaris.json', usuari)
            else:
                print("Credencials incorrectes!")

        elif opcio == "2":
            usuari_tipus, val = tipus_usuari()
            if usuari_tipus:
                existent = False
                print("\n** Registre d'usuari **")
                id = generar_id_usuari(usuaris)
                telefon = introduir_telefon()
                sexe = introduir_sexe()
                nom = input("Introdueix el teu nom: ")
                cognom1 = input("Introdueix el teu primer cognom: ")
                cognom2 = input("Introdueix el teu segon cognom: ")
                dia = input("Introdueix el dia en que vas nèixer: ")
                mes = input("Introdueix el mes en que vas nèixer (Les 3 primeres lletres. Ex: Jan): ")
                anyy = input("Introdueix l'any en que vas nèixer: ")
                while not validar_data(dia, mes, anyy):
                    print("Format no vàlid.")
                    dia = input("Introdueix el dia en que vas nèixer: ")
                    mes = input("Introdueix el mes en que vas nèixer (Les 3 primeres lletres. Ex: Jan): ")
                    anyy = input("Introdueix l'any en que vas nèixer: ")
                correu = input("Introdueix el teu correu electrònic: ")
                while not validar_correu(correu):
                    print("Correu electrònic no vàlid.")
                    correu = input("Introdueix un correu electrònic vàlid: ")
                password = input("Introdueix la teva contrasenya: ")

                for usuari in usuaris:
                    if usuari.get_correu == correu:
                        print("Usuari ja existent, inicia sessió")
                        existent = True
                if not existent:
                    nou_usuari = Usuari(id, telefon, sexe, nom, cognom1, cognom2, dia, mes, anyy, correu, password, 0, DadesMediques(id), None, None, XarxesSocials(id, nom))
                    usuaris.append(nou_usuari)
                    guardar_usuari('usuaris.json', nou_usuari)

                    print(f"Registre complet! El teu ID és {id}")
                    menu_app(nou_usuari, metges, des_de_registre=True)
                    guardar_usuari('usuaris.json', nou_usuari)
            else:
                other_main(val)
        elif opcio == "3":
            print("Sortint... Adéu!")
            break

if __name__ == "__main__":
    main()
