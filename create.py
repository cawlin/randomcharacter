from flask import Response, request, redirect, render_template, url_for, Flask

import character

# configuration
SECRET_KEY = 'Y\xf6\xf2j\xcf\xc5\xac\xde{\xaf\x1a\xc8\x8dZ0\x9e\x14\xb6\x90\xd7\x02\x03\xf0\x1a'
DEBUG = True

app = Flask(__name__)
app.config.from_object(__name__)

SYSTEMS = {
    'lbb': character.LBBCharacter,
    'greyhawk': character.GreyhawkCharacter,
    'basic': character.BasicCharacter,
}
    
@app.route('/')
def index():
    return redirect('/basic/')    
    
@app.route('/text/')
def index_text():
    return redirect('/basic/text/')    
    
@app.route('/<system>/', defaults={'fmt': "html"})
@app.route('/<system>/<fmt>/')
def generate(system, fmt):
    if fmt == "text":
        template = "plaintext.txt"
        mimetype = "text/plain"
    elif fmt == "html":
        template = "index.html"
        mimetype = "text/html"
    # TODO: As JSON
    # elif fmt == "json":
    #   template = "index.html"
    #   mimetype = "application/json"
    else:
        # default to HTML for unknown display formats
        return redirect(url_for('generate', system=system, fmt="html"))
        
    system = SYSTEMS.get(system, None)     
    if not system:
        # default to basic for unknown systems
        return redirect(url_for('generate', system='basic', fmt=fmt))
            
    content = render_template(template, c=system())
    response = Response(content, status=200, mimetype=mimetype)
    return response 
    
if __name__ == '__main__':
    app.run("0.0.0.0")