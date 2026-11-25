import datetime
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "TP4")))

import Corpus
import Document


def main() -> None:
	hackernews = Document.HackerNewsDocument(
		"Wolves in the news",
		"Alice",
		datetime.date(2026, 11, 20),
		"https://news.example/wolves",
		"Une discussion concernant les loups.",
		nb_comments=12,
	)

	arxiv = Document.ArxivDocument(
		"Wolves and ecosystems",
		"Bob",
		datetime.date(2026, 11, 21),
		"https://arxiv.example/wolves",
		"Un article scientifique sur les ecosystemes.",
		co_auteurs=["Carol", "Dave"],
	)

	corpus = Corpus.Corpus("Corpus wolves")
	corpus.addDocument(hackernews)
	corpus.addDocument(arxiv)

	print(corpus)
	corpus.showBySource(10)

	print("Singleton:", corpus is Corpus.Corpus("Autre nom"))

	doc_create = Document.DocumentFactory.create(
		"hacker-news",
		"Document cree par l'usine",
		"Eve",
		datetime.date(2026, 11, 22),
		"https://news.example/factory",
		"Texte produit par l'usine.",
		nb_comments=3,
	)
	corpus.addDocument(doc_create)

	save_path = os.path.join(os.path.dirname(__file__), "corpus_tp5.csv")
	corpus.save(save_path)

	corpus_charge = Corpus.Corpus("Corpus temporaire")
	corpus_charge.load(save_path)
	print("Documents charges:")
	corpus_charge.showBySource(10)


if __name__ == "__main__":
	main()
