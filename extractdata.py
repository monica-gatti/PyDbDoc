from pymongo import MongoClient
from pprint import pprint
import re

full_dns_name = 'mongodb://ec2-54-229-30-76.eu-west-1.compute.amazonaws.com:27017'
username = 'test'
password = 'test'
authSource = 'admin'

client = MongoClient(host=full_dns_name, username=username, password=password, authSource=authSource)

#afficher la liste des bases de données disponibles
print( "\n*********(b)afficher la liste des bases de données disponibles:", client.list_database_names())

#afficher la liste des collections disponibles dans cette base de données
arxiv = client["arxiv"]
print("\n*********(c)afficher la liste des collections disponibles dans cette base de données", arxiv.list_collection_names())

#afficher un des documents de cette collection
print("\n*********(d)afficher un des documents de cette collection")
pprint(arxiv.papers.find_one())

#afficher le nombre de documents dans cette collection
print("\n*********(e)afficher le nombre de documents dans cette collection:", arxiv.papers.count_documents({}))


print("\n*********(a)afficher le titre de 10 articles \n:")
for t in list(arxiv.papers.find({},{"title":1, "_id":0}).limit(10)):
    print(t)
print("\n*********(b)afficher les 10 premiers auteurs par ordre alphabétique \n")
for a in list( arxiv.papers.find({},{"authors":1, "_id":0}).sort("authors", 1).limit(10)):
    print(a)

# afficher le nombre d'articles qui n'ont pas été publiés par "Damien Chablat"
print("\n*********(c)afficher le nombre d'articles qui n'ont pas été publiés par Damien Chablat:", arxiv.papers.count_documents({'submitter':{'$ne':'Damien Chablat'}}))

# afficher le nombre de papiers téléversés en 2014. On pourra s'appuyer sur une expréssion régulière.
print("\n*********(d)afficher le nombre de papiers téléversés en 2014:", arxiv.papers.count_documents({'update_date':{'$regex':'^2014'}}))

#afficher le titre d'un article qui contient l'expression Machine Learning. On pourra utiliser une expression régulière.
print("\n*********(e)afficher le titre d'un article qui contient l'expression Machine Learning:", arxiv.papers.find_one({"title" : {'$regex':'Machine Learning'}},{"title":1, "_id":0}))

#afficher le nombre de publications par submitter pour les 10 personnes les plus prolifiques. 
# On pourra utiliser un pipeline d'aggrégation avec les mots-clefs $group, $sort, $limit.
print("\n*********(f)afficher le nombre de publications par submitter pour les 10 personnes les plus prolifiques.")
for v in list(arxiv.papers.aggregate([{"$group" :{"_id":"$submitter", "np":{"$sum" : 1 }}}, {"$sort" : {"np":-1}}, {"$limit" : 10}])):
    print(v)