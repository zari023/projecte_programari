# Classe Usuari
class Usuari:
    def __init__(self, id, telefon, sexe, nom, cognom1, cognom2, dia, mes, anyy, correu, password, registre_medic_complet, dades_mediques=None, notificacions=None, monitoratge=None, xarxes_socials=None):
        self.id = id
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
        self.registre_medic_complet = registre_medic_complet
        self.dades_mediques = dades_mediques
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











# Classe Metge
class Metge:
    def __init__(self, DNI, nom, cognom1, cognom2, telefon, hospital, numColegiat, especialitat):
        self.DNI = DNI
        self.nom = nom
        self.cognom1 = cognom1
        self.cognom2 = cognom2
        self.telefon = telefon
        self.hospital = hospital
        self.numColegiat = numColegiat
        self.especialitat = especialitat

    def __str__(self):
        return f"Dr. {self.nom} {self.cognom1} {self.cognom2} ({self.especialitat}) - {self.hospital}"

# Classe DadesMediques
class DadesMediques:
    def __init__(self, idUsuari, malalties = [], medicacions = (), altura = int, pes = int, alergies = []):
        self._idUsuari = idUsuari
        self._malalties = malalties
        self._medicacions = medicacions  # Llista de tuples (medicació, quantitat)
        self._altura = altura
        self._pes = pes
        self._alergies = alergies  # Llista d'al·lèrgies

    # Getters
    def get_idUsuari(self):
        return self._idUsuari
    
    def get_malalties(self):
        return self._malalties

    def get_medicacions(self):
        return self._medicacions

    def get_altura(self):
        return self._altura

    def get_pes(self):
        return self._pes

    def get_alergies(self):
        return self._alergies

    # Setters
    def set_idUsuari(self, idUsuari):
        self._idUsuari = idUsuari

    def set_malalties(self, malalties):
        self._malalties = malalties
        
    def set_medicacions(self, medicacions):
        self._medicacions = medicacions

    def set_altura(self, altura):
        self._altura = altura

    def set_pes(self, pes):
        self._pes = pes

    def set_alergies(self, alergies):
        self._alergies = alergies

    def __str__(self):
        return f"Usuari: {self._idUsuari}, Medicacions: {self._medicacions}, Alçada: {self._altura}, Pes: {self._pes}, Al·lèrgies: {self._alergies}"

# Classe Cita
class Cita:
    def __init__(self, idVisita, data, tipusVisita, prescripcions, idUsuari, DNI_metge):
        self.idVisita = idVisita
        self.data = data
        self.tipusVisita = tipusVisita  # "online" o "presencial"
        self.prescripcions = prescripcions  # Llista de prescripcions
        self.idUsuari = idUsuari
        self.DNI_metge = DNI_metge

    def __str__(self):
        prescripcions_str = ", ".join(self.prescripcions)
        return f"Cita {self.idVisita} - Data: {self.data}, Tipus: {self.tipusVisita}, Prescripcions: {prescripcions_str}, Usuari: {self.idUsuari}, Metge: {self.DNI_metge}"

