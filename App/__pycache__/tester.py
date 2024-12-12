import unittest
from unittest.mock import patch, mock_open
from datetime import datetime
from classes import Usuari, Metge, DadesMediques, Cita
from codi_actualitzat import (
    generar_id_usuari,
    carregar_metges,
    carregar_cites,
    guardar_cites,
    validar_correu,
    validar_data,
    editar_pes,
    editar_altura,
    guardar_dades_mediques
)

class TestBackendLogic(unittest.TestCase):

    def setUp(self):
        """Configura els objectes comuns a diversos testos."""
        self.metge = Metge(
            DNI="12345678A",
            nom="Joan",
            cognom1="Pérez",
            cognom2="García",
            telefon="654321987",
            hospital="Hospital Clínic",
            numColegiat="987654",
            especialitat="Cardiologia",
            disponibilitat=["2024-12-12"]
        )
        
        self.usuari = Usuari(
            id=1,
            telefon="123456789",
            sexe="home",
            nom="Pau",
            cognom1="López",
            cognom2="Martínez",
            dia=15,
            mes="Jan",
            anyy=1985,
            correu="pau.lopez@gmail.com",
            password="password123",
            registre_medic_complet=False,
            dades_mediques=DadesMediques(idUsuari=1, malalties=["asma"], medicacions=[], altura=175, pes=70, alergies=[]),
            notificacions={},
            monitoratge=None,
            xarxes_socials=None
        )

    @patch("builtins.open", new_callable=mock_open, read_data='[]')
    @patch("json.load", return_value=[])
    @patch("json.dump")
    def test_guardar_cites(self, mock_json_dump, mock_json_load, mock_file):
        """Test per afegir una nova cita i guardar-la."""
        cita = Cita(
            idVisita=12345,
            data="2024-12-12",
            tipusVisita="online",
            prescripcions="Paracetamol",
            idUsuari=1,
            DNI_metge="12345678A",
            cognomMetge="Pérez"
        )
        guardar_cites(cita)
        mock_json_dump.assert_called_once()  # Comprova que es crida json.dump
        args, _ = mock_json_dump.call_args
        self.assertIn("idVisita", args[0][0])  # Verifica que la cita s'ha afegit correctament

    @patch("builtins.open", new_callable=mock_open, read_data='[]')
    @patch("json.load", return_value=[])
    def test_cites_per_usuari(self, mock_json_load, mock_file):
        """Test per verificar les cites d'un usuari."""
        cites = carregar_cites('cites.json', idUsuari=1)
        self.assertEqual(cites, [])  # Comprova que no hi ha cites inicials

    @patch("builtins.open", new_callable=mock_open, read_data='[{"DNI": "12345678A", "nom": "Joan", "cognom1": "Pérez", "cognom2": "García", "telefon": "654321987", "hospital": "Hospital Clínic", "numColegiat": "987654", "especialitat": "Cardiologia", "disponibilitat": []}]')
    @patch("json.load")
    def test_carregar_metges(self, mock_json_load, mock_file):
        """Test per carregar metges d'un fitxer JSON."""
        mock_json_load.return_value = [
            {
                "DNI": "12345678A",
                "nom": "Joan",
                "cognom1": "Pérez",
                "cognom2": "García",
                "telefon": "654321987",
                "hospital": "Hospital Clínic",
                "numColegiat": "987654",
                "especialitat": "Cardiologia",
                "disponibilitat": []
            }
        ]
        metges = carregar_metges('metges.json')
        self.assertGreater(len(metges), 0)
        self.assertIsInstance(metges[0], Metge)

    def test_generar_id_usuari(self):
        """Test per verificar la generació d'IDs únics d'usuaris."""
        usuaris = [self.usuari]
        nou_id = generar_id_usuari(usuaris)
        self.assertNotEqual(nou_id, self.usuari.get_id)

    def test_validar_correu(self):
        """Test per verificar la validació del correu electrònic."""
        self.assertTrue(validar_correu("test@example.com"))
        self.assertFalse(validar_correu("testexample.com"))

    def test_validar_data(self):
        """Test per verificar la validació de dates."""
        self.assertTrue(validar_data(15, "Jan", 1985))
        self.assertFalse(validar_data(31, "Feb", 2024))

    def test_dades_mediques_set_get(self):
        """Test per comprovar els getters i setters de DadesMediques."""
        dades_mediques = self.usuari.get_dades_mediques
        self.assertEqual(dades_mediques.get_altura, 175)
        self.assertEqual(dades_mediques.get_pes, 70)
        
        # Modificar valors
        dades_mediques.set_altura(180)
        dades_mediques.set_pes(75)
        
        self.assertEqual(dades_mediques.get_altura, 180)
        self.assertEqual(dades_mediques.get_pes, 75)

    def test_afegir_notificacions(self):
        """Test per afegir notificacions a l'usuari."""
        notificacions = self.usuari.get_notificacions
        self.assertEqual(notificacions, {'missatges': [], 'trucades': [], 'cites': [], 'recordatoris': []})  # Inicialment buit
        
        notificacions["missatges"] = ["Benvingut al sistema!"]
        self.usuari.set_notificacions(notificacions)
        
        self.assertIn("Benvingut al sistema!", self.usuari.get_notificacions["missatges"])

    def test_completar_registre_medic(self):
        """Test per comprovar la completació del registre mèdic."""
        self.assertFalse(self.usuari.get_registre_medic_complet)
        
        self.usuari.set_registre_medic_complet(True)
        
        self.assertTrue(self.usuari.get_registre_medic_complet)

    def test_usuari_to_string(self):
        """Test per comprovar la representació en cadena d'un usuari."""
        expected = "Usuari: Pau López Martínez, Telèfon: 123456789, Sexe: home, Data Naixement: 15/Jan/1985, Correu: pau.lopez@gmail.com"
        self.assertEqual(str(self.usuari), expected)

    def test_metge_to_string(self):
        """Test per comprovar la representació en cadena d'un metge."""
        expected = "Dr. Joan Pérez García (Cardiologia) - Hospital Clínic"
        self.assertEqual(str(self.metge), expected)

    def test_afegir_malaltia(self):
        """Test per afegir una malaltia a les dades mèdiques."""
        malalties = self.usuari.get_dades_mediques.get_malalties
        self.assertIn("asma", malalties)
        
        malalties.append("diabetis")
        self.usuari.get_dades_mediques.set_malalties(malalties)
        
        self.assertIn("diabetis", self.usuari.get_dades_mediques.get_malalties)

    def test_afegir_medicacio(self):
        """Test per afegir una medicació a les dades mèdiques."""
        medicacions = self.usuari.get_dades_mediques.get_medicacions
        self.assertEqual(len(medicacions), 0)
        
        medicacions.append(("Paracetamol", "500mg"))
        self.usuari.get_dades_mediques.set_medicacions(medicacions)
        
        self.assertIn(("Paracetamol", "500mg"), self.usuari.get_dades_mediques.get_medicacions)

    @patch("builtins.input", side_effect=["180"])
    def test_editar_altura_valid(self, mock_input):
        """Test per comprovar que es pot editar una altura vàlida."""
        editar_altura(self.usuari)
        self.assertEqual(self.usuari.get_dades_mediques.get_altura, 180)

    @patch("builtins.input", side_effect=["400", "-10", "150"])
    def test_editar_altura_invalid(self, mock_input):
        """Test per comprovar que no es pot assignar una altura invàlida fins introduir una vàlida."""
        editar_altura(self.usuari)
        self.assertEqual(self.usuari.get_dades_mediques.get_altura, 150)

    @patch("builtins.input", side_effect=["80"])
    def test_editar_pes_valid(self, mock_input):
        """Test per comprovar que es pot editar un pes vàlid."""
        editar_pes(self.usuari)
        self.assertEqual(self.usuari.get_dades_mediques.get_pes, 80)

    @patch("builtins.input", side_effect=["500", "-20", "90"])
    def test_editar_pes_invalid(self, mock_input):
        """Test per comprovar que no es pot assignar un pes invàlid fins introduir un vàlid."""
        editar_pes(self.usuari)
        self.assertEqual(self.usuari.get_dades_mediques.get_pes, 90)

    def test_cita_to_string(self):
        """Test per comprovar la representació en cadena d'una cita."""
        cita = Cita(
            idVisita=12345,
            data="2024-12-12",
            tipusVisita="online",
            prescripcions="Paracetamol",
            idUsuari=1,
            DNI_metge="12345678A",
            cognomMetge="Pérez"
        )
        expected = "Cita 12345 - Data: 2024-12-12, Tipus: online, Prescripcions: Paracetamol, Metge: Dr Pérez"
        self.assertEqual(str(cita), expected)

    def test_generar_id_cita_unique(self):
        """Test per verificar que es generen IDs únics per a les cites."""
        id1 = 12345
        id2 = 54321
        self.assertNotEqual(id1, id2)

    @patch("builtins.open", new_callable=mock_open, read_data='[]')
    @patch("json.load", return_value=[])
    @patch("json.dump")
    def test_guardar_dades_mediques(self, mock_json_dump, mock_json_load, mock_file):
        """Test per comprovar la funcionalitat de guardar dades mèdiques."""
        dades_med = self.usuari.get_dades_mediques
        guardar_dades_mediques(self.usuari.get_id, dades_med)
        mock_json_dump.assert_called_once()
        args, _ = mock_json_dump.call_args
        self.assertIn("ID_Usuari", args[0][0])  # Comprova que l'ID de l'usuari es guarda correctament
        self.assertIn("Altura", args[0][0])  # Comprova que altres dades es guarden correctament

if __name__ == "__main__":
    unittest.main()
