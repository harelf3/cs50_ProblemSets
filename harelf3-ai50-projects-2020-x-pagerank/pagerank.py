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
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
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
    # if page has no links 
    # else
    probabilidict = dict() 
    linkss =len(corpus[page])
    if linkss == 0:
        n = len(corpus)
        for link in corpus:
            probabilidict[link] = 1/n
    else:
        links = corpus[page]
        for link in corpus:
            probabilidict[link] = (1-damping_factor)/len(corpus)
            if link in links:
                probabilidict[link] += damping_factor/len(links)
    return probabilidict


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    probabilidict =dict()
    z =list(corpus.keys())
    current = random.choice(z)
    for page in corpus:
        probabilidict[page] = 0
    probabilidict[current] +=1
    count = 1
    while count < n :
        probabilities = transition_model(corpus,current,damping_factor)
        pages= []
        probability = []
        for link in probabilities:
            pages.append(link)
            probability.append(probabilities[link])
        current = random.choices(pages,weights=probability)
        current = current[0]
        probabilidict[current] +=1
        count +=1

    
    for links in probabilidict:
        probabilidict[links] = probabilidict[links]/n
    return probabilidict

    


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    # works #
    # getting the amount of files we have to mess with 
    n = len(corpus) 
    # we are getting a list so we can store all corpus values 
    page_count = {}
    # we run through all corpus values and get a list of them and add them to dictionary 
    for pages in corpus:
        page_count[pages] =1/n
    stop = 0.0005
    while True:
        count = 0
        for key in corpus:
            # we calculate the first half of the equation 
            start = (1 - damping_factor) / n
            probability = 0
            # this is the sigma we iterate over with page beeing i 
            for page in corpus:
                # we check if our file is in the links if yes we know that this is his parent 
                if key in corpus[page]:
                    num_links = len(corpus[page])
                    # adding the sigma probability after we went over all of the options we can be sure he 
                    # dosent have more parents
                    probability = probability + page_count[page] / num_links
            probability = damping_factor * probability
            start += probability
            if abs(page_count[key] - start) < stop:
                count += 1
            page_count[key] = start
        if count == n:
            break
    return page_count


if __name__ == "__main__":
    main()
