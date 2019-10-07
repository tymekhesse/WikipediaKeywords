import wikipedia
import spacy
from spacy.matcher import Matcher
import math
import re
from collections import Counter

nlp = spacy.load('en_core_web_sm', disable=['parser', 'ner', 'textcat'])

matched_phrases = []


def collect_sents(matcher, doc, i, matches):
    match_id, start, end = matches[i]
    span = doc[start: end]
    matched_phrases.append(span.lemma_)


patterns = [[{'POS': 'NOUN', 'IS_ALPHA': True, 'IS_STOP': False, 'OP': '+'}]]
matcher = Matcher(nlp.vocab)
for pattern in patterns:
    matcher.add('keyword', collect_sents, pattern)


def extract_keywords_wikipedia(pagename, num_keywords):
    global matched_phrases
    #page = wikipedia.page(pagename)
    #pagenlp = nlp(page.content)
    pagenlp = nlp(pagename)
    matched_phrases = []
    matches = matcher(pagenlp)
    keywords = dict(Counter(matched_phrases).most_common(100))
    keywords_cvalues = {}
    for keyword in sorted(keywords.keys()):
        parent_terms = list(filter(lambda t: t != keyword and re.match('\\b%s\\b' % keyword, t), keywords.keys()))
        keywords_cvalues[keyword] = keywords[keyword]
        for pt in parent_terms:
            keywords_cvalues[keyword] -= float(keywords[pt]) / float(len(parent_terms))
        keywords_cvalues[keyword] *= 1 + math.log(len(keyword.split()), 2)
    best_keywords = []
    for keyword in sorted(keywords_cvalues, key=keywords_cvalues.get, reverse=True)[:num_keywords]:
        best_keywords.append([keyword, keywords_cvalues[keyword]])
    return best_keywords


# print(extract_keywords_wikipedia("New York City", 10))
# print(extract_keywords_wikipedia("Python (programming language)", 10))
# print(extract_keywords_wikipedia("Artificial intelligence", 10))
# print(extract_keywords_wikipedia("Computer science", 10))
str = """As Donald Trump strived to enforce message discipline among Republicans in the face of a building threat that he will be impeached, new forces beyond the US president’s control appeared likely to accelerate the congressional impeachment inquiry further in the coming week.
At least one additional whistleblower has stepped forward to describe an alleged scheme by Trump to extort Ukraine for dirt on Democratic 2020 presidential rival Joe Biden, the individual’s lawyer announced.

Congress is preparing to take testimony on Tuesday from a major figure in the Ukraine scandal, Gordon Sondland, a wealthy hotelier and major Trump donor who was made US ambassador to the European Union.

Similar testimony last week by former US special envoy to Ukraine Kurt Volker led to the disclosure of a damaging series of text messages further implicating Trump in the scandal.


Trump-Ukraine texts: read the revealing diplomatic messages in full
 Read more
And Trump’s would-be defenders in the Republican ranks, with the notable exception of two figures who themselves are deeply implicated in the Ukraine affair – secretary of state Mike Pompeo and Trump lawyer Rudy Giuliani – have fallen mostly silent. No Trump defender from the White House appeared on the US Sunday morning news shows, nor did any members of the congressional Republican political leadership.

Trump’s course of self-defense, meanwhile, appeared to be increasingly erratic. The president told House Republicans that his reportedly outgoing energy secretary, Rick Perry, was the secret Machiavelli behind a phone call Trump held with Ukrainian president Volodymyr Zelenskiy, central to the scandal, Axios reported.

“Not a lot of people know this but, I didn’t even want to make the call,” Trump was quoted as saying. “The only reason I made the call was because Rick asked me to.”"""
print(extract_keywords_wikipedia(str, 5))
