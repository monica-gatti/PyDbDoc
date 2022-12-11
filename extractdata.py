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
print("Damien Chablat")
# afficher le nombre d'articles qui n'ont pas été publiés par "Damien Chablat"

for r in list(arxiv.papers.find({'authors':{'$regex':'%Damien'}})):
    print(r)

# for r in list( arxiv.papers.find( {"authors": {'$regex': '%Damien%', "$options" :'i' } })):
#     print(r)
