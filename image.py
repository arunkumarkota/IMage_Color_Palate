from flask import Flask, render_template, request, redirect
import os
from werkzeug.utils import secure_filename
from matplotlib import image as img
from matplotlib import pyplot as plt
from scipy.cluster.vq import whiten, kmeans
import pandas as pd

app = Flask(__name__)

UPLOAD_FOLDER = "/Users/{your folder path}/{your folder path}/{your folder path}/static"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/uploadDoc", methods=['POST', 'GET'])
def uploadDoc():
    if request.method == "POST":
        file = request.files['file']
        # filename = secure_filename(file.filename)
        filename = secure_filename("image.jpg")
        if file.filename == '':
            return f'<h1>File Save Unsuccessful - Please check !</h1>'
        else:
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            image = img.imread('./static/image.jpg')
            df = pd.DataFrame()
            df['r'] = pd.Series(image[:, :, 0].flatten())
            df['g'] = pd.Series(image[:, :, 1].flatten())
            df['b'] = pd.Series(image[:, :, 2].flatten())
            df['r_whiten'] = whiten(df['r'])
            df['g_whiten'] = whiten(df['g'])
            df['b_whiten'] = whiten(df['b'])
            quantity = int(request.form["quantity"])
            cluster_centers, distortion = kmeans(df[['r_whiten', 'g_whiten', 'b_whiten']], quantity)
            r_std, g_std, b_std = df[['r', 'g', 'b']].std()
            colors = []
            colorshex = []
            for color in cluster_centers:
                sr, sg, sb = color
                colors.append((int(sr * r_std), int(sg * g_std), int(sb * b_std)))
            print(colors)
            for color in colors:
                hexvalue = '#%02x%02x%02x' % color
                colorshex.append(hexvalue)
            return render_template("run.html", imgColors=colorshex, img='./static/image.jpg')


if __name__ == "__main__":
    app.run(debug=True)
