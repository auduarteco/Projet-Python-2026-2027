import datetime

import Author
import Document


def main() -> None:

	id2doc: dict = dict()
	id2aut: dict = dict()
	nextID: int = 0

	document: Document.Document = Document.Document(
		"Exemple",
		"Aurélien Duarte Costa",
		datetime.date(2026, 11, 12),
		"http://example.net/article",
		"Contenu du document."
	)

	id2doc[nextID] = document
	if document.auteur not in id2aut:
		id2aut[document.auteur] = Author.Author(document.auteur, 0, dict())

	id2aut[document.auteur].add(document)
	nextID += 1

	print(id2doc)
	print(id2aut)
	print(id2doc[0].titre)

	statistiquesAuteur: str = input("Nom de l'auteur : ")
	documentsAuteur: list[Document.Document] = list(
		document for document in id2doc.values() if document.auteur == statistiquesAuteur
	)
	nbDocuments: int = len(documentsAuteur)
	tailleMoyenne: float = (
		(sum(len(document.texte) for document in documentsAuteur) / nbDocuments)
		if nbDocuments else 0.0
	)

	print("Nombre de documents produits :", nbDocuments)
	print("Taille moyenne des documents (en nombre de caractères) :", tailleMoyenne)


if __name__ == "__main__": main()
