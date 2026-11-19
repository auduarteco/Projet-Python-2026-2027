import html
import json
import urllib.parse
import urllib.request

import pandas as pd
import xmltodict


def main() -> None:

	# Partie 1 : chargement des données

	theme: str = "wolves"
	docs: list = list()
	origines: list = list()

	# 1.1

	# Construction de l'adresse URL de l'IPA de Hacker News
	urlHN: str = "https://hn.algolia.com/api/v1/search?" + urllib.parse.urlencode(
		dict(query = theme, tags = "story", hitsPerPage = 50)
	)
	print(urlHN)

	# Chargement des données depuis l'IPA de Hacker News
	with urllib.request.urlopen(urlHN) as response:
		dataHN: dict = json.load(response)

	# Affichage des informations sur les données récupérées
	print(dataHN.keys())
	print(dataHN["nbHits"])
	hits: list = dataHN["hits"]
	print(len(hits))
	print(hits[0].keys())

	# Récupération du contenu textuel des documents
	for i in range(len(hits)):
		hit: dict = hits[i]
		text: str = hit.get("story_text") # type: ignore
		if not text: text = hit.get("title", "")
		text: str = html.unescape(text).replace("<p>", " ").strip()
		docs.append(text)
		origines.append("hackernews")

	# Affichage du nombre de documents récupérés
	print("Documents Hacker News :", len(docs))

	# 1.2

	# Construction de l'adresse URL de l'IPA d'arXiv
	urlArxiv: str = "http://export.arxiv.org/api/query?" + urllib.parse.urlencode(
		dict(search_query = "all:" + theme, start = 0, max_results = 50)
	)
	print(urlArxiv)

	# Chargement des données depuis l'IPA d'arXiv
	with urllib.request.urlopen(urlArxiv) as response:
		dataArxiv: dict = xmltodict.parse(response.read())

	# Affichage des informations sur les données récupérées
	print(dataArxiv.keys())
	print(dataArxiv["feed"].keys())

	entrees: list = dataArxiv["feed"].get("entry", [])
	if isinstance(entrees, dict): entrees = [entrees]
	print(len(entrees))
	print(entrees[0].keys())

	for i in range(len(entrees)):
		entree: dict = entrees[i]
		text: str = entree["summary"].replace("\n", ' ').strip()
		docs.append(text)
		origines.append("arxiv")

	print("Taille du corpus :", len(docs))

	# Partie 2 : sauvegarde des données

	# 2.1) Création d'une trame de données à partir des documents récupérés
	dataFrame: pd.DataFrame = pd.DataFrame(
		dict(
			id = range(len(docs)),
			text = docs,
			origine = origines
		)
	)
	print(dataFrame.shape)
	print(dataFrame.head())
	print(dataFrame["origine"].value_counts())

	# 2.2) Sauvegarde de la trame de données dans un fichier TSV
	dataFrame.to_csv("corpus.csv", sep="\t", index=False)

	# 2.3) Chargement de la trame de données depuis le fichier TSV
	dataFrame = pd.read_csv("corpus.csv", sep="\t")
	print(dataFrame.shape)

	# Partie 3 : premières manipulations des données

	# 3.1) Affichage du nombre de documents dans la trame de données
	print("Nombre de documents :", len(dataFrame))

	# 3.2) Affichage du nombre de mots et de phrases pour chaque document
	for i in range(len(dataFrame)):
		text: str = str(dataFrame.loc[i, "text"])
		words = text.split(' ')
		sentences = text.split('.')
		print(len(words), "mots,", len(sentences), "phrases")

	# 3.3) Filtrage des documents trop courts (moins de 20 caractères)
	print("Avant filtrage :", len(dataFrame))
	dataFrame = dataFrame[dataFrame["text"].str.len() >= 20]
	print("Après filtrage :", len(dataFrame))

	# 3.4) Affichage des 500 premiers caractères du texte
	# concaténé de tous les documents
	string: str = ' '.join(dataFrame["text"])
	print(len(string))
	print(string[:500])


if __name__ == "__main__": main()
