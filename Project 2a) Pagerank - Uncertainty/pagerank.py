import os
import random
import re
import sys
import copy

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    { 1.html: [2.hmlt, 3.html] }
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    if corpus[page] == {}:
        return {key : 1/len(list(corpus.keys())) for key in list(corpus.keys())}
    # Spread the "1 - damping_factor" among a list of all the pages in the corpus:
    distribution = {key : (1 - damping_factor)/len(list(corpus.keys())) for key in list(corpus.keys())}
    for key, value in distribution.items():
        if key in corpus[page]:
            distribution[key] = value + (damping_factor/len(corpus[page])) # Probability of each link to be chosen
    return distribution


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    extractions = []
    for sample in range(n):
        if len(extractions) == 0:
            extractions.append(random.choice(list(corpus.keys())))
        else:
            distribution = transition_model(corpus, extractions[-1], damping_factor) # Get the distribution for the last extraction
            new_page = random.choices(list(distribution.keys()), list(distribution.values()))[0]
            extractions.append(new_page)
    return {key : extractions.count(key)/n for key in list(corpus.keys())}


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    pagerank = {key : 1/len(corpus) for key in list(corpus.keys())} # Start by ranking each page with 1/N
    while True:
        old_pagerank = copy.deepcopy(pagerank)
        for page in pagerank.keys():
            random_choice = (1-damping_factor)/len(corpus)
            linked_pages = {key : len(values) for key, values in corpus.items() if page in values} # We get a dictionary with all the pages that link to page as keys and the number of links they have as values
            pagerank[page] = random_choice + damping_factor * sum([pagerank[key]/num_links for key, num_links in linked_pages.items()])
        if all(abs(rank - old_pagerank[page]) < 0.001 for page, rank in pagerank.items()):
            break
    return pagerank

if __name__ == "__main__":
    main()
