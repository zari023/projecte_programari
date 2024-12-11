# Classe Usuari
class Usuari:
    def __init__(self, id, telefon, sexe, nom, cognom1, cognom2, dia, mes, anyy, correu, password, registre_medic_complet, dades_mediques=None, notificacions=None, monitoratge=None, xarxes_socials=None,):
        self.__id = id
        self.__telefon = telefon
        self.__sexe = sexe
        self.__nom = nom
        self.__cognom1 = cognom1
        self.__cognom2 = cognom2
        self.__dia = dia
        self.__mes = mes
        self.__anyy = anyy
        self.__correu = correu
        self.__password = password
        self.__registre_medic_complet = registre_medic_complet
        self.__dades_mediques = dades_mediques
        self.__notificacions = {
            "missatges": [],
            "trucades": [],
            "cites": [],
            "recordatoris": [],
        }
        self.__monitoratge = monitoratge  # El metge que monitoritza
        self.__xarxes_socials = xarxes_socials

    def __str__(self):
        return f"Usuari: {self.__nom} {self.__cognom1} {self.__cognom2}, Telèfon: {self.__telefon}, Sexe: {self.__sexe}, Data Naixement: {self.__dia}/{self.__mes}/{self.__anyy}, Correu: {self.__correu}"
    
    # Getters
    @property
    def get_id(self):
        return self.__id
    @property
    def get_telefon(self):
        return self.__telefon
    @property
    def get_sexe(self):
        return self.__sexe
    @property
    def get_nom(self):
        return self.__nom
    @property
    def get_cognom1(self):
        return self.__cognom1
    @property
    def get_cognom2(self):
        return self.__cognom2
    @property
    def get_dia(self):
        return self.__dia
    @property
    def get_mes(self):
        return self.__mes
    @property
    def get_anyy(self):
        return self.__anyy
    @property
    def get_correu(self):
        return self.__correu
    @property
    def get_password(self):
        return self.__password
    @property
    def get_registre_medic_complet(self):
        return self.__registre_medic_complet
    @property
    def get_dades_mediques(self):
        return self.__dades_mediques
    @property
    def get_notificacions(self):
        return self.__notificacions
    @property
    def get_monitoratge(self):
        return self.__monitoratge
    @property
    def get_xarxes_socials(self):
        return self.__xarxes_socials

    # Setters
    def set_id(self, id):
        self.__id = id
    
    def set_telefon(self, telefon):
        # Optional: Add phone number validation
        self.__telefon = telefon
    
    def set_sexe(self, sexe):
        # Optional: Add validation for sexe
        self.__sexe = sexe
    
    def set_nom(self, nom):
        self.__nom = nom
    
    def set_cognom1(self, cognom1):
        self.__cognom1 = cognom1
    
    def set_cognom2(self, cognom2):
        self.__cognom2 = cognom2
    
    def set_dia(self, dia):
        # Optional: Add date validation
        self.__dia = dia
    
    def set_mes(self, mes):
        # Optional: Add month validation
        self.__mes = mes
    
    def set_anyy(self, anyy):
        # Optional: Add year validation
        self.__anyy = anyy
    
    def set_correu(self, correu):
        # Optional: Add email validation
        self.__correu = correu
    
    def set_password(self, password):
        # Recommendation: Add password strength validation
        self.__password = password
    
    def set_registre_medic_complet(self, registre_medic_complet):
        self.__registre_medic_complet = registre_medic_complet
    
    def set_dades_mediques(self, dades_mediques):
        self.__dades_mediques = dades_mediques
    
    def set_notificacions(self, notificacions):
        self.__notificacions = notificacions
    
    def set_monitoratge(self, monitoratge):
        self.__monitoratge = monitoratge
    
    def set_xarxes_socials(self, xarxes_socials):
        self.__xarxes_socials = xarxes_socials
    #----------------------------------------------------------------------------            
    '''#no calen aquestes diria
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
        return self.dades_mediques["medicacions"]'''
    #----------------------------------------------------------------------------

# Classe Metge
class Metge:
    def __init__(self, DNI, nom, cognom1, cognom2, telefon, hospital, numColegiat, especialitat, disponibilitat):
        self.__DNI = DNI
        self.__nom = nom
        self.__cognom1 = cognom1
        self.__cognom2 = cognom2
        self.__telefon = telefon
        self.__hospital = hospital
        self.__numColegiat = numColegiat
        self.__especialitat = especialitat
        self.__disponibilitat = disponibilitat


    def __str__(self):
        return f"Dr. {self.__nom} {self.__cognom1} {self.__cognom2} ({self.__especialitat}) - {self.__hospital}"

    @property # Getters
    def get_DNI(self):
        return self.__DNI
    @property
    def get_nom(self):
        return self.__nom
    @property
    def get_cognom1(self):
        return self.__cognom1
    @property
    def get_cognom2(self):
        return self.__cognom2
    @property
    def get_telefon(self):
        return self.__telefon
    @property
    def get_hospital(self):
        return self.__hospital
    @property
    def get_num_colegiat(self):
        return self.__numColegiat
    @property
    def get_especialitat(self):
        return self.__especialitat
    @property
    def get_disponibilitat(self):
        return self.__disponibilitat

    # Setters
    def set_DNI(self, DNI):
        # Optionally, add DNI validation if needed
        self.__DNI = DNI
    
    def set_nom(self, nom):
        self.__nom = nom
    
    def set_cognom1(self, cognom1):
        self.__cognom1 = cognom1
    
    def set_cognom2(self, cognom2):
        self.__cognom2 = cognom2
    
    def set_telefon(self, telefon):
        # Optional: Add phone number validation
        self.__telefon = telefon
    
    def set_hospital(self, hospital):
        self.__hospital = hospital
    
    def set_num_colegiat(self, numColegiat):
        self.__numColegiat = numColegiat
    
    def set_especialitat(self, especialitat):
        self.__especialitat = especialitat
    
    def set_disponibilitat(self, disponibilitat):
        self.__disponibilitat = disponibilitat

    # Optional: Method to get full name
    def get_full_name(self):
        full_name = f"{self.__nom} {self.__cognom1}"
        if self.__cognom2:
            full_name += f" {self.__cognom2}"
        return full_name
# Classe DadesMediques
class DadesMediques:
    def __init__(self, idUsuari, malalties = [], medicacions = (), altura = int, pes = int, alergies = []):
        self.__idUsuari = idUsuari
        self.__malalties = malalties
        self.__medicacions = medicacions  # Llista de tuples (medicació, quantitat)
        self.__altura = altura
        self.__pes = pes
        self.__alergies = alergies  # Llista d'al·lèrgies

    # Getters
    
    @property
    def get_idUsuari(self):
        return self.__idUsuari
    
    @property
    def get_malalties(self):
        return self.__malalties

    @property
    def get_medicacions(self):
        return self.__medicacions

    @property
    def get_altura(self):
        return self.__altura

    @property
    def get_pes(self):
        return self.__pes

    @property
    def get_alergies(self):
        return self.__alergies

    # Setters
    def set_idUsuari(self, idUsuari):
        self.__idUsuari = idUsuari

    def set_malalties(self, malalties):
        self.__malalties = malalties
        
    def set_medicacions(self, medicacions):
        self.__medicacions = medicacions

    def set_altura(self, altura):
        self.__altura = altura

    def set_pes(self, pes):
        self.__pes = pes

    def set_alergies(self, alergies):
        self.__alergies = alergies

    def __str__(self):
        return f"Malalties: {self.__malalties}, Medicacions: {self.__medicacions}, Alçada: {self.__altura}, Pes: {self.__pes}, Al·lèrgies: {self.__alergies}"

# Classe Cita
class Cita:
    def __init__(self, idVisita, data, tipusVisita, prescripcions, idUsuari, DNI_metge, cognomMetge):
        self.__idVisita = idVisita
        self.__data = data
        self.__tipusVisita = tipusVisita  # "online" o "presencial"
        self.__prescripcions = prescripcions
        self.__idUsuari = idUsuari
        self.__DNI_metge = DNI_metge
        self.__cognomMetge = cognomMetge

    def __str__(self):
        return f"Cita {self.__idVisita} - Data: {self.__data}, Tipus: {self.__tipusVisita}, Prescripcions: {self.__prescripcions}, Metge: Dr {self.__cognomMetge}"

    # Getters
    @property
    def get_id_visita(self):
        return self.__idVisita
    
    @property
    def get_data(self):
        return self.__data
    
    @property
    def get_tipus_visita(self):
        return self.__tipusVisita
    
    @property
    def get_prescripcions(self):
        return self.__prescripcions
    
    @property
    def get_id_usuari(self):
        return self.__idUsuari
    
    @property
    def get_DNI_metge(self):
        return self.__DNI_metge
    
    @property
    def get_cognom_metge(self):
        return self.__cognomMetge

    # Setters
    def set_id_visita(self, idVisita):
        self.__idVisita = idVisita
    
    def set_data(self, data):
        self.__data = data
    
    def set_prescripcions(self, prescripcions):
        self.__prescripcions = prescripcions
    
    def set_id_usuari(self, idUsuari):
        self.__idUsuari = idUsuari
    
    def set_DNI_metge(self, DNI_metge):
        self.__DNI_metge = DNI_metge
    
    def set_cognom_metge(self, cognomMetge):
        self.__cognomMetge = cognomMetge
