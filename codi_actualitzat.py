import re
from datetime import datetime
from xarxes_socials_functions import *
from xarxes_socials_enhanced import *


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
        self.xarxes_socials = {
            "contactes": {},  # Unified contacts dictionary
            "xats": {},  # Chats with each contact
            "trucades": [],
            "grups": {}
        }

    def __str__(self):
        return f"Usuari: {self.nom} {self.cognom1} {self.cognom2}, Telèfon: {self.telefon}, Sexe: {self.sexe}, Data Naixement: {self.dia}/{self.mes}/{self.anyy}, Correu: {self.correu}"
    def gestionar_contactes(self):
        """Gestiona la llista de contactes"""
        while True:
            print("\n--- Gestió de Contactes ---")
            print("1. Veure contactes")
            print("2. Afegir contacte")
            print("3. Tornar")
            
            opcio = input("Selecciona una opció: ")
            
            if opcio == "1":
                self._mostrar_contactes()
            elif opcio == "2":
                self._afegir_contacte()
            elif opcio == "3":
                break
            else:
                print("Opció no vàlida.")

    def _mostrar_contactes(self):
        """Mostra tots els contactes"""
        if not self.xarxes_socials["contactes"]:
            print("No tens cap contacte.")
            return
        
        print("\n--- Els teus Contactes ---")
        for nom, detalls in self.xarxes_socials["contactes"].items():
            print(f"Nom: {nom}")
            print(f"Telèfon: {detalls.get('telefon', 'No disponible')}")
            print(f"Correu: {detalls.get('correu', 'No disponible')}")
            print("---")

    def _afegir_contacte(self):
        """Afegeix un nou contacte"""
        nom = input("Introdueix el nom del contacte: ")
        
        # Comprova si el contacte ja existeix
        if nom in self.xarxes_socials["contactes"]:
            print(f"El contacte {nom} ja existeix.")
            return
        
        telefon = input("Introdueix el telèfon (opcional): ")
        correu = input("Introdueix el correu (opcional): ")
        
        # Afegeix el contacte
        self.xarxes_socials["contactes"][nom] = {
            "telefon": telefon,
            "correu": correu,
            "xats": []  # Historial de xats amb aquest contacte
        }
        print(f"Contacte {nom} afegit!")
        return nom

    def gestionar_xats(self):
        """Gestiona els xats de l'usuari, similar a WhatsApp"""
        while True:
            print("\n--- Xats ---")
            if not self.xarxes_socials["xats"] or not self.xarxes_socials["contactes"]:
                print("No tens cap xat. Vols iniciar un nou xat?")
                self._preguntar_afegir_contacte()
                

            # Mostrar la llista de xats
            print("\nSelecciona un xat o inicia un de nou:")
            xats = []
            if self.xarxes_socials["xats"]:
                xats = list(self.xarxes_socials["xats"].keys())
                for i, contacte in enumerate(xats, 1):
                    print(f"{i}. {contacte}")
            print(f"{len(xats) + 1}. Iniciar un nou xat")
            print(f"{len(xats) + 2}. Tornar al menú principal")
            
            try:
                seleccio = int(input("Selecciona una opció: "))
                if 1 <= seleccio <= len(xats):
                    contacte = xats[seleccio - 1]
                    self._interactuar_xat(contacte)
                elif seleccio == len(xats) + 1:
                    self._enviar_missatge_nou()
                elif seleccio == len(xats) + 2:
                    break
                else:
                    print("Opció no vàlida.")
            except ValueError:
                print("Entrada no vàlida. Si us plau, selecciona un número.")

    def _interactuar_xat(self, contacte):
        #FARIA QUE FINS QUE NO VULGUI SORTIR NO SURTI DEL XAT
        """Permet interactuar amb un xat existent"""
        print(f"\n--- Xat amb {contacte} ---")
        missatges = self.xarxes_socials["xats"].get(contacte, [])
        for missatge in missatges:
            print(missatge)

        missatge_nou = input(f"Missatge per {contacte} (buit per tornar): ").strip()
        if missatge_nou:
            self.xarxes_socials["xats"][contacte].append(f"Tu: {missatge_nou}")
            print("Missatge enviat!")

    def _enviar_missatge_nou(self):
        """Inicia un nou xat seleccionant un contacte"""
        if not self.xarxes_socials["contactes"]:
            print("No tens contactes disponibles per iniciar un xat.")
            self._preguntar_afegir_contacte()
            return

        contactes = list(self.xarxes_socials["contactes"].keys())
        print("\nSelecciona un contacte per iniciar un xat:")
        for i, contacte in enumerate(contactes, 1):
            print(f"{i}. {contacte}")
        print(f"{i+1}. Afegir nou contacte")

        try:
            seleccio = int(input("Número de contacte: "))
            if 1 <= seleccio <= len(contactes):
                contacte = contactes[seleccio - 1]
                if contacte not in self.xarxes_socials["xats"]:
                    self.xarxes_socials["xats"][contacte] = []
                self._interactuar_xat(contacte)
            elif seleccio == i+1:
                contacte = self._afegir_contacte()
                self.xarxes_socials["xats"][contacte] = []
                self._interactuar_xat(contacte)
            else:
                print("Selecció no vàlida.")
        except ValueError:
            print("Entrada no vàlida. Si us plau, selecciona un número.")
    def _preguntar_afegir_contacte(self):
        """Pregunta a l'usuari si vol afegir un contacte"""
        while True:
            resposta = input("Vols afegir un contacte? (Si/No): ").strip().lower()
            if resposta == "si":
                self._afegir_contacte()
            if resposta == "no":
                break
    #----------------------------------------------------------------------------            
    #no calen aquestes diria
    def afegir_medicacio(self):
        medicacio = input("")
        self.dades_mediques["medicacions"].append(medicacio)

    def eliminar_medicacio(self, medicacio):
        """Elimina una medicación del usuario."""
        if medicacio in self.dades_mediques["medicacions"]:
            self.dades_mediques["medicacions"].remove(medicacio)
        else:
            print(f"La medicació '{medicacio}' no existeix.")

    def veure_medicacions(self):
        """Devuelve la lista de medicaciones."""
        return self.dades_mediques["medicacions"]
    #----------------------------------------------------------------------------
    
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
                while True:    
                    print("\n--- Dades Mèdiques ---")
                    print("1. Visualitzar Dades Mèdiques")
                    print("2. Editar Dades Mèdiques")
                    print("3. Tornar al menú principal")
                    opcio = input("Selecciona una opció: ")
                    
                    if opcio == "1":
                        for clau, valor in usuari.dades_mediques.items():
                            print(f"{clau}: {valor}")
                    if opcio == "2":
                        #poder editar dades mèdiques
                        pass
                    if opcio == "3":
                        break
                    
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

            nou_usuari = Usuari(telefon, sexe, nom, cognom1, cognom2, dia, mes, anyy, correu, password)
            usuaris.append(nou_usuari)
            print("Registre completat!")

        elif opcio == "3":
            print("Sortint...")
            break

if __name__ == "__main__":
    main()
