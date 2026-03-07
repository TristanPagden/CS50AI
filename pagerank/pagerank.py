import os
import random
import re
import sys

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
    Parse a directory of HTML pages_num and check for links to other pages_num.
    Return a dictionary where each key is a page, and values are
    a list of all other pages_num in the corpus that are linked to by the page.
    """
    pages_num = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages_num[filename] = set(links) - {filename}

    # Only include links to other pages_num in the corpus
    for filename in pages_num:
        pages_num[filename] = set(
            link for link in pages_num[filename] if link in pages_num
        )

    return pages_num


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages_num in the corpus.
    """

    distribution = {name: 0 for name in corpus}

    if len(corpus[page]) == 0:
        for name in distribution:
            distribution[name] = 1 / len(corpus)
        return distribution

    random_probability = (1 - damping_factor) / len(corpus)

    link_probability = damping_factor / len(corpus[page])

    for name in distribution:
        distribution[name] += random_probability

        if name in corpus[page]:
            distribution[name] += link_probability

    return distribution


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages_num
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """

    visited = {name: 0 for name in corpus}

    current = random.choice(list(visited))
    visited[current] += 1

    for i in range(0, n - 1):
        model = transition_model(corpus, current, damping_factor)

        rand = random.random()
        total_probability = 0

        for name, probability in model.items():
            total_probability += probability
            if rand <= total_probability:
                current = name
                break

        visited[current] += 1

    rank_pages = {name: (visit_num / n) for name, visit_num in visited.items()}

    return rank_pages


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """

    pages_num = len(corpus)
    first_rank = 1 / pages_num
    random_choice_prob = (1 - damping_factor) / len(corpus)
    iterations = 0

    rank_pages = {name: first_rank for name in corpus}
    rank_new_pages = {name: None for name in corpus}
    maximun_change = first_rank

    while maximun_change > 0.001:
        iterations += 1
        maximun_change = 0

        for name in corpus:
            surf_prob = 0
            for other in corpus:
                if len(corpus[other]) == 0:
                    surf_prob += rank_pages[other] * first_rank

                elif name in corpus[other]:
                    surf_prob += rank_pages[other] / len(corpus[other])

            new_rank = random_choice_prob + (damping_factor * surf_prob)
            rank_new_pages[name] = new_rank

        norm = sum(rank_new_pages.values())
        rank_new_pages = {page: (rank / norm) for page, rank in rank_new_pages.items()}

        for name in corpus:
            rank_change = abs(rank_pages[name] - rank_new_pages[name])
            if rank_change > maximun_change:
                maximun_change = rank_change

        rank_pages = rank_new_pages.copy()

    return rank_pages


if __name__ == "__main__":
    main()
