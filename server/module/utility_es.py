from elasticsearch import Elasticsearch
import ast
import json
from nltk.stem import WordNetLemmatizer

# Lemmatizer
lemmatizer = WordNetLemmatizer()

#Connect to ES
def connect_elasticsearch():
    _es = None
    _es = Elasticsearch([{'host':'localhost', 'port':9200}])
    if _es.ping():
        print("Connected!")
    else:
        print("Could not connect!")
    return _es

#Search ES
def search(es_object, index_name, search):
    res = es_object.search(index=index_name, body=search)
    return res

def answer_extraction(es_obj, questions_dict,ques_class, name_entity, ing_entities, type_entities,method_entities):
    if ques_class not in questions_dict.keys():
        return "No answer for this question!"
    source = questions_dict[ques_class]["source"]
    size = questions_dict[ques_class]["size"]        
    must_query = []
    should_query = []    
        
    if name_entity:    
        must_query.append({
            "match": {
               "Title": {
                    "query": name_entity,                    
                    "fuzziness": 3
                }   
            }
        })
    for method_entity in method_entities:
        lemma_entity = lemmatizer.lemmatize(method_entity,'v')
        should_query.append({
            "match": {
                "Title": {
                    "query": lemma_entity,
                    "fuzziness": 2
                }
            }
        })        
    for ing_entity in ing_entities:
        must_query.append({
            "match": {
                "Ingredients": {
                    "query": ing_entity,
                    "fuzziness": 2
                }
            }
        })
    for type_entity in type_entities:
        should_query.append({
            "match": {
                "Category": {
                    "query": type_entity,
                    "fuzziness": 2
                }
            }
        })
    query = {
        "_source": source,
        "size": size,
        "query": {
            "bool": {
                "must": must_query,
                "should": should_query,
                "minimum_should_match": "75%",
                "boost" : 1.0
            }
        }
    }
    return search(es_obj, 'recipes', json.dumps(query))
