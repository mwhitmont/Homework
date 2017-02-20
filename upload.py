from flask import Flask, render_template, request
from flask.ext.uploads import UploadSet, configure_uploads, ALL

app = Flask(__name__)

photos = UploadSet('photos', ALL)

app.config['UPLOADED_PHOTOS_DEST'] = 'static/img'
configure_uploads(app, photos)

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST' and 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        return filename
    return render_template('upload2.html')


if __name__ == '__main__':
	app.run(debug=True)