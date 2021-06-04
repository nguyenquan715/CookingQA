import module.feature_engineering as fe
import module.utility_es as es
from gensim.models import Word2Vec, KeyedVectors
import pickle
from nltk.tokenize import word_tokenize
import pandas as pd
import numpy as np

def get_entities(tokens, tags):     
    entities_dict = {
        "NAME": [],
        "TYPE": [],
        "ING" : [],
        "METHOD": []
    }
    entity = ""    
    for index, tag in enumerate(tags):        
        if tag.startswith('B'):
            if index >= 1 and tags[index-1] != "O":
                entities_dict[tags[index-1][2:]].append(entity)
            entity = tokens[index]
        elif tag.startswith('I'):
            entity += " "+tokens[index]
        elif tag == 'O':
            if index >= 1 and tags[index-1] != "O":
                entities_dict[tags[index-1][2:]].append(entity)
            entity = ""        
    if len(entity) > 0 and tags[-1]!="O":
        entities_dict[tags[-1][2:]].append(entity)
    return entities_dict

def answering_question(w2v_model, question, questions_dict, questions_clf, entities_ext, es_obj):
    for word in ['why','where','how often']:
        if question.lower().find(word) != -1:
            return "No answer for this question!"
    tokens = word_tokenize(question)   
    clean_tokens = fe.clean(question)
    #Feature engineering
    ques_embedding = fe.embedding_text(w2v_model, clean_tokens)
    ques_feature = fe.sen2fea(tokens)
    #Classification and NER
    question_class = questions_clf.predict([ques_embedding])[0]
    tags = entities_ext.predict([ques_feature])[0]
    #Get entities
    entities_dict = get_entities(tokens, tags)
    name_entities, ing_entities, type_entities, method_entities = entities_dict["NAME"], entities_dict["ING"], entities_dict["TYPE"], entities_dict["METHOD"]
    #Get answer
    answer_dict = {
        "class": question_class,
        "tags": tags,
        "name_entities": name_entities,
        "ing_entities": ing_entities,
        "type_entities": type_entities,
        "method_enitities": method_entities
    }
    if len(name_entities)==0:
        answer_dict.update({
            "answer": [es.answer_extraction(es_obj, questions_dict, question_class, "", ing_entities, type_entities, method_entities)]
        })
        return answer_dict
    answer = []
    for name_entity in name_entities:
        answer.append(es.answer_extraction(es_obj, questions_dict, question_class, name_entity, ing_entities, type_entities, method_entities))
    answer_dict.update({
        "answer": answer
    })
    return answer_dict



