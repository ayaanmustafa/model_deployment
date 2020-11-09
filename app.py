from flask import *  
from keras.preprocessing import image
import tensorflow as tf
app = Flask(__name__)  
import time,os
import numpy as np
from werkzeug.utils import secure_filename

MAIN = "D:/hackathons/model_deployment/"
UPLOAD_FOLDER = 'uploaded/'
EXTENSIONS = ['png','jpg','jpeg']
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')  
def upload():  
    return render_template("upload.html")  
 
@app.route('/success', methods = ['POST'])  
def success():  
    if request.method == 'POST':  
        if 'image' not in request.files:
            flash('No file part')
            return redirect('/')
        
        image1 = request.files['image'] 
        print(image1)
        try:
            from werkzeug.datastructures import FileStorage
            image1= FileStorage(filename=image1.filename)
            x = image1.filename.split('.')[-1]
            print(x)
            if x in EXTENSIONS:
                filename = secure_filename(image1.filename)
                path = os.path.join(MAIN,UPLOAD_FOLDER, filename)
                print(path)
                request.files['image'].save(path)
                model = tf.keras.models.load_model('best_model.h5')
                img = image.load_img(path, target_size=(200, 200))
                x = image.img_to_array(img)
                x = np.expand_dims(x, axis=0)
                img = np.vstack([x])
                classes = model.predict(img)
                for y in classes:
                    lotus = y[0]
                    rose = y[1]
                    sunflower = y[2]
                return render_template("success.html", name = image1.filename,lotus=lotus,rose=rose,sunflower=sunflower,path=path) 
            else:
                print("Error occurred")
                flash("Wrong format or empty file")
                time.sleep(1)
                return redirect('/') 
        except Exception as e:
            print(e)
            return redirect('/')  

@app.route('/return_')
def return_():
    return render_template('upload.html')

 
  
if __name__ == '__main__':  
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.run(debug = True)  
