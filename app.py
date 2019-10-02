from flask import Flask, render_template, request, url_for
from extract_boxes import extract_boxes
from extract_roi import extract_roi
from layout import generate_layout
from random import randint

app = Flask(__name__)

@app.route("/")
def home():
    return render_template('home.html')

@app.route("/upload", methods=['POST'])
def upload():
    imagefile = request.files.get('template_input', '')
    imagefile.save('out/filled_template.jpg')
    extract_boxes("out/filled_template.jpg")
    extract_roi("out/filled_template")
    return render_template('text_input.html')

@app.route("/generate_output")
def generate():
    text = request.args.get('text_input')
    generate_layout(text, "out/filled_template", "static/generated.png")
    return render_template('output.html', random=randint(0, 100000))

if __name__ == '__main__':
    app.run(debug=True)
