import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.tokenize import sent_tokenize

texts = pickle.load(open('real_texts.p', 'rb'))
real_texts = []
for text in texts:
    real_texts.append(' '.join(text))

def search_query(query, text, n):
    vectorizer = TfidfVectorizer()
    matrix = vectorizer.fit_transform(text)
    query_vec = vectorizer.transform(query)
    best_sim = 0
    best_idx = 0
    for row in range(matrix.shape[0]):
        sim = float(cosine_similarity(query_vec, matrix.todense()[row]))
        if sim > best_sim:
            best_idx = row
            best_sim = sim
    
    new_vectorizer = TfidfVectorizer()
    sent_texts = sent_tokenize(text[best_idx])
    new_matrix = new_vectorizer.fit_transform(sent_texts)
    new_query = new_vectorizer.transform(query)
    best = []
    for row in range(new_matrix.shape[0]):
        sim = float(cosine_similarity(new_query, new_matrix.todense()[row]))
        best.append((sim, row))
    sorted_best = sorted(best, key=lambda x: x[0], reverse=True)
    sorted_n = sorted_best[:n]
    text = []
    for (_, i) in sorted_n:
        text.append(sent_texts[i])
    return text
