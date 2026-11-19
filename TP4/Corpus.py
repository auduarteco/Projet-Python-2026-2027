import pandas as pd

import Author
import Document


class Corpus:

	def __init__(self, nom: str) -> None:
		self.nom: str = nom
		self.authors: dict = dict()
		self.id2doc: dict = dict()
		self.ndoc: int = 0
		self.naut: int = 0


	def addDocument(self, document: Document.Document) -> None:
		"""
		Ajoute un document au corpus et met à jour les informations sur l'auteur.

		@param document: Le document à ajouter au corpus.
		"""

		# Ajout du document au corpus
		self.id2doc[self.ndoc] = document
		self.ndoc += 1

		# Gestion de l'auteur
		author: str = document.auteur
		if author not in self.authors:
			self.authors[author] = Author.Author(author, 0, dict())
			self.naut += 1
		self.authors[author].add(document)


	def showByTitle(self, n: int) -> None:
		"""
		Affiche les n premiers documents du corpus triés par titre.

		@param n: Le nombre de documents à afficher.
		"""

		documents: list[Document.Document] = sorted(
			self.id2doc.values(),
			key=lambda document: document.titre.lower()
		)

		for i in range(min(n, len(documents))):
			document: Document.Document = documents[i]
			print(document)


	def showByDate(self, n: int) -> None:
		"""
		Affiche les n premiers documents du corpus triés par date.

		@param n: Le nombre de documents à afficher.
		"""

		documents: list[Document.Document] = sorted(
			self.id2doc.values(),
			key=lambda document: document.date
		)

		for i in range(min(n, len(documents))):
			document: Document.Document = documents[i]
			print(document)


	def __repr__(self) -> str:
		"""
		Renvoie une représentation textuelle du corpus, incluant son nom, le nombre de documents et le nombre d'auteurs.
		
		@return: Une chaîne de caractères représentant le corpus.
		"""
		return(
			"Corpus : %s\n" % self.nom +
			"Nombre de documents : %d\n" % self.ndoc +
			"Nombre d'auteurs : %d\n" % self.naut
		)


	def save(self, fileName: str) -> None:
		"""
		Sauvegarde le corpus dans un fichier CSV.

		@param fileName: Le nom du fichier dans lequel sauvegarder le corpus.
		"""

		data: list = list()

		for i in range(self.ndoc):
			document: Document.Document = self.id2doc[i]
			data.append({
				"titre": document.titre,
				"auteur": document.auteur,
				"date": document.date,
				"texte": document.texte
			})

		dataFrame: pd.DataFrame = pd.DataFrame(data)
		dataFrame.to_csv(fileName, index=False)


	def load(self, fileName: str):
		"""
		Charge le corpus à partir d'un fichier CSV.

		@param fileName: Le nom du fichier à partir duquel charger le corpus.
		"""

		dataFrame: pd.DataFrame = pd.read_csv(fileName)

		self.id2doc.clear()
		self.authors.clear()
		self.ndoc = self.naut = 0

		for i in range(len(dataFrame)):

			row: pd.Series = dataFrame.iloc[i]
			document: Document.Document = Document.Document(
				row["titre"],
				row["auteur"],
				row["date"],
				row["url"],
				row["texte"],
			)

			self.addDocument(document)
