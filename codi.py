import csv
import os

# Classe Usuari
class Usuari:
    def __init__(self, nom, password):
        self._nom = nom
        self._password = password
        self._registre_medic = False
        self._dades_personals = {}
        self._medicaments = []
        self._cites = []

    # Getters i Setters
    @property
    def nom(self):
        return self._nom

    @nom.setter
    def nom(self, nou_nom):
        self._nom = nou_nom

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, nova_password):
        self._password = nova_password

    @property
    def registre_medic(self):
        return self._registre_medic

    @registre_medic.setter
    def registre_medic(self, registre):
        self._registre_medic = registre

    @property
    def dades_personals(self):
        return self._dades_personals

    @dades_personals.setter
    def dades_personals(self, noves_dades):
        self._dades_personals.update(noves_dades)

    @property
    def medicaments(self):
        return self._medicaments

    @property
    def cites(self):
        return self._cites

# Classe Medicament
class Medicament:
    def __init__(self, nom, dosis, hora):
        self._nom = nom
        self._dosis = dosis
        self._hora = hora

    # Getters i Setters
    @property
    def nom(self):
        return self._nom

    @nom.setter
    def nom(self, nou_nom):
        self._nom = nou_nom

    @property
    def dosis(self):
        return self._dosis

    @dosis.setter
    def dosis(self, nova_dosis):
        self._dosis = nova_dosis

    @property
    def hora(self):
        return self._hora

    @hora.setter
    def hora(self, nova_hora):
        self._hora = nova_hora

    def consultar_posologia(self):
        return f"{self.nom}: {self.dosis} a les {self.hora}"


# Classe XarxaSocial
class XarxaSocial:
    def __init__(self):
        self._xats = []
        self._trucades = []
        self._grups = {}

    # Getters i Setters
    @property
    def xats(self):
        return self._xats

    @property
    def trucades(self):
        return self._trucades

    @property
    def grups(self):
        return self._grups

    def afegir_xat(self, xat):
        self._xats.append(xat)

    def afegir_trucada(self, trucada):
        self._trucades.append(trucada)

    def registrar_preferencies_grup(self, grup, preferencies):
        self._grups[grup] = preferencies

    def buscar_afegir_grup(self, grup):
        if grup not in self._grups:
            self._grups[grup] = "Afegit"
            return f"Grup {grup} afegit."
        return f"Grup {grup} ja existeix."


# Funcions per gestionar la base de dades
def carregar_dades(file_path):
    usuaris = []
    if os.path.exists(file_path):
        with open(file_path, mode="r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                usuari = Usuari(row["nom"], row["password"])
                usuari.registre_medic = row["registre_medic"] == "True"
                usuari.dades_personals = eval(row["dades_personals"])
                usuari.medicaments = eval(row["medicaments"])
                usuari.cites = eval(row["cites"])
                usuaris.append(usuari)
    return usuaris


def guardar_dades(file_path, usuaris):
    with open(file_path, mode="w", encoding="utf-8", newline="") as file:
        fieldnames = ["nom", "password", "registre_medic", "dades_personals", "medicaments", "cites"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for usuari in usuaris:
            writer.writerow({
                "nom": usuari.nom,
                "password": usuari.password,
                "registre_medic": usuari.registre_medic,
                "dades_personals": str(usuari.dades_personals),
                "medicaments": str([vars(medicament) for medicament in usuari.medicaments]),
                "cites": str(usuari.cites),
            })


# Funcions generals del programa
def iniciar_sessio(usuaris, nom, password):
    for usuari in usuaris:
        if usuari.nom == nom and usuari.password == password:
            return usuari
    return None


def registrar_usuari(usuaris, nom, password):
    nou_usuari = Usuari(nom, password)
    usuaris.append(nou_usuari)
    return nou_usuari


# Funció principal
def main():
    file_path = "usuaris.csv"
    usuaris = carregar_dades(file_path)

    print("Benvingut al sistema!")
    while True:
        print("\n1. Iniciar sessió")
        print("2. Registrar-se")
        opcio = input("Selecciona una opció: ")

        if opcio == "1":
            nom = input("Introdueix el teu usuari: ")
            password = input("Introdueix la contrasenya: ")
            usuari = iniciar_sessio(usuaris, nom, password)

            if usuari:
                print(f"Benvingut, {usuari.nom}!")
                while True:
                    print("\n1. Consultar dades personals")
                    print("2. Menú mèdic")
                    print("3. Sortir")
                    opcio_usuari = input("Selecciona una opció: ")

                    if opcio_usuari == "1":
                        print("Les teves dades personals:")
                        print(usuari.dades_personals)

                    elif opcio_usuari == "2":
                        print("\n1. Consultar dades mèdiques")
                        print("2. Afegir medicaments")
                        opcio_medic = input("Selecciona una opció: ")

                        if opcio_medic == "1":
                            if usuari.registre_medic:
                                print("Dades mèdiques:")
                                print(usuari.dades_personals)
                            else:
                                print("No tens registre mèdic. Fes-lo ara.")
                                dades_mediques = {"edat": input("Edat: "), "pes": input("Pes: ")}
                                usuari.registre_medic = True
                                usuari.dades_personals = dades_mediques

                        elif opcio_medic == "2":
                            nom_medicament = input("Nom del medicament: ")
                            dosis = input("Dosis: ")
                            hora = input("Hora: ")
                            medicament = Medicament(nom_medicament, dosis, hora)
                            usuari.medicaments.append(medicament)
                            print(f"Medicament {nom_medicament} afegit.")

                    elif opcio_usuari == "3":
                        print("Sortint del sistema...")
                        guardar_dades(file_path, usuaris)
                        return

            else:
                print("Usuari o contrasenya incorrecta!")

        elif opcio == "2":
            nom = input("Introdueix el teu nom: ")
            password = input("Introdueix la teva contrasenya: ")
            usuari = registrar_usuari(usuaris, nom, password)
            print(f"Usuari {usuari.nom} registrat correctament.")

        else:
            print("Opció no vàlida!")


if __name__ == "__main__":
    main()
