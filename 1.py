# -*- coding: utf-8 -*-

import nltk
from matplotlib import style
from nltk import pos_tag
from nltk.tokenize import word_tokenize
#from nltk.chunk import conlltags2tree
from nltk.tree import Tree
#pip install langdetect daca nu este instalat modulul
from langdetect import detect
from nltk.corpus import wordnet as wn
from nltk.stem import WordNetLemmatizer
from nltk import sent_tokenize
style.use('fivethirtyeight')


# Process text
def process_text():
    raw_text = open("sample_text.txt").read()
    token_text = word_tokenize(raw_text)
    return token_text

token_text=process_text()
tagged_words = nltk.pos_tag(token_text)

# NER taggers

def nltk_tagger():
    ne_tagged = nltk.ne_chunk(tagged_words)
    return (ne_tagged)




# Parse named entities from tree
def structure_ne(ne_tree):
    ne = []
    for subtree in ne_tree:
        if type(subtree) == Tree:
            ne_label = subtree.label()
            ne_string = " ".join([token for token, pos in subtree.leaves()])
            ne.append((ne_string, ne_label))
    return ne

ne_tagged=structure_ne(nltk_tagger())

#Singura functie necesara pentru detectarea limbii(avand ca intrare un paragraf)
def get_language(paragraph):
    return detect(paragraph)
#Determinarea sinonimelor
def penn_to_wn(tag):
    if tag.startswith('N'):
        return wn.NOUN
    elif tag.startswith('V'):
        return wn.VERB
    return None


def Synonym(sent_tokenize_list):
    # print(sent_tokenize_list)
    g = open('sentences.txt', 'w')
    f = open('synonyms.txt', 'w')
    f.write("{")
    g.write("{")
    for counter, sent in enumerate(sent_tokenize_list):
        tagged = pos_tag(word_tokenize(sent))

        synsets = [set() for _ in range(len(tagged))]
        lemmatzr = WordNetLemmatizer()
        f.write("\"" + sent + "\":")
        if (sent[-1] == "?"):
            g.write("\"" + sent + "\":\"intrebare\"")
            if (counter + 1 != len(sent_tokenize_list)):
                g.write(",\n")
            else:
                g.write("\n")
        else:
            g.write("\"" + sent + "\":\"afirmatie\"")
            if (counter + 1 != len(sent_tokenize_list)):
                g.write(",\n")
            else:
                g.write("\n")
        f.write("{")
        for i, token in enumerate(tagged):
            wn_tag = penn_to_wn(token[1])
            if not wn_tag:
                # f.write("1:"+token[0]+']\n')

                continue
            if (i > 0):
                f.write(",\n")
            f.write("\"" + token[0] + "\":[")
            lemma = lemmatzr.lemmatize(token[0], pos=wn_tag)
            for synonym in wn.synsets(lemma, pos=wn_tag):
                synsets[i].add(str(synonym)[8:-7])
            if (len(synsets[i]) == 0):
                synsets[i].add(lemma)
            for syn_num, synonym in enumerate(synsets[i]):
                if (syn_num > 3 or syn_num + 2 == len(synsets[i]) or len(synsets[i]) == 1):
                    f.write("\"" + str(syn_num + 1) + ":" + str(synonym) + "\"")
                    break

                else:
                    f.write("\"" + str(syn_num + 1) + ":" + str(synonym) + "\", ")

            f.write("]")

        if (counter + 1 != len(sent_tokenize_list)):
            f.write("},\n")
        else:
            f.write("}\n")
    f.write("}")
    g.write("}")


Synonym(sent_tokenize("Cartman is just big boned and he likes chocolate. Remember Nagasaki"))
#nltk_main()
language_output=open("language.txt","w")
language_output.write("{\"language\":"+"\""+get_language(open("sample_text.txt").read())+"\"}")
language_output.close()
postag_output=open("postag.txt","w")
postag_output.write("{")
for i in tagged_words:
    postag_output.write("\""+str(i[0])+"\":\""+str(i[1])+"\",")
postag_output.write("}")
postag_output.close()
namedentities_output=open("namedentities.txt","w")
namedentities_output.write("{")
for i in ne_tagged:
    namedentities_output.write("\""+str(i[0])+"\":\""+str(i[1])+"\",")
namedentities_output.write("}")
namedentities_output.close()
