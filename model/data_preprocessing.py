import re
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize


def remove_not_words(content):
    content = re.sub(r'[^\w\s]', '', content)
    content = re.sub(r'\d+', '', content)
    return content


def stem_text(text):
    stemmer = PorterStemmer()
    token_words = word_tokenize(text)
    stemmed_text = []
    for word in token_words:
        stemmed_text.append(stemmer.stem(word))
    return ' '.join(stemmed_text)


def prepare_data(data):
    data['content'] = data['content'].apply(remove_not_words)
    data['content'] = data['content'].apply(stem_text)
    return data



