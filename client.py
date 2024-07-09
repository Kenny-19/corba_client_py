import sys
from omniORB import CORBA
import CosNaming
import school

def main(argv):
    try:
        orb_args = ["-ORBInitRef", "NameService=corbaname::localhost:1050"]
        orb = CORBA.ORB_init(argv + orb_args, CORBA.ORB_ID)
        obj = orb.resolve_initial_references("NameService")
        naming_service = obj._narrow(CosNaming.NamingContext)
        if naming_service is None:
            print("Failed to narrow the NameService reference")
            sys.exit(1)

        name = [CosNaming.NameComponent("GestionEtudiants", "")]
        objref = naming_service.resolve(name)
        gestion_etudiants = objref._narrow(school.GestionEtudiants)

        if gestion_etudiants is None:
            print("Object reference is not a GestionEtudiants")
            sys.exit(1)

        # Enregistrer un étudiant
        etudiant = school.Etudiant("001", "Alice", "F", "2024", "2000-01-01")
        gestion_etudiants.enregistrerEtudiant(etudiant)
        print("Enregistrement de l'étudiant terminé.")

        # Modifier la promotion et la date de naissance d'un étudiant
        gestion_etudiants.modifierEtudiant("001", "2025", "2000-01-02")
        print("Modification de l'étudiant terminée.")

        # Lire les étudiants par promotion
        etudiants = gestion_etudiants.lireEtudiantsParPromotion("2025")
        for etudiant in etudiants:
            print(f"Etudiant: {etudiant.matricule}, {etudiant.nom}, {etudiant.sexe}, {etudiant.promotion}, {etudiant.dateNaissance}")

    except CORBA.Exception as e:
        print(f"Error: {e}")

    orb.destroy()

if __name__ == "__main__":
    main(sys.argv)
