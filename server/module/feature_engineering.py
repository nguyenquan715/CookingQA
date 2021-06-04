import numpy as np
from gensim.models import Word2Vec, KeyedVectors
from nltk.tag import pos_tag
from string import punctuation
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag
from nltk.stem.porter import PorterStemmer
from nltk.stem import WordNetLemmatizer

# Clean tokens
lemmatizer = WordNetLemmatizer()
remove_tags = ["UH","SYM",".","TO"]
def clean(text):
    tokens = word_tokenize(text)
    word_tags = pos_tag(tokens)
    return [lemmatizer.lemmatize(word_tag[0].lower()) for word_tag in word_tags if word_tag[1] not in remove_tags]

# Get embedding of sentence
DIMENSION = 300
def embedding_text(w2v_model, tokens):
    embedding = np.zeros(DIMENSION)
    for token in tokens:
        if token in w2v_model:            
            embedding += w2v_model[token]
    embedding = embedding/len(tokens)
    return embedding

# Feature engineering for CRF
def sen2fea(tokens):
    features = []
    tokens_lower = [token.lower() for token in tokens]
    token_tags = pos_tag(tokens_lower)
    for i,word in enumerate(tokens_lower):
        postag = token_tags[i][1]
        feature = {
            "bias": 1.0,
            "word.lower()": word.lower(),
            "word[-3:]": word[-3:],
            "word[-2:]": word[-2:],                        
            "word.isdigit()": word.isdigit(),
            "postag": postag,
            "postag[:2]": postag[:2],
        }
        if i > 0:
            word1 = tokens_lower[i-1]
            postag1 = token_tags[i-1][1]            
            feature.update({
                '-1:word.lower()': word1.lower(),                               
                '-1:word.isdigit()': word1.isdigit(),
                '-1:postag': postag1,
                '-1:postag[:2]': postag1[:2],                
            })
        else:
            feature['BOS'] = True
            
        if i < len(tokens)-1:
            word1 = tokens_lower[i+1]
            postag1 = token_tags[i+1][1]            
            feature.update({
                '+1:word.lower()': word1.lower(),                                
                '+1:word.isdigit()': word1.isdigit(),
                '+1:postag': postag1,
                '+1:postag[:2]': postag1[:2],                
            })
        else:
            feature['EOS'] = True
        features.append(feature)
    return features


