
from math import log10 as _log10
# from pagerank_weighted import pagerank_weighted_scipy as _pagerank
from textcleaner import clean_text_by_sentences as _clean_text_by_sentences
from graph import build_graph as _build_graph
from graph import remove_unreachable_nodes as _remove_unreachable_nodes

from scipy.sparse import csr_matrix
from scipy.linalg import eig
from numpy import empty as empty_matrix



def pagerank_weighted_scipy(graph, damping=0.85):
    adjacency_matrix = build_adjacency_matrix(graph)
    probability_matrix = build_probability_matrix(graph)

    pagerank_matrix = damping * adjacency_matrix.todense() + (1 - damping) * probability_matrix
    vals, vecs = eig(pagerank_matrix, left=True, right=False)
    return process_results(graph, vecs)


def build_adjacency_matrix(graph):
    # print "Called build adj mat!!"

    row = []
    col = []
    data = []
    nodes = graph.nodes()
    length = len(nodes)

    for i in xrange(length):
        current_node = nodes[i]
        neighbors_sum = sum(graph.edge_weight((current_node, neighbor)) for neighbor in graph.neighbors(current_node))
        for j in xrange(length):
            edge_weight = float(graph.edge_weight((current_node, nodes[j])))
            if i != j and edge_weight != 0:
                row.append(i)
                col.append(j)
                data.append(edge_weight / neighbors_sum)

    return csr_matrix((data,(row,col)), shape=(length,length))


def build_probability_matrix(graph):
    # print "Called Build prob mat!!"

    dimension = len(graph.nodes())
    matrix = empty_matrix((dimension,dimension))

    probability = 1 / float(dimension)
    matrix.fill(probability)

    return matrix


def process_results(graph, vecs):
    # print "Called Proc res!!"
    scores = {}
    for i, node in enumerate(graph.nodes()):
        scores[node] = abs(vecs[i][0])

    return scores




def _set_graph_edge_weights(graph):
    # print "Called set graph edge weights!!!"
    for sentence_1 in graph.nodes():
        for sentence_2 in graph.nodes():

            edge = (sentence_1, sentence_2)
            if sentence_1 != sentence_2 and not graph.has_edge(edge):
                similarity = _get_similarity(sentence_1, sentence_2)
                if similarity != 0:
                    graph.add_edge(edge, similarity)

# #similarity from summa
def _get_similarity(s1, s2):
    # print "Called get similarity!!!"

    words_sentence_one = s1.split()
    words_sentence_two = s2.split()

    common_word_count = _count_common_words(words_sentence_one, words_sentence_two)

    log_s1 = _log10(len(words_sentence_one))
    log_s2 = _log10(len(words_sentence_two))

    if log_s1 + log_s2 == 0:
        return 0

    return common_word_count / (log_s1 + log_s2)


#Jaccard similarity
# def _get_similarity(s1, s2):
#     # print "Called get similarity!!!"

#     words_sentence_one = s1.split()
#     words_sentence_two = s2.split()

#     common_word_count = _count_common_words(words_sentence_one, words_sentence_two)
#     all_word_count = _count_all_words(words_sentence_one, words_sentence_two)


#     if all_word_count == 0:
#         return 0
#     return common_word_count / all_word_count



def _count_common_words(words_sentence_one, words_sentence_two):
    # print "Called count common words!!!"
    return len(set(words_sentence_one) & set(words_sentence_two))

# def _count_all_words(words_sentence_one, words_sentence_two):
#     # print "Called count common words!!!"
#     return len(set(words_sentence_one) | set(words_sentence_two))


def _format_results(extracted_sentences, split, score):
    # print "Called format results!!!"
    if score:
        return [(sentence.text, sentence.score) for sentence in extracted_sentences]
    if split:
        return [sentence.text for sentence in extracted_sentences]
    return "\n".join([sentence.text for sentence in extracted_sentences])


def _add_scores_to_sentences(sentences, scores):
    # print "Called add score to sentences!!!"
    for sentence in sentences:
        # Adds the score to the object if it has one.
        if sentence.token in scores:
            sentence.score = scores[sentence.token]
        else:
            sentence.score = 0




def _extract_most_important_sentences(sentences, ratio, words):
    # print "Called extract imp sent!!!"
    sentences.sort(key=lambda s: s.score, reverse=True)

    # If no "words" option is selected, the number of sentences is
    # reduced by the provided ratio.
    if words is None:
        length = len(sentences) * ratio
        return sentences[:int(length)]

    # Else, the ratio is ignored.
    else:
        return _get_sentences_with_word_count(sentences, words)


def summarize(text, ratio=0.2, words=None, language="english", split=False, scores=False):
    print "Called summarize!!"

    # Gets a list of processed sentences.
    sentences = _clean_text_by_sentences(text, language)

    # Creates the graph and calculates the similarity coefficient for every pair of nodes.
    graph = _build_graph([sentence.token for sentence in sentences])
    _set_graph_edge_weights(graph)

    # Remove all nodes with all edges weights equal to zero.
    _remove_unreachable_nodes(graph)

    # Ranks the tokens using the PageRank algorithm. Returns dict of sentence -> score
    # pagerank_scores = _pagerank(graph)
    pagerank_scores = pagerank_weighted_scipy(graph)

    # Adds the summa scores to the sentence objects.
    _add_scores_to_sentences(sentences, pagerank_scores)

    # Extracts the most important sentences with the selected criterion.
    extracted_sentences = _extract_most_important_sentences(sentences, ratio, words)

    # Sorts the extracted sentences by apparition order in the original text.
    extracted_sentences.sort(key=lambda s: s.index)

    return _format_results(extracted_sentences, split, scores)



