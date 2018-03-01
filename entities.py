from pony import orm
from datetime import date

db = orm.Database();

class AuthentificationEmploye(db.Entity):
	id_authentification = orm.PrimaryKey(int, auto=True)
	matricule = orm.Required(str, unique=True)
	mot_de_passe = orm.Required(str)
	employe = orm.Optional('Employe')

class AuthentificationClient(db.Entity):
	id_authentification = orm.PrimaryKey(int, auto=True)
	courriel = orm.Required(str, unique=True)
	mot_de_passe = orm.Required(str)
	client = orm.Optional('Client')

class Localisation(db.Entity):
	id_localisation = orm.PrimaryKey(int, auto=True)
	ville = orm.Required(str)
	province = orm.Required(str)
	adresses = orm.Set('Adresse')

class Adresse(db.Entity):
	id_adresse = orm.PrimaryKey(int, auto=True)
	id_localisation = orm.Required(Localisation)
	adresse_civique = orm.Required(str)
	code_postal = orm.Required(str)
	dossier = orm.Optional('Dossier')

class Dossier(db.Entity):
	id_dossier = orm.PrimaryKey(int, auto=True)
	id_adresse = orm.Required(Adresse)
	nom = orm.Required(str)
	prenom = orm.Required(str)
	num_telephone = orm.Required(str)
	date_naissance = orm.Required(date)
	employe = orm.Optional('Employe')
	client = orm.Optional('Client')

class Employe(db.Entity):
	id_employe = orm.PrimaryKey(int, auto=True)
	id_dossier = orm.Required(Dossier)
	id_authentification = orm.Required(AuthentificationEmploye)

class Forfait(db.Entity):
	id_forfait = orm.PrimaryKey(int, auto=True)
	nom = orm.Required(str)
	cout = orm.Required(int)
	max_location = orm.Required(int)
	max_duree = orm.Required(int)
	abonnement = orm.Set('Abonnement')

class Abonnement(db.Entity):
	id_abonnement = orm.PrimaryKey(int, auto=True)
	id_forfait = orm.Required(Forfait)
	date_debut = orm.Required(date)
	date_fin = orm.Required(date)
	client = orm.Optional('Client')

class CarteCredit(db.Entity):
	id_carte = orm.PrimaryKey(int, auto=True)
	numero = orm.Required(str)
	cvv = orm.Required(str)
	date_expiration = orm.Required(date)
	client = orm.Optional('Client')

class Client(db.Entity):
	id_client = orm.PrimaryKey(int, auto=True)
	id_dossier = orm.Required(Dossier)
	id_carte = orm.Required(CarteCredit)
	id_authentification = orm.Required(AuthentificationClient)
	id_abonnement = orm.Required(Abonnement)
	locations = orm.Set('Location')

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
	date_naissance = orm.Optional(date)
	lieu_naissance = orm.Optional(str)
	bio = orm.Optional(str)
	films = orm.Set('Film', reverse='id_realisateur')
	roles = orm.Set('Role')
	film_scenarist = orm.Set('Film' , reverse='scenaristes')

class Film(db.Entity):
	id_film = orm.PrimaryKey(int, auto=True)
	id_realisateur = orm.Optional(Personne)
	titre = orm.Required(str)
	annee_sortie = orm.Required(date)
	duree = orm.Required(int)
	langue_originale = orm.Optional(str)
	resume = orm.Required(str)
	genre = orm.Set(Genre)
	pays = orm.Set(Pays)
	roles = orm.Set('Role')
	copies = orm.Set('Copie')
	scenaristes = orm.Set(Personne)

class Role(db.Entity):
	id_film = orm.Required(Film)
	id_personne = orm.Required(Personne)
	titre = orm.Required(str)
	orm.PrimaryKey(id_film, id_personne)

class Copie(db.Entity):
	id_copie = orm.PrimaryKey(int, auto=True)
	id_film = orm.Required(Film)
	code = orm.Required(str)
	locations = orm.Set('Location')

class Location(db.Entity):
	id_location = orm.PrimaryKey(int, auto=True)
	id_client = orm.Required(Client)
	id_copie = orm.Required(Copie)
	debut = orm.Required(date)
	fin = orm.Required(date)
	remise = orm.Optional(date)

def init():
	db.bind(provider='sqlite', filename='./db/Labo2.db')
	db.generate_mapping(create_tables=False)
	with db.set_perms_for(Film):
		orm.perm('edit create delete view', group='anybody')
	with db.set_perms_for(Role):
		orm.perm('edit create delete view', group='anybody')
	with db.set_perms_for(Personne):
		orm.perm('edit create delete view', group='anybody')

