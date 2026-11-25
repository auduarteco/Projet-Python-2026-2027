import datetime
import json

class Document:

	def __init__(self, titre: str, auteur: str, date: datetime.date, url: str, texte: str, type: str = "Document") -> None:
		self.titre: str = titre
		self.auteur: str = auteur
		self.date: datetime.date = date
		self.url: str = url
		self.texte: str = texte
		self.type: str = type

	def afficherInformations(self) -> None:
		"""Affiche les informations du document."""
		print("Titre :", self.titre)
		print("Auteur :", self.auteur)
		print("Date :", self.date)
		print("URL :", self.url)
		print("Texte :", self.texte)

	def getType(self) -> str:
		return self.type

	def __str__(self) -> str: return self.titre


class HackerNewsDocument(Document):

	def __init__(
		self,
		titre: str,
		auteur: str,
		date: datetime.date,
		url: str,
		texte: str,
		nb_comments: int = 0,
	) -> None:
		super().__init__(titre, auteur, date, url, texte, "Hacker News")
		self.nb_comments: int = nb_comments
		self.commentaires: int = nb_comments

	def getNbComments(self) -> int:
		return self.nb_comments

	def setNbComments(self, nb_comments: int) -> None:
		self.nb_comments = nb_comments
		self.commentaires = nb_comments

	def getType(self) -> str:
		return "Hacker News"

	def __str__(self) -> str:
		return "%s (%d commentaires)" % (self.titre, self.nb_comments)


class ArxivDocument(Document):

	def __init__(
		self,
		titre: str,
		auteur: str,
		date: datetime.date,
		url: str,
		texte: str,
		co_auteurs: list[str] | None = None,
	) -> None:
		super().__init__(titre, auteur, date, url, texte, "Arxiv")
		self.co_auteurs: list[str] = co_auteurs if co_auteurs is not None else []
		self.coauthors: list[str] = self.co_auteurs

	def getCoAuteurs(self) -> list[str]:
		return self.co_auteurs

	def setCoAuteurs(self, co_auteurs: list[str]) -> None:
		self.co_auteurs = co_auteurs
		self.coauthors = co_auteurs

	def getType(self) -> str:
		return "Arxiv"

	def __str__(self) -> str:
		co_auteurs = ", ".join(self.co_auteurs)
		suffix = " [co-auteurs : %s]" % co_auteurs if co_auteurs else ""
		return "%s%s" % (self.titre, suffix)


class DocumentFactory:

	@staticmethod
	def create(
		document_type: str,
		titre: str,
		auteur: str,
		date: datetime.date,
		url: str,
		texte: str,
		**kwargs,
	) -> Document:
		source = document_type.strip().lower().replace("_", "").replace("-", "")
		if source in ("hackernews", "hacker"):
			return HackerNewsDocument(
				titre,
				auteur,
				date,
				url,
				texte,
				int(kwargs.get("nb_comments", kwargs.get("commentaires", 0))),
			)
		if source == "arxiv":
			co_auteurs = kwargs.get("co_auteurs", kwargs.get("coauthors", []))
			if isinstance(co_auteurs, str):
				try:
					parsed = json.loads(co_auteurs)
					co_auteurs = parsed if isinstance(parsed, list) else co_auteurs
				except json.JSONDecodeError:
					co_auteurs = [name.strip() for name in co_auteurs.split(",") if name.strip()]
			return ArxivDocument(titre, auteur, date, url, texte, list(co_auteurs))
		return Document(titre, auteur, date, url, texte)

	createDocument = create


def create_document(
	document_type: str,
	titre: str,
	auteur: str,
	date: datetime.date,
	url: str,
	texte: str,
	**kwargs,
) -> Document:
	return DocumentFactory.create(document_type, titre, auteur, date, url, texte, **kwargs)
