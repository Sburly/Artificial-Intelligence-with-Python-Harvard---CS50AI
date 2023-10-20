import nltk
import sys
import os
import string
import math

FILE_MATCHES = 1
SENTENCE_MATCHES = 1


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python questions.py corpus")

    # Calculate IDF values across files
    files = load_files(sys.argv[1])
    file_words = {
        filename: tokenize(files[filename])
        for filename in files
    }
    file_idfs = compute_idfs(file_words)

    # Prompt user for query
    query = set(tokenize(input("Query: ")))

    # Determine top file matches according to TF-IDF
    filenames = top_files(query, file_words, file_idfs, n=FILE_MATCHES)

    # Extract sentences from top files
    sentences = dict()
    for filename in filenames:
        for passage in files[filename].split("\n"):
            for sentence in nltk.sent_tokenize(passage):
                tokens = tokenize(sentence)
                if tokens:
                    sentences[sentence] = tokens

    # Compute IDF values across sentences
    idfs = compute_idfs(sentences)

    # Determine top sentence matches
    matches = top_sentences(query, sentences, idfs, n=SENTENCE_MATCHES)
    for match in matches:
        print(match)


def load_files(directory):
    """
    Given a directory name, return a dictionary mapping the filename of each
    `.txt` file inside that directory to the file's contents as a string.
    """
    result = dict()
    for file in os.listdir(directory):
        if file.endswith('.txt'):
            with open(path := os.path.join(directory, file), encoding='utf-8') as f:
                result[file] = f.read()
    return result


def tokenize(document):
    """
    Given a document (represented as a string), return a list of all of the
    words in that document, in order.

    Process document by coverting all words to lowercase, and removing any
    punctuation or English stopwords.
    """
    stopwords = nltk.corpus.stopwords.words("english")
    return [token for token in nltk.tokenize.word_tokenize(document.lower()) if token not in string.punctuation and token not in stopwords]


def compute_idfs(documents):
    """
    Given a dictionary of `documents` that maps names of documents to a list
    of words, return a dictionary that maps words to their IDF values.

    Any word that appears in at least one of the documents should be in the
    resulting dictionary.
    """
    total_words = {word: 0 for word in {word for doc in documents.values() for word in doc}}
    for doc in documents.values():
        for word in set(doc):
            total_words[word] += 1
    return {word: math.log(len(documents) / count) for word, count in total_words.items()}


def top_files(query, files, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the filenames of the the `n` top
    files that match the query, ranked according to tf-idf.
    """
    ranked_files = {}
    for doc, words in files.items():
        word_counts = {word: words.count(word) for word in words if word in idfs}
        tf_idfs = {word: count * idfs[word] for word, count in word_counts.items() if word in query}
        file_tfidfs = sum(tf_idfs.values())
        if file_tfidfs:
            ranked_files[doc] = file_tfidfs
    return sorted(ranked_files, key=ranked_files.get, reverse=True)[:n]


def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping
    sentences to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the `n` top sentences that match
    the query, ranked according to idf. If there are ties, preference should
    be given to sentences that have a higher query term density.
    """
    ranked_sentences = {}
    for sen, words in sentences.items():
        matching_word_measure = sum([idfs.get(word, 0) for word in query if word in words])
        if matching_word_measure:
            query_term_density = sum([words.count(word) for word in query if word in idfs]) / len(words)
            ranked_sentences[sen] = (matching_word_measure, query_term_density)
    return sorted(ranked_sentences, key=lambda x: (ranked_sentences[x][0], ranked_sentences[x][1]), reverse=True)[:n]


if __name__ == "__main__":
    main()
