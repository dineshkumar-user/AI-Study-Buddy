import re

from sklearn.feature_extraction.text import TfidfVectorizer


def clean_text(text):
    text = text.lower()
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def split_sentences(text):
    sentences = re.split(
        r"(?<=[.!?])\s+",
        text
    )

    return [
        sentence.strip()
        for sentence in sentences
        if len(sentence.strip()) > 20
    ]


def tfidf_summary(text, number_of_sentences=5):

    sentences = split_sentences(text)

    if not sentences:
        return []

    if len(sentences) <= number_of_sentences:
        return sentences

    cleaned = [
        clean_text(sentence)
        for sentence in sentences
    ]

    vectorizer = TfidfVectorizer(
        stop_words="english"
    )

    matrix = vectorizer.fit_transform(cleaned)

    scores = matrix.sum(axis=1).A1

    ranked = scores.argsort()[
        -number_of_sentences:
    ][::-1]

    selected = sorted(ranked)

    return [
        sentences[index]
        for index in selected
    ]