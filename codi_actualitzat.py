import re
from datetime import datetime
from xarxes_socials_functions import *
from xarxes_socials_enhanced import *
import csv
import random
from classes import *
import json


def generar_id():
    return random.randint(1000, 9999)

# Carregar metges
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
                especialitat=row['especialitat']
            )
            metges.append(metge)
    return metges


def carregar_dades_mediques(ruta_json, id_usuari):
    try:
        with open(ruta_json, 'r', encoding='utf-8') as file:
            dades = json.load(file)
        # Filtrar dades per ID_Usuari
        for row in dades:
            if int(row["ID_Usuari"]) == int(id_usuari):
                print(row["ID_Usuari"], row['Malalties'],row["Medicacions"], row["Altura"], row["Pes"], row["Alergies"])
                return DadesMediques(row["ID_Usuari"], row["Medicacions"], row["Altura"], row["Pes"], row["Alergies"])
            
        return DadesMediques(id_usuari)  
        # Retorna None si no es troben dades per aquest usuari
        return None
    except FileNotFoundError:
        print(f"Error: No s'ha trobat el fitxer {ruta_json}.")
        return None
    except json.JSONDecodeError:
        print("Error: Format JSON invàlid.")
        return None

# Filtrar cites per ID d'usuari
# Filtrar cites per ID d'usuari
def carregar_cites(file_path, idUsuari):
    cites = []
    with open(file_path, mode='r', encoding='utf-8') as file:
        dades = json.load(file)
        for row in dades:
            if str(row['idUsuari']) == str(idUsuari):
                cites.append(Cita(
                    idVisita=row['idVisita'],
                    data=row['data'],
                    tipusVisita=row['tipusVisita'],
                    prescripcions=row['prescripcions'],
                    idUsuari=row['idUsuari'],
                    DNI_metge=row['DNI_metge']
                ))
    return cites

# Cargar usuarios desde CSV
def carregar_usuaris(file_path):
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
                registre_medic_complet=bool(int(row['Registre_Medic']))
            )
            usuaris.append(usuari)
    return usuaris

# Guardar un nuevo usuario en el CSV
def guardar_usuari(file_path, usuari):
    with open(file_path, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow([
            usuari.id, usuari.telefon, usuari.sexe, usuari.nom,
            usuari.cognom1, usuari.cognom2, usuari.dia, usuari.mes,
            usuari.anyy, usuari.correu, usuari.password, usuari.registre_medic_complet
        ])

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

def gestio_dades_mediques(usuari):
    while True:
        print("\n--- Dades Mèdiques ---")
        print("1. Visualitzar Dades Mèdiques")
        print("2. Editar Dades Mèdiques")
        print("3. Tornar al menú principal")
        
        opcio = input("Selecciona una opció: ")
        
        if opcio == "1":
            # Visualitzar dades mèdiques
            print(usuari.dades_mediques)
        
        elif opcio == "2":
            # Editar dades mèdiques
            while True:
                print("\nQuè vols editar?")
                print("1. Medicacions")
                print("2. Altura")
                print("3. Pes")
                print("4. Al·lèrgies")
                print("5. Tornar")
                
                subOpcio = input("Selecciona una opció: ")
                
                if subOpcio == "1":
                    # Editar medicacions
                    #POTSER ESTARIA GUAY DONAR OPCIÓ PER AFEGIR MEDICACIONS
                    print("Medicacions actuals:", usuari.dades_mediques.get_medicacions())
                    medicacions = introduir_medicaments()
                    usuari.dades_mediques.set_medicacions(medicacions)
                    print("Medicacions actualitzades.")
                
                elif subOpcio == "2":
                    # Editar altura
                    nova_altura = float(input("Introdueix nova altura (en cm): "))
                    usuari.dades_mediques.set_altura(nova_altura)
                    print("Altura actualitzada.")
                
                elif subOpcio == "3":
                    # Editar pes
                    nou_pes = float(input("Introdueix nou pes (en kg): "))
                    usuari.dades_mediques.set_pes(nou_pes)
                    print("Pes actualitzat.")
                
                elif subOpcio == "4":
                    # Editar al·lèrgies
                    print("Al·lèrgies actuals:", usuari.dades_mediques.get_alergies())
                    noves_alergies = input("Introdueix noves al·lèrgies (separades per ;): ")
                    alergies = noves_alergies.split(';')
                    usuari.dades_mediques.set_alergies(alergies)
                    print("Al·lèrgies actualitzades.")
                
                elif subOpcio == "5":
                    break
                
                else:
                    print("Opció no vàlida. Si us plau, tria una opció del menú.")
        
        elif opcio == "3":
            break
        
        else:
            print("Opció no vàlida. Si us plau, tria una opció del menú.")


# Validació de correu electrònic
def validar_correu(correu):
    return re.match(r"[^@]+@[^@]+\.[^@]+", correu) is not None

# Validació data naixement
def validar_data(dia, mes, anyy):
    mesos_valids = ["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"]
    try:
        dia = int(dia)
        anyy = int(anyy)
        if mes.lower() not in mesos_valids:
            raise ValueError
        return True
    except ValueError:
        return False

def validar_telefon(tel):
    if len(tel) != 9:
        print("Número de telèfon incorrecte")
        return False
    return True

def introduir_telefon():
    while True:
        tel = input("Introdueix el teu telèfon:")
        res = validar_telefon(tel)
        if res:
            return tel
        
# Mostrar notificacions
def mostrar_notificacions(usuari):
    print("\n--- Notificacions ---")
    for categoria, notificacions in usuari.notificacions.items():
        if notificacions:
            print(f"{categoria.capitalize()}:")
            for notificacio in notificacions:
                print(f"  - {notificacio}")
        else:
            print(f"{categoria.capitalize()}: No hi ha notificacions.")

# Completar el registre mèdic
def completar_registre_medic(usuari):
    print("\n--- Completar el Registre Mèdic ---")
    
    malalties = input("Introdueix les teves malalties prèvies (separades per comes, o pressiona Enter si no tens cap): ")
    malalties_llista = malalties.split(",") if malalties else []
    usuari.dades_mediques.set_malalties_previes(malalties_llista)
    
    # Al·lèrgies
    al_lergies = input("Introdueix les teves al·lèrgies (separades per comes, o pressiona Enter si no tens cap): ")
    alergies_llista = al_lergies.split(",") if al_lergies else []
    usuari.dades_mediques.set_alergies(alergies_llista)
    
    # Alçada
    while True:
        try:
            alçada = float(input("Introdueix la teva alçada (en cm): "))
            usuari.dades_mediques.set_altura(alçada)
            break
        except ValueError:
            print("Si us plau, introdueix un valor numèric vàlid.")
    
    # Pes
    while True:
        try:
            pes = float(input("Introdueix el teu pes (en kg): "))
            usuari.dades_mediques.set_pes(pes)
            break
        except ValueError:
            print("Si us plau, introdueix un valor numèric vàlid.")
    
    # Medicació
    medicacions = []
    while True:
        medicacio = input("Introdueix el nom de la medicació que estàs prenent (o pressiona Enter per acabar): ")
        if medicacio == "":
            break
        
        dosi = input(f"Introdueix la dosi de {medicacio}: ")
        medicacions.append((medicacio, dosi))
    
    # Actualitzar medicacions a la classe DadesMediques
    usuari.dades_mediques.set_medicacions(tuple(medicacions))
    
    # Concertar cita amb el metge
    metge = "Dr. Joan Pérez"  # Nom fictici del metge
    print(f"\nSeleccionant metge: {metge}")

    dies_disponibles = ["10 Jan 2025", "12 Jan 2025"]
    print("Dies disponibles:")
    for i, dia in enumerate(dies_disponibles, 1):
        print(f"{i}. {dia}")
    while True:
        opcio_dia = input("Selecciona el dia (1 o 2): ")
        if opcio_dia == "1" or opcio_dia == "2":
            break
        print("Opció incorrecta")
    dia_seleccionat = dies_disponibles[int(opcio_dia)-1]
    hores_disponibles = ["10:00", "11:00", "12:00", "13:00"]
    
    print("\nHores disponibles per a la cita:")
    for i, hora in enumerate(hores_disponibles, 1):
        print(f"{i}. {hora}")
    while True:
        opcio_hora = int(input("Selecciona l'hora: "))
        if 1<= opcio_hora <= len(hores_disponibles):
            break
        print("Opció incorrecta")
    hora_seleccionada = hores_disponibles[opcio_hora-1]

    #potser massa restrictiu?
    while True:
        tipus_visita = input("\nSelecciona el tipus de visita (online/presencial): ").lower()
        if tipus_visita == "online" or tipus_visita == "presencial":
            break
        print("Opció incorrecte")
    ############################################
    
    cita = f"Cita amb {metge} el {dia_seleccionat} a les {hora_seleccionada} - Tipus de visita: {tipus_visita}"
    usuari.notificacions["cites"].append(cita)
    usuari.monitoratge = metge  # Asignem el metge com qui monitoritza

    print("Registre mèdic completat i cita concertada!")
    return cita

def monitoratge(usuari):
    print("\n--- Configuració de Monitoratge ---")
    if not usuari.registre_medic_complet:
        print("No tens el registre mèdic completat. No es pot monitoritzar fins que no ho facis.")
    else:
        while True:
            if usuari.monitoratge is None:
                print("El monitoratge està desactivat")
                print("1. Activar monitoratge")
                print("2. Tornar")
                opcio_monitoratge = input("Selecciona una opció: ")
                if opcio_monitoratge == "1":
                    usuari.monitoratge = "Dr. Joan Pérez"
                elif opcio_monitoratge == "2":
                    return
                else:
                    print("Opció no disponible")
            else:
                print(f"Monitoratge activat amb el metge {usuari.monitoratge}.")
                print("Dispositius: Cap")
                print("1. Desactivar monitoratge")
                print("2. Tornar")
                opcio_monitoratge = input("Selecciona una opció: ")
                if opcio_monitoratge == "1":
                    usuari.monitoratge = None
                elif opcio_monitoratge == "2":
                    return
                else:
                    print("Opció no disponible")

# Menú principal dins de l'app
def menu_app(usuari, des_de_registre):
    while True:
        print("\n--- Menú Principal ---")
        mostrar_notificacions(usuari)
        if not usuari.registre_medic_complet:
            print("1. Completar el registre mèdic")
        else:
            print("1. Menú mèdic")
        print("2. Xarxes socials")
        print("3. Perfil")
        print("4. Emergència")
        print("5. Sortir")
        opcio = input("Selecciona una opció: ")
        if opcio == "1":
            if not usuari.registre_medic_complet:
                cita = completar_registre_medic(usuari)
                print(f"Cita concertada: {cita}")
                usuari.registre_medic_complet = 1
            else:
                print("\n--- Menú Mèdic ---")
                print("1. Dades Mèdiques")
                print("2. Pastilles ")
                print("3. Activitat Física")
                print("4. Cites")
                opcio_medic = input("Selecciona una opció: ")
                if opcio_medic == "1":
                    gestio_dades_mediques(usuari)
                elif opcio_medic == "2":
                    while True:    
                            print("\n--- Pastilles ---")
                            print("1. Visualitzar Dades Mèdiques")
                            print("2. Editar Dades Mèdiques")
                            print("3. Tornar al menú principal")
                            opcio = input("Selecciona una opció: ")
                            
                            if opcio == "1":
                                print(usuari.dades_mediques)
                            if opcio == "2":
                                #poder editar dades mèdiques
                                pass
                            if opcio == "3":
                                break
                elif opcio_medic == "3":
                    while True:    
                            print("\n--- Activitat Física ---")
                            print("1. Visualitzar Dades Mèdiques")
                            print("2. Editar Dades Mèdiques")
                            print("3. Tornar al menú principal")
                            opcio = input("Selecciona una opció: ")
                            
                            if opcio == "1":
                                print(usuari.dades_mediques)
                            if opcio == "2":
                                #poder editar dades mèdiques
                                pass
                            if opcio == "3":
                                break
                elif opcio_medic == "4":
                    while True:    
                            print("\n--- Cites ---")
                            print("1. Visualitzar Dades Mèdiques")
                            print("2. Editar Dades Mèdiques")
                            print("3. Tornar al menú principal")
                            opcio = input("Selecciona una opció: ")
                            
                            if opcio == "1":
                                print(usuari.dades_mediques)
                            if opcio == "2":
                                #poder editar dades mèdiques
                                pass
                            if opcio == "3":
                                break
                else:
                    print("Opció no vàlida")
                    
        elif opcio == "2":
            while True:
                print("\n--- Xarxes Socials ---")
                print("1. Xats")
                print("2. Trucades")
                print("3. Grups")
                print("4. Contactes")
                print("5. Tornar al Menú Principal")
                opcio_socials = input("Selecciona una opció: ")

                if opcio_socials == "1":
                    usuari.gestionar_xats()

                elif opcio_socials == "2":
                    fer_trucada(usuari)

                elif opcio_socials == "3":
                    gestionar_grups(usuari)
                elif opcio_socials == "4":
                    usuari.gestionar_contactes()
                elif opcio_socials == "5":
                    break

                else:
                    print("Opció no vàlida.")


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
                    # Repetir el registre de perfil
                    menu_app(usuari, des_de_registre=True)
                elif opcio == "2":
                    monitoratge(usuari)
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

# Programa principal

def main():
    usuaris = carregar_usuaris('usuaris.json')
    metges = carregar_metges('metges.json')

    print("\n** Benvingut al sistema **")

    while True:
        print("\n1. Iniciar sessió")
        print("2. Registrar-se")
        print("3. Sortir")
        opcio = input("Selecciona una opció: ")

        if opcio == "1":
            correu = input("Introdueix el teu correu electrònic: ")
            password = input("Introdueix la contrasenya: ")
            usuari = next((u for u in usuaris if u.correu == correu and u.password == password), None)

            if usuari:
                print(f"Benvingut, {usuari.nom}!")

                # Carregar dades mediques i cites del usuari
                dades_mediques = carregar_dades_mediques('dades_mediques.json', usuari.id)
                cites = carregar_cites('cites.json', usuari.id)
                usuari.dades_mediques = dades_mediques

                """print("\\nLes teves dades mèdiques:")
                for d in dades_mediques:
                    print(d)

                print("\\nLes teves cites programades:")
                for c in cites:
                    print(c)"""
                print(usuari.registre_medic_complet)
                menu_app(usuari, des_de_registre=False)
            else:
                print("Credencials incorrectes!")

        elif opcio == "2":
            existent = False
            print("\n** Registre d'usuari **")
            id = generar_id()
            telefon = introduir_telefon()
            sexe = input("Introdueix el teu sexe: ")
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
                if usuari.correu == correu:
                    print("Usuari ja existent, inicia sessió")
                    existent = True
            if not existent:
                nou_usuari = Usuari(id, telefon, sexe, nom, cognom1, cognom2, dia, mes, anyy, correu, password)
                usuaris.append(nou_usuari)
                guardar_usuari('usuaris.json', nou_usuari)

                print(f"Registre complet! El teu ID és {id}")
                menu_app(nou_usuari, des_de_registre=True)

        elif opcio == "3":
            print("Sortint... Adéu!")
            break

if __name__ == "__main__":
    main()
