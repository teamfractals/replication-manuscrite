import os

from flask import Flask, render_template, request, url_for
from extract_boxes import extract_boxes
from extract_roi import extract_roi_for_dir
from layout import generate_layout
from random import randint

app = Flask(__name__)

hue_sat = {"red": (None, None),
           "blue": (117, 100),
           "green": (64, 105)}

@app.route("/")
def home():
    return render_template('home.html')

@app.route("/upload")
def upload():
    return render_template('upload.html')

@app.route("/uploaded", methods=['POST'])
def uploaded():
    imagefile = request.files.get('template_input', '')
    os.makedirs('out', exist_ok=True)
    imagefile.save('out/filled_template.jpg')
    extract_boxes("out/filled_template.jpg")
    extract_roi_for_dir("out/filled_template")
    return render_template('text_input.html', input_name="text_input", action='/generate')

@app.route("/generate", methods=['POST'])
def generate():
    text = request.form['text_input']
    pencolor = request.form['pencolor']

    h, s = hue_sat.get(pencolor, (None, None))
    npages = generate_layout(text, "out/filled_template", "static/__generated__", hue=h, sat=s)
    page_seq = [str(i) + ".png" for i in range(npages)]
    return render_template('output_display.html', page_seq=page_seq, random=randint(0, 100000))

@app.route("/demo")
def demo():
    return render_template('text_input.html', input_name="demo_input", action='/demo_output')

@app.route("/demo_output", methods=['POST'])
def demo_output():
    text = request.form['demo_input']
    pencolor = request.form['pencolor']
    if not os.path.exists("out/demo_filled"):
        extract_boxes("static/demo_filled.jpg")
        extract_roi_for_dir("out/demo_filled")

    print('Pencolor received:', pencolor)
    h, s = hue_sat.get(pencolor, (None, None))
    print('Hue:', h, 'Sat:', s)
    npages = generate_layout(text, "out/demo_filled", "static/__generated__", hue=h, sat=s)
    page_seq = [str(i) + ".png" for i in range(npages)]
    return render_template('output_display.html', page_seq=page_seq, random=randint(0, 100000))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

