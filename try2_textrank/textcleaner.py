# encoding: cp850

import string
import unicodedata
import logging
logger = logging.getLogger('summa.preprocessing.cleaner')

try:
    from pattern.en import tag
    logger.info("'pattern' package found; tag filters are available for English")
    HAS_PATTERN = True
except ImportError:
    logger.info("'pattern' package not found; tag filters are not available for English")
    HAS_PATTERN = False




from snowball import SnowballStemmer
# from stopwords import get_stopwords_by_language
import re  # http://regex101.com/#python to test regex
# from syntactic_unit import SyntacticUnit

SEPARATOR = r"@"
RE_SENTENCE = re.compile('(\S.+?[.!?])(?=\s+|$)|(\S.+?)(?=[\n]|$)')  # backup (\S.+?[.!?])(?=\s+|$)|(\S.+?)(?=[\n]|$)
AB_SENIOR = re.compile("([A-Z][a-z]{1,2}\.)\s(\w)")
AB_ACRONYM = re.compile("(\.[a-zA-Z]\.)\s(\w)")
AB_ACRONYM_LETTERS = re.compile("([a-zA-Z])\.([a-zA-Z])\.")
UNDO_AB_SENIOR = re.compile("([A-Z][a-z]{1,2}\.)" + SEPARATOR + "(\w)")
UNDO_AB_ACRONYM = re.compile("(\.[a-zA-Z]\.)" + SEPARATOR + "(\w)")


LANGUAGES = {"danish", "dutch", "english", "finnish", "french", "german", \
             "hungarian", "italian", "norwegian", "porter", "portuguese", \
             "romanian", "russian", "spanish", "swedish"}
STEMMER = None
STOPWORDS = None


def set_stemmer_language(language):
    # print "1"
    global STEMMER
    if not language in LANGUAGES:
        raise ValueError("Valid languages are danish, dutch, english, finnish," +
                 " french, german, hungarian, italian, norwegian, porter, portuguese," +
                 "romanian, russian, spanish, swedish")
    STEMMER = SnowballStemmer(language)


def set_stopwords_by_language(language):
    # print "2"

    global STOPWORDS
    words = get_stopwords_by_language(language)
    STOPWORDS = frozenset(w for w in words.split() if w)


def init_textcleanner(language):
    # print "3"

    set_stemmer_language(language)
    set_stopwords_by_language(language)


def split_sentences(text):
    # print "4"
    processed = replace_abbreviations(text)
    return [undo_replacement(sentence) for sentence in get_sentences(processed)]


def replace_abbreviations(text):
    # print "5"
    return replace_with_separator(text, SEPARATOR, [AB_SENIOR, AB_ACRONYM])


def undo_replacement(sentence):
    # print "6"
    return replace_with_separator(sentence, r" ", [UNDO_AB_SENIOR, UNDO_AB_ACRONYM])


def replace_with_separator(text, separator, regexs):
    # print "7"
    replacement = r"\1" + separator + r"\2"
    result = text
    for regex in regexs:
        result = regex.sub(replacement, result)
    return result


def get_sentences(text):
    # print "8"
    for match in RE_SENTENCE.finditer(text):
        yield match.group()


# Taken from gensim
def to_unicode(text, encoding='utf8', errors='strict'):
    """Convert a string (bytestring in `encoding` or unicode), to unicode."""
    # print "9"
    if isinstance(text, unicode):
        return text
    return unicode(text, encoding, errors=errors)


# Taken from gensim
RE_PUNCT = re.compile('([%s])+' % re.escape(string.punctuation), re.UNICODE)
def strip_punctuation(s):
    # print "10"
    s = to_unicode(s)
    return RE_PUNCT.sub(" ", s)


# Taken from gensim
RE_NUMERIC = re.compile(r"[0-9]+", re.UNICODE)
def strip_numeric(s):
    # print "11"
    s = to_unicode(s)
    return RE_NUMERIC.sub("", s)


def remove_stopwords(sentence):
    # print "12"
    return " ".join(w for w in sentence.split() if w not in STOPWORDS)


def stem_sentence(sentence):
    # print "13"
    word_stems = [STEMMER.stem(word) for word in sentence.split()]
    return " ".join(word_stems)


def apply_filters(sentence, filters):
    # print "14"
    for f in filters:
        sentence = f(sentence)
    return sentence


def filter_words(sentences):
    # print "15"
    filters = [lambda x: x.lower(), strip_numeric, strip_punctuation, remove_stopwords,
               stem_sentence]
    # filters = []

    apply_filters_to_token = lambda token: apply_filters(token, filters)
    return map(apply_filters_to_token, sentences)


def merge_syntactic_units(original_units, filtered_units, tags=None):
    # print "19"
    units = []
    for i in xrange(len(original_units)):
        if filtered_units[i] == '':
            continue

        text = original_units[i]
        token = filtered_units[i]
        tag = tags[i][1] if tags else None
        sentence = SyntacticUnit(text, token, tag)
        sentence.index = i

        units.append(sentence)

    return units


def clean_text_by_sentences(text, language="english"):
    """ Tokenizes a given text into sentences, applying filters and lemmatizing them.
    Returns a SyntacticUnit list. """
    # print "20"
    init_textcleanner(language)
    original_sentences = split_sentences(text)
    filtered_sentences = filter_words(original_sentences)

    return merge_syntactic_units(original_sentences, filtered_sentences)


# class SnowballStemmer():


#     languages = ("danish", "dutch", "english", "finnish", "french", "german",
#                  "hungarian", "italian", "norwegian", "porter", "portuguese",
#                  "romanian", "russian", "spanish", "swedish")

#     def __init__(self, language):
#         if language not in self.languages:
#             raise ValueError("The language '%s' is not supported." % language)
#         stemmerclass = globals()[language.capitalize() + "Stemmer"]
#         self.stemmer = stemmerclass()
#         self.stem = self.stemmer.stem

class SyntacticUnit(object):

    def __init__(self, text, token=None, tag=None):
        # print "Called syntactic init!!!"
        self.text = text
        self.token = token
        self.tag = tag[:2] if tag else None # just first two letters of tag
        self.index = -1
        self.score = -1

# encoding: UTF-8

english = """
all six eleven just less being indeed over both anyway detail four front already through yourselves fify
mill still its before move whose one system also somewhere herself thick show had enough should to only
seeming under herein ours two has might thereafter do them his around thereby get very de none cannot
every whether they not during thus now him nor name regarding several hereafter did always cry whither
beforehand this someone she each further become thereupon where side towards few twelve because often ten
anyhow doing km eg some back used go namely besides yet are cant our beyond ourselves sincere out even
what throughout computer give for bottom mine since please while per find everything behind does various
above between kg neither seemed ever across t somehow be we who were sixty however here otherwise whereupon
nowhere although found hers re along quite fifteen by on about didn last would anything via of could thence
put against keep etc s became ltd hence therein onto or whereafter con among own co afterwards formerly
within seems into others whatever yourself down alone everyone done least another whoever moreover couldnt
must your three from her their together top there due been next anyone whom much call too interest thru
themselves hundred was until empty more himself elsewhere mostly that fire becomes becoming hereby but
else part everywhere former don with than those he me forty myself made full twenty these bill using up us
will nevertheless below anywhere nine can theirs toward my something and sometimes whenever sometime then
almost wherever is describe am it doesn an really as itself at have in seem whence ie any if again hasnt
inc un thin no perhaps latter meanwhile when amount same wherein beside how other take which latterly you
fill either nobody unless whereas see though may after upon therefore most hereupon eight amongst never
serious nothing such why a off whereby third i whole noone many well except amoungst yours rather without
so five the first having once
"""


portuguese = """
de a o que e do da em um para é com não uma os no se na por mais as dos como mas foi ao ele das tem à seu
sua ou ser quando muito há nos já está eu também só pelo pela até isso ela entre era depois sem mesmo aos ter
seus quem nas me esse eles estão você tinha foram essa num nem suas meu às minha têm numa pelos elas havia seja
qual será nós tenho lhe deles essas esses pelas este fosse dele tu te vocês vos lhes meus minhas teu tua teus
tuas nosso nossa nossos nossas dela delas esta estes estas aquele aquela aqueles aquelas isto aquilo estou está
estamos estão estive esteve estivemos estiveram estava estávamos estavam estivera estivéramos esteja estejamos
estejam estivesse estivéssemos estivessem estiver estivermos estiverem hei há havemos hão houve houvemos houveram
houvera houvéramos haja hajamos hajam houvesse houvéssemos houvessem houver houvermos houverem houverei houverá
houveremos houverão houveria houveríamos houveriam sou somos são era éramos eram fui foi fomos foram fora fôramos
seja sejamos sejam fosse fôssemos fossem for formos forem serei será seremos serão seria seríamos seriam tenho
tem temos tém tinha tínhamos tinham tive teve tivemos tiveram tivera tivéramos tenha tenhamos tenham tivesse
tivéssemos tivessem tiver tivermos tiverem terei terá teremos terão teria teríamos teriam
"""

LANGUAGES = {"english": english, "portuguese": portuguese}

def get_stopwords_by_language(language):
    if language in LANGUAGES:
        return LANGUAGES[language]
    return LANGUAGES["english"]


