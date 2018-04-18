#!/usr/bin/python

from bottle import Bottle, run, get, post, request
import entities
import time
from datetime import date
from pony import orm
import json
import sqlite3

app = Bottle()

entities.init()

@app.post('/login')
@orm.db_session
def login():
	from bottle import response
	email = request.json['identifiant']
	password = request.json['motDePasse']
	
	client = orm.select(c.client for c in entities.AuthentificationClient if c.courriel == email and c.mot_de_passe == password).first()
	
	if(client != None):
		films = orm.select(f for f in entities.Film)[:]
		acteurs = orm.select(a.id_personne for a in entities.Role)[:]
		personnes = orm.select(p for p in entities.Personne)[:]
		
		response.content_type = 'application/json'
		return json.JSONEncoder().encode({
			'client':{
				'id_client': client.id_client,
				'nom': client.id_dossier.prenom + ' ' + client.id_dossier.nom,
				'location': [
					l.id_copie.id_copie for l in client.locations
				],
				'forfait': {'max_location' : client.id_abonnement.id_forfait.max_location}
			},
			'listePersonne': [
				{
					'id_personne': p.id_personne,
					'nom': p.nom
				}
				for p in personnes
			],
			'listeActeur': [
				{
					'id_personne': a.id_personne,
					'nom': a.nom,
					'date_naissance': a.date_naissance.strftime('%Y-%m-%d') if a.date_naissance is not None else None,
					
				}
				for a in acteurs
			],
			'listeFilm': [
				{
					'id_film': f.id_film,
					'titre': f.titre,
					'annee_sortie': f.annee_sortie,
					'duree': f.duree,
					'resume': f.resume,
					'genre': [g.nom for g in f.genre],
					'pays': [p.nom for p in f.pays],
					'langue_originale': f.langue_originale,
					'realisateur': f.id_realisateur.id_personne if f.id_realisateur is not None else None,
					'scenariste': [s.id_personne for s in f.scenaristes],
					'acteur': [{'id_personne': r.id_personne.id_personne, 'role': r.titre} for r in f.roles]
					
				}
				for f in films
			]
		})

@app.post('/location')
@orm.db_session
def location():
	copie = request.json['id_copie']
	client = request.json['id_client']
	
	theClient = orm.select(c for c in entities.Client if c.id_client == client).first()
	
	l = entities.Location(
		id_client = theClient,
		id_copie = orm.select(c for c in entities.Copie if c.id_copie == copie).first(),
		debut = date.today(),
		fin = date(2018, 3, 29)
	)
	
	print(l)
	
	orm.flush()
	
	from bottle import response
	response.content_type = 'application/json'
	return json.JSONEncoder().encode({
		'client': {
			'location': [
				l.id_copie.id_copie for l in theClient.locations
			]
		}
	})

@orm.db_session
def getFilmCorr(ids, rate):
	films = orm.select(f for f in entities.Film)[:]
	return json.JSONEncoder().encode({
		'films': [
			{
				'titre': f.titre
			} for f in films if f.id_film in ids
		],
		'rating': rate
	})

@app.post('/recommandation')
def recommandation():
	film = request.json['id_film']
	client = request.json['id_client']
	
	conn = sqlite3.connect('./db/Labo2.db')
	
	conn.enable_load_extension(True)
	conn.load_extension('./db/maths')
	
	c = conn.cursor()
	
	idfilm = [id[0]
	for id in c.execute('''SELECT otherFilmid as idFilm, Correlation.correlation FROM Correlation WHERE thisFilmid = ? AND idFilm NOT IN (SELECT Copie.id_film FROM Location JOIN Copie ON Copie.id_copie = Location.id_copie WHERE Location.id_client = ?) ORDER BY Correlation.correlation LIMIT 3''', [film, client])
	]
	
	c.execute('''SELECT avgcote FROM avgCote WHERE idFilm = ?''', film)
	rateobj = c.fetchone()
	if rateobj is not None:
		rate = c.fetchone()[0]
	else:
		rate = 0
	
	return getFilmCorr(idfilm, rate)
	
	
	


































run(app, host='localhost', port=8090)
