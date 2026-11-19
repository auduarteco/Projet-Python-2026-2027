import Document

class Author:

	def __init__(self, name: str, ndoc: int, production: dict[int, Document.Document]) -> None:
		self.name: str = name
		self.ndoc: int = ndoc
		self.production: dict[int, Document.Document] = production

	def add(self, document: Document.Document) -> None:
		"""
		Ajoute un document à la production de l'auteur.

		@param document: Le document à ajouter.
		"""
		self.production[self.ndoc] = document
		self.ndoc += 1

	def __str__(self) -> str:
		return "Auteur : %s, Nombre de documents : %d, Production : %s" % (self.name, self.ndoc, self.production)
