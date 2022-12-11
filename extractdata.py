from pymongo import MongoClient
from pprint import pprint
import re

full_dns_name = 'mongodb://ec2-54-229-30-76.eu-west-1.compute.amazonaws.com:27017'
username = 'test'
password = 'test'
authSource = 'admin'

client = MongoClient(host=full_dns_name, username=username, password=password, authSource=authSource)

#afficher la liste des bases de données disponibles
print( "Liste de base de donne:", client.list_database_names())

#afficher la liste des collections disponibles dans cette base de données
arxiv = client["arxiv"]
print("Liste de collection de la bdd arvix", arxiv.list_collection_names())

#afficher un des documents de cette collection
pprint(arxiv.papers.find_one())

#afficher le nombre de documents dans cette collection
print("Nombre de documents in collection papers:", arxiv.papers.count_documents({}))

#afficher le titre de 10 articles
print("\n*********Titres \n:")
for t in list(arxiv.papers.find({},{"title":1, "_id":0}).limit(10)):
    print(t)
print("\n*********Autheurs \n")
#afficher les 10 premiers auteurs par ordre alphabétique
for a in list( arxiv.papers.find({},{"authors":1, "_id":0}).sort("authors", 1).limit(10)):
    print(a)

# afficher le nombre d'articles qui n'ont pas été publiés par "Damien Chablat"
print("Le nombre d'articles pas publie par Damien est:", arxiv.papers.count_documents({'submitter':{'$ne':'Damien Chablat'}}))

# afficher le nombre de papiers téléversés en 2014. On pourra s'appuyer sur une expréssion régulière.
print("Le nombre des papiers televersé en 2004 est:", arxiv.papers.count_documents({'update_date':{'$regex':'^2014'}}))

#afficher le titre d'un article qui contient l'expression Machine Learning. On pourra utiliser une expression régulière.
print("Titrearticle qui contient Machine Learning:", arxiv.papers.find_one({"title" : {'$regex':'Machine Learning'}},{"title":1, "_id":0}))

#afficher le nombre de publications par submitter pour les 10 personnes les plus prolifiques. 
# On pourra utiliser un pipeline d'aggrégation avec les mots-clefs $group, $sort, $limit.
print("\n nombre de publications par submitter pour les 10 personnes les plus prolifiques")
for v in list(arxiv.papers.aggregate([{"$group" :{"_id":"$submitter", "np":{"$sum" : 1 }}}, {"$sort" : {"np":-1}}, {"$limit" : 10}])):
    print(v)