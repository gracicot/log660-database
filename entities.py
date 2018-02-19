from pony import orm
from datetime import date

db = orm.Database();

class AuthentificationEmploye(db.Entity):
	id_authentification = orm.PrimaryKey(int, auto=True)
	matricule = orm.Required(str, unique=True)
	mot_de_masse = orm.Required(str)

class AuthentificationClient(db.Entity):
	id_authentification = orm.PrimaryKey(int, auto=True)
	courriel = orm.Required(str, unique=True)
	mot_de_masse = orm.Required(str)

class Localisation(db.Entity):
	id_localisation = orm.PrimaryKey(int, auto=True)
	ville = orm.Required(str)
	province = orm.Required(str)

class Adresse(db.Entity):
	id_adresse = orm.PrimaryKey(int, auto=True)
	localisation = orm.Required(Localisation)
	adresse_civique = orm.Required(str)
	code_postal = orm.Required(str)

class Dossier(db.Entity):
	id_dossier = orm.PrimaryKey(int, auto=True)
	adresse = orm.Required(Adresse)
	nom = orm.Required(str)
	prenom = orm.Required(str)
	num_telephone = orm.Required(str)
	date_naissance = orm.Required(date)

class Employe(db.Entity):
	id_employe = orm.PrimaryKey(int, auto=True)
	dossier = orm.Required(Dossier)
	authentification = orm.Required(AuthentificationEmploye)

class Forfait(db.Entity):
	id_forfait = orm.PrimaryKey(int, auto=True)
	nom = orm.Required(str)
	cout = orm.Required(int)
	max_location = orm.Required(int)
	max_duree = orm.Required(int)

class Abonnement(db.Entity):
	id_abonnement = orm.PrimaryKey(int, auto=True)
	forfait = orm.Required(Forfait)
	date_debut = orm.Required(date)
	date_fin = orm.Required(date)

class CarteCredit(db.Entity):
	id_carte = orm.PrimaryKey(int, auto=True)
	numero = orm.Required(str)
	cvv = orm.Required(str)
	date_expiration = orm.Required(date)

class Client(db.Entity):
	id_client = orm.PrimaryKey(int, auto=True)
	dossier = orm.Required(Dossier)
	carte = orm.Required(CarteCredit)
	authentification = orm.Required(AuthentificationClient)
	abonnement = orm.Required(Abonnement)

class Genre(db.Entity):
	id_genre = orm.PrimaryKey(int, auto=True)
	nom = orm.Required(str)
	films = orm.Set('Film')

class Pays(db.Entity):
	id_pays = orm.PrimaryKey(int, auto=True)
	nom = orm.Required(str)
	films = orm.Set('Film')

class Personne(db.Entity):
	id_personne = orm.PrimaryKey(int, auto=True)
	nom = orm.Required(str)
	date_naissance = orm.Required(date)
	lieu_naissance = orm.Required(str)
	bio = orm.Required(str)

class Film(db.Entity):
	id_film = orm.PrimaryKey(int, auto=True)
	realisateur = orm.Required(Personne)
	titre = orm.Required(str)
	annee_sortie = orm.Required(date)
	duree = orm.Required(int)
	langue_originale = orm.Required(str)
	resume = orm.Required(str)
	genre = orm.Set(Genre)
	pays = orm.Set(Pays)

class Role(db.Entity):
	film = orm.Required(Film)
	acteur = orm.Required(Personne)
	titre = orm.Required(str)

class Copie(db.Entity):
	id_copie = orm.PrimaryKey(int, auto=True)
	film = orm.Required(Film)
	code = orm.Required(str)

class Location(db.Entity):
	id_location = orm.PrimaryKey(int, auto=True)
	client = orm.Required(Client)
	copie = orm.Required(Copie)
	debut = orm.Required(date)
	fin = orm.Required(date)
	remise = orm.Optional(date)
