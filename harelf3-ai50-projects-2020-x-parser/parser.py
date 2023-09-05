import nltk
import sys


TERMINALS = """
Adj -> "country" | "dreadful" | "enigmatical" | "little" | "moist" | "red"
Adv -> "down" | "here" | "never"
Conj -> "and" | "until"
Det -> "a" | "an" | "his" | "my" | "the"
N -> "armchair" | "companion" | "day" | "door" | "hand" | "he" | "himself"
N -> "holmes" | "home" | "i" | "mess" | "paint" | "palm" | "pipe" | "she"
N -> "smile" | "thursday" | "walk" | "we" | "word"
P -> "at" | "before" | "in" | "of" | "on" | "to"
V -> "arrived" | "came" | "chuckled" | "had" | "lit" | "said" | "sat"
V -> "smiled" | "tell" | "were"
"""



NONTERMINALS = """
S -> NP VP | NP VP Conj VP | S Conj S 
AP ->  Adj AP| Adj 
NP -> N | Det NP | NP PP | AP NP
PP -> P NP | P S
VP -> V | V NP | V PP | V NP PP | Adv VP | VP Adv 
"""

grammar = nltk.CFG.fromstring(NONTERMINALS + TERMINALS)
parser = nltk.ChartParser(grammar)


def main():

    # If filename specified, read sentence from file
    if len(sys.argv) == 2:
        with open(sys.argv[1]) as f:
            s = f.read()

    # Otherwise, get sentence as input
    else:
        s = input("Sentence: ")

    # Convert input into list of words
    s = preprocess(s)

    # Attempt to parse sentence
    try:
        trees = list(parser.parse(s))
    except ValueError as e:
        print(e)
        return
    if not trees:
        print("Could not parse sentence.")
        return

    # Print each tree with noun phrase chunks
    for tree in trees:
        tree.pretty_print()

        print("Noun Phrase Chunks")
        for np in np_chunk(tree):
            print(" ".join(np.flatten()))


def preprocess(sentence):
    """
    Convert `sentence` to a list of its words.
    Pre-process sentence by converting all characters to lowercase
    and removing any word that does not contain at least one alphabetic
    character.
    """
    ###
    token_list = nltk.tokenize.word_tokenize(sentence)
    copy_list = token_list.copy()
    for word in range(len(copy_list)):
        copy_list[word] = copy_list[word].lower()
        if not copy_list[word].isalpha():
            copy_list.remove(copy_list[word]) 
    return copy_list



def np_chunk(tree):
    """
    Return a list of all noun phrase chunks in the sentence tree.
    A noun phrase chunk is defined as any subtree of the sentence
    whose label is "NP" that does not itself contain any other
    noun phrases as subtrees.
    """
    np_list = []
    np_set =set()
    # we want a recursion that when len is 1 will start checking and only for each sub tree its like a 
    # reverse search 
    """ for hight in range(tree.height()):
        for s in tree.subtrees(lambda tree: tree.height() == hight):
            if s.label() =="NP" :
                # we know the hight is 7 
                np_list.append(s.leaves())
    print(np_list)  """               
    for h in range(tree.height()):
        for s in tree.subtrees(lambda tree:tree.height()==h):
            if s.label() == 'NP' and not list(s.subtrees(lambda t: t.label() == 'NP' and t != s)):
                np_list.append(s)
    return np_list



if __name__ == "__main__":
    main()
