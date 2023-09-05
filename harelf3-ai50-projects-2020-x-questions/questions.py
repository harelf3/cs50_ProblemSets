
import nltk
import sys

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
    # dont know if can import os i think there is no probleam because they want tio use os.path
    ### 
    import os
    data_dict = dict()
    for file in os.listdir(directory):
        with open(os.path.join(directory,file), 'r', encoding="utf8") as f:
            z = f.read()
            data_dict[file] =z 

    return data_dict


def tokenize(document):
    """
    Given a document (represented as a string), return a list of all of the
    words in that document, in order.

    Process document by coverting all words to lowercase, and removing any
    punctuation or English stopwords.
    """
    ###
    # we have still === and == and "" inside see if it matters
    import string
    document =document.lower()
    document_list = nltk.tokenize.word_tokenize(document)
    document_list_copy = document_list.copy()
    for word in document_list:
        if word in string.punctuation or word in nltk.corpus.stopwords.words("english"):
            document_list_copy.remove(word)
    
    return document_list_copy


def compute_idfs(documents):
    """
    Given a dictionary of `documents` that maps names of documents to a list
    of words, return a dictionary that maps words to their IDF values.

    Any word that appears in at least one of the documents should be in the
    resulting dictionary.
    """
    # again dont know if i can do this 
    ###
    import math
    count_in_document = dict()
    for file_name in documents:
        max = len(documents)
        list =[]
        for word in documents[file_name]:
            if word in list:
                continue
            try:
                count_in_document[word]+= 1
            except:
                count_in_document[word] =1
            list.append(word)
    all_docs =len(documents)
    for new_word in count_in_document:
        divide = count_in_document[new_word]
        new_div =all_docs/divide
        count_in_document[new_word] = math.log(new_div)
        
    return count_in_document

def top_files(query, files, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the filenames of the the `n` top
    files that match the query, ranked according to tf-idf.
    """
    ###
    # scores[0] = files[0]
    scores =[]
    file_names =[]
    for file in files:
        file_score =[]
        word_counter = dict()
        for word in files[file]:
            try:
                word_counter[word] +=1
            except:
                word_counter[word]= 1
        for word in query:
            try:
                file_score.append(word_counter[word]*idfs[word])
            except:
                pass
        scores.append(sum(file_score))
        file_names.append(file)
    orders =[]
    for i in range(n) :
        best = max(scores)
        index = scores.index(best)
        orders.append(file_names[index])
    return orders

        

def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping
    sentences to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the `n` top sentences that match
    the query, ranked according to idf. If there are ties, preference should
    be given to sentences that have a higher query term density.
    """
    sentences_score = []
    sentences_names= []
    for sentence in sentences:
        sentence_score = 0
        for word in sentences[sentence]:
            if word in query:
                sentence_score += idfs[word]
        sentences_score.append(sentence_score)
        sentences_names.append(sentence)
    orders =[]
    for i in range(n) :
        best = max(sentences_score)
        dubble = [z for z,val in enumerate(sentences_score) if val==best]
        # this means tie >>
        if len(dubble) ==1:
            rank = []
            name =[]
            for i in dubble:
                sen = sentences_names[i]
                sentence_value = 0
                for word in query:
                    if word in sen:
                        sentence_value +=1
                sentence_value = sentence_value/10
                rank.append(sentence_value)
                name.append(sen)
            gtf_winner = rank.index(max(rank))
            gtf_winner_name = name[gtf_winner]
            orders.append(gtf_winner_name)
            if n == len(orders):
                return orders
        index = sentences_score.index(best)
        orders.append(sentences_names[index])
    return orders


if __name__ == "__main__":
    main()
