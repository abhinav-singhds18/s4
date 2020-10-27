alert("i am dying");

var displacy = new displaCy('http://localhost:5000', {
    container: '#displacy',
})

function parse(text) {
    displacy.parse(text)
}