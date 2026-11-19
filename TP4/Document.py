import datetime

class Document:

	def __init__(self, titre: str, auteur: str, date: datetime.date, url: str, texte: str) -> None:
		self.titre: str = titre
		self.auteur: str = auteur
		self.date: datetime.date = date
		self.url: str = url
		self.texte: str = texte

	def afficherInformations(self) -> None:
		"""Affiche les informations du document."""
		print("Titre :", self.titre)
		print("Auteur :", self.auteur)
		print("Date :", self.date)
		print("URL :", self.url)
		print("Texte :", self.texte)

	def __str__(self) -> str: return self.titre
