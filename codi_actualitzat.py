import re
from datetime import datetime

# Classe Usuari
class Usuari:
    def __init__(self, telefon, sexe, nom, cognom1, cognom2, dia, mes, anyy, correu, password):
        self.telefon = telefon
        self.sexe = sexe
        self.nom = nom
        self.cognom1 = cognom1
        self.cognom2 = cognom2
        self.dia = dia
        self.mes = mes
        self.anyy = anyy
        self.correu = correu
        self.password = password
        self.registre_medic_complet = False
        self.dades_mediques = {}
        self.notificacions = {
            "missatges": [],
            "trucades": [],
            "cites": [],
            "recordatoris": [],
        }
        self.monitoratge = None  # El metge que monitoritza

    def __str__(self):
        return f"Usuari: {self.nom+" "+self.cognom1+" "+self.cognom2}, Telèfon: {self.telefon}, Sexe: {self.sexe}, Data Naixement: {self.dia+"/"+self.mes+"/"+self.anyy}, Correu: {self.correu}"

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
    
    # Malalties prèvies
    malalties = input("Introdueix les teves malalties prèvies (separades per comes, o pressiona Enter si no tens cap): ")
    usuari.dades_mediques["Malalties Prèvies"] = malalties.split(",") if malalties else []

    # Alergies
    al_lergies = input("Introdueix les teves al·lèrgies (separades per comes, o pressiona Enter si no tens cap): ")
    usuari.dades_mediques["Al·lèrgies"] = al_lergies.split(",") if al_lergies else []

    # Alçada
    alçada = input("Introdueix la teva alçada (en cm): ")
    usuari.dades_mediques["Alçada"] = alçada

    # Pes
    pes = input("Introdueix el teu pes (en kg): ")
    usuari.dades_mediques["Pes"] = pes

    # Medicació
    medicacions = []
    while True:
        medicacio = input("Introdueix el nom de la medicació que estàs prenent (o pressiona Enter per acabar): ")
        if medicacio == "":
            break
        dosi = input(f"Introdueix la dosi de {medicacio} en mg: ")
        medicacions.append({"medicacio": medicacio, "dosi": dosi})
    
    usuari.dades_mediques["Medications"] = medicacions
    
    # Concertar cita amb el metge
    metge = "Dr. Joan Pérez"  # Nom fictici del metge
    print(f"\nSeleccionant metge: {metge}")

    dies_disponibles = ["10 Jan 2025", "12 Jan 2025"]
    print("Dies disponibles:")
    for i, dia in enumerate(dies_disponibles, 1):
        print(f"{i}. {dia}")
    
    opcio_dia = input("Selecciona el dia (1 o 2): ")
    dia_seleccionat = dies_disponibles[int(opcio_dia)-1]
    hores_disponibles = ["10:00", "11:00", "12:00", "13:00"]
    
    print("\nHores disponibles per a la cita:")
    for i, hora in enumerate(hores_disponibles, 1):
        print(f"{i}. {hora}")
    
    opcio_hora = input("Selecciona l'hora: ")
    hora_seleccionada = hores_disponibles[int(opcio_hora)-1]

    tipus_visita = input("\nSelecciona el tipus de visita (online/presencial): ").lower()

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
            print("1. Dades mèdiques")
        print("2. Xarxes socials")
        print("3. Perfil")
        print("4. Emergència")
        print("5. Sortir")
        opcio = input("Selecciona una opció: ")

        if opcio == "1":
            if not usuari.registre_medic_complet:
                cita = completar_registre_medic(usuari)
                print(f"Cita concertada: {cita}")
                usuari.registre_medic_complet = True
            else:
                print("\n--- Dades Mèdiques ---")
                for clau, valor in usuari.dades_mediques.items():
                    print(f"{clau}: {valor}")

        elif opcio == "2":
            print("\n--- Xarxes Socials ---")
            print("Aquesta funcionalitat encara està en desenvolupament.")

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

# Funció principal
def main():
    usuaris = []

    print("Benvingut al sistema!")
    while True:
        print("\n1. Iniciar sessió")
        print("2. Registrar-se")
        print("3. Sortir")
        opcio = input("Selecciona una opció: ")

        if opcio == "1":  # Iniciar sessió
            usuari_input = input("Introdueix el teu telèfon o correu electrònic: ")
            password = input("Introdueix la contrasenya: ")

            usuari = next((u for u in usuaris if (u.telefon == usuari_input or u.correu == usuari_input) and u.password == password), None)
            if usuari:
                print(f"Benvingut, {usuari.nom}!")
                menu_app(usuari, des_de_registre=False)
            else:
                print("Telèfon/correu o contrasenya incorrecta!")

        elif opcio == "2":  # Registrar-se
            print("\n** Registre **")
            telefon = input("Introdueix el teu telèfon: ")
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

            nou_usuari = Usuari(telefon, sexe, nom, cognom1, cognom2, dia, mes, anyy, correu, password)
            usuaris.append(nou_usuari)
            print("Registre completat!")

        elif opcio == "3":
            print("Sortint...")
            break

if __name__ == "__main__":
    main()
