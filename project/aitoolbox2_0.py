from flask import Flask, render_template, request,redirect,url_for
from werkzeug.utils import secure_filename
import os
import numpy as np
import cv2


app = Flask(__name__)

app.config["IMAGE_UPLOAD"] = "./static/uploaded"

@app.route('/render')
def render():
    return render_template('index.html')

@app.route('/upload', methods = ['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
      img = request.files['file']
      filename = secure_filename(img.filename)
      
      basedir = os.path.abspath(os.path.dirname(__file__))
      img.save(os.path.join(basedir,app.config["IMAGE_UPLOAD"],filename))
      
      func = request.form['func']
      if func == "sharpening" :
          return redirect(url_for('sharpy',filename = filename))
      elif func == "blurring" :
          return redirect(url_for('blurry', filename = filename))
      elif func == "colorizer" :
          return redirect(url_for('colorize', filename = filename))
      elif func == "greyscale" :
          return redirect(url_for('grey', filename = filename))
      elif func == "neg" :
          return redirect(url_for('neg', filename = filename))
      return render_template('index.html')
    return render_template('index.html')

@app.route('/sharpy/<filename>')
def sharpy(filename):
    path = './static/sharpened'
    img = cv2.imread(app.config["IMAGE_UPLOAD"]+"/"+filename)
    kernel = np.array([[0, -1, 0],
                       [-1, 5,-1],
                       [0, -1, 0]])
    image_sharp = cv2.filter2D(img , ddepth=-1, kernel=kernel)
    cv2.imwrite(os.path.join(path, filename), image_sharp)
    cv2.waitKey(0)
    functionname = 'sharpened'
    return render_template('output.html',filename = filename , functionname = functionname)

@app.route('/blurry/<filename>')
def blurry(filename):
    path = './static/blurred'
    img = cv2.imread(app.config["IMAGE_UPLOAD"]+"/"+filename)
    img2 = cv2.blur(img,(10,10))
    cv2.imwrite(os.path.join(path, filename), img2 )
    cv2.waitKey(0)
    functionname = 'blurred'
    return render_template('output.html',filename = filename , functionname = functionname)

@app.route('/colorize/<filename>')
def colorize(filename):
    path = "./static/colorized"
    img = cv2.imread(app.config["IMAGE_UPLOAD"]+"/"+filename)
    DIR = "./project"
    PROTOTXT = os.path.join(DIR, "../model/prototxt/name LtoAB.prototxt")
    POINTS = os.path.join(DIR, "../model/points/pts_in_hull.npy")
    MODEL = os.path.join(DIR, "../model/model/colorization_release_v2.caffemodel" )

    net = cv2.dnn.readNetFromCaffe(PROTOTXT,MODEL)   
    pts = np.load(POINTS)

    class8 = net.getLayerId("class8_ab")
    conv8 = net.getLayerId("conv8_313_rh")
    pts = pts.transpose().reshape(2,313,1,1)
    net.getLayer(class8).blobs = [pts.astype("float32")]
    net.getLayer(conv8).blobs = [np.full([1,313], 2.606, dtype = "float32")]


    scaled = img.astype("float32")/255.0
    lab = cv2.cvtColor(scaled,cv2.COLOR_BGR2LAB)

    resized = cv2.resize(lab, (224,224))
    L = cv2.split(resized)[0]
    L -= 50

    net.setInput(cv2.dnn.blobFromImage(L))
    ab = net.forward()[0, :, :, :].transpose((1,2,0))

    ab = cv2.resize(ab, (img.shape[1], img.shape[0]))

    L = cv2.split(lab)[0]
    colorized = np.concatenate((L[:,:,np.newaxis],ab),axis = 2)

    colorized = cv2.cvtColor(colorized, cv2.COLOR_LAB2BGR)
    colorized = np.clip(colorized,0,1)

    colorized = (255 * colorized).astype("uint8")
    
    cv2.imwrite(os.path.join(path, filename),colorized )
    cv2.waitKey(0)
    functionname = 'colorized'
    return render_template('output.html',filename = filename , functionname = functionname)

@app.route('/grey/<filename>')
def grey(filename):
    path = "./static/grayscale"
    img = cv2.imread(app.config["IMAGE_UPLOAD"]+"/"+filename)
    image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    cv2.imwrite(os.path.join(path, filename),image )
    cv2.waitKey(0)
    functionname = 'grayscale'
    return render_template('output.html',filename = filename , functionname = functionname)

@app.route('/neg/<filename>')
def neg(filename):
    path = "./static/negitive-positive"
    img = cv2.imread(app.config["IMAGE_UPLOAD"]+"/"+filename)
    pixel_h, pixel_v = img.shape[0], img.shape[1]
    for i in range(pixel_h):
        for j in range(pixel_v):
            img[i][j] = [255, 255, 255] - img[i][j]
    cv2.imwrite(os.path.join(path, filename),img )
    cv2.waitKey(0)
    functionname = 'negitive-positive'
    return render_template('output.html',filename = filename , functionname = functionname)

@app.route('/display/<functionname>/<filename>')
def display_image(functionname ,filename) :
    return redirect(url_for('static', filename = '/'+ functionname + '/' + filename ))

if __name__ == "__main__" :
    app.run(debug=True)
