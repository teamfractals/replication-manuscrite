from flask import Flask, render_template, request, url_for
from extract_boxes import extract_boxes
from extract_roi import extract_roi_for_dir
from layout import generate_layout
from random import randint

app = Flask(__name__)

@app.route("/")
def home():
    return render_template('home.html')

@app.route("/upload")
def upload():
    return render_template('upload.html')

@app.route("/uploaded", methods=['POST'])
def uploaded():
    imagefile = request.files.get('template_input', '')
    imagefile.save('out/filled_template.jpg')
    extract_boxes("out/filled_template.jpg")
    extract_roi_for_dir("out/filled_template")
    return render_template('text_input.html')

@app.route("/generate", methods=['POST'])
def generate():
    text = request.form['text_input']
    npages = generate_layout(text, "out/filled_template", "static/__generated__")
    page_seq = [str(i) + ".png" for i in range(npages)]
    return render_template('output_display.html', page_seq=page_seq, random=randint(0, 100000))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

