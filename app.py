import requests
from flask import Flask, render_template, request
from similarity import sbert_model, cosine, sentences
import spacy

from spacy import displacy

nlp = spacy.load("en_core_web_sm")

# from spacy_nlp import displacy_service


app = Flask(__name__)


@app.route('/')
def hello_world():
    print('i am dying')
    return render_template("search.html")


@app.route('/search', methods=["GET", "POST"])
def search_request():
    most_sim_list = []

    query = request.form["input"]
    # print(query)
    # print(sbert_model)
    query_vec = sbert_model.encode([query])[0]

    for sent in sentences:
        sim = cosine(query_vec, sbert_model.encode([sent])[0])
        if sim > 0.001:
            most_sim_dict = {}
            most_sim_dict['dist'] = sim.item(),
            most_sim_dict['sent'] = sent
            most_sim_list.append(most_sim_dict)

        # print(type(sim))
        # count.append(sim)
        # print(type(sim.item()))
    # print(query_vec)
    # most_sim_docs = sentence_sim.get_most_similar(query)
    # print(sorted(most_sim_list, key=lambda i: i['dist'], reverse=True))
    # print(most_sim_list)
    most_sim_list_sorted = sorted(most_sim_list, key=lambda i: i['dist'], reverse=True)
    # print(most_sim_list_sorted)
    # hits = [{"body": sent} for sent in (d['sent'] for d in most_sim_list_sorted)]
    hits = [[sent['sent'], sent['dist']] for sent in most_sim_list_sorted]
    # print(hits)
    # hits = [{"body": doc} for doc in most_sim_docs]

    res = {}
    res['total'] = len(most_sim_list_sorted)
    res['hits'] = hits

    # displacy_service(query)
    # response_data = requests.post(url="http://localhost:5000/visualize/" + query)

    # return render_template('results.html', res=res)
    return render_template('results.html', res=res)


@app.route('/visualize/<string:text>', methods=["GET", "POST"])
def displacy_service(text):
    doc = nlp(text)
    return displacy.parse_deps(doc)


if __name__ == '__main__':
    app.run()
