from flask import Flask, redirect, url_for, render_template, flash, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user,\
    current_user
from oauth import OAuthSignIn
from werkzeug import secure_filename
import subprocess
import os
import re

# stuff for uploading
from flask.ext.uploads import UploadSet, configure_uploads, ALL
#end stuff for uploading

app = Flask(__name__)
app.config['SECRET_KEY'] = 'top secret!'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['OAUTH_CREDENTIALS'] = {
    'facebook': {
        'id': '317459725322708',
        'secret': 'bf3d86ffca84ce6aebcc043a027f0779'
    },
    'github': {
        'id': '9aaca0d24c3774c51b9f', 
        'secret': '214d1a2afc0f728ddba2c085f38827754f11922b'  
    }
}

commandbase = 'cf_sol.py'
commandtestfile = 'cf_sol_test.py'
trainingfile = 'tinyTraining.txt'

#stuff for uploading
photos = UploadSet('photos', ALL)
app.config['UPLOADED_PHOTOS_DEST'] = 'newuploads' # in current flow, this shouldn't get used
configure_uploads(app, photos)
#end stuff for uploading

db = SQLAlchemy(app)
lm = LoginManager(app)
lm.login_view = 'index'

myPath = '/Users/morgan/oauth-example/homework/'


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    social_id = db.Column(db.String(64), nullable=False, unique=True)
    nickname = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(64), nullable=True)


@lm.user_loader
def load_user(id):
    return User.query.get(int(id))


@app.route('/')
def index():
    return render_template('index.html', commandbase=commandbase)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/authorize/<provider>')
def oauth_authorize(provider):
    if not current_user.is_anonymous:
        return redirect(url_for('index'))
    oauth = OAuthSignIn.get_provider(provider)
    return oauth.authorize()


@app.route('/callback/<provider>')
def oauth_callback(provider):
    if not current_user.is_anonymous:
        return redirect(url_for('index'))
    oauth = OAuthSignIn.get_provider(provider)

    social_id, username, email = oauth.callback()    
    return email
    if social_id is None:
        flash('Authentication failed.')
        return redirect(url_for('index'))

    user = User.query.filter_by(social_id=social_id).first()
    if not user:
        user = User(social_id=social_id, nickname=username, email=email)
        db.session.add(user)
        db.session.commit()
    login_user(user, True)
    
    temppath = myPath + email
    if not os.path.exists(temppath):
        os.makedirs(temppath)

    return redirect(url_for('index'))


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST' and 'photo' in request.files:
        app.config['UPLOADED_PHOTOS_DEST'] = 'homework' + '/' + current_user.nickname
        configure_uploads(app, photos)
        filename = photos.save(request.files['photo'])
        newfile = request.files['photo'].filename
        return testcommand()
    return render_template('upload2.html')


@app.route('/testcommand')
def testcommand():
    dumpfile = myPath + current_user.nickname + '/' + 'outputfile'
  #  cmd = 'mkdir '+current_user.email
  #  p.subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
  #  output = p.stdout.read() 
    #cmd = 'ls /etc/fstab /etc/non-existent-file'

    # copy tinyTraining.txt to the user's homework directory
    # copy cf_sol_test.py to the user's homework directory
    # run 'python cf_sol_test.py'
    cmd = 'cd '+myPath + current_user.nickname + ' ; cp ../../' + commandtestfile +' . ; cp ../../' + commandtestfile + ' . ; python ' + commandtestfile
    
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    stdout = []
    while True:
        line = p.stdout.readline()
        line =line 
        stdout.append(line)
        print line,
        if line == '' and p.poll() != None:
            break
    std = ''.join(stdout)
    open(dumpfile,"wb").write(std)
    return std    


if __name__ == '__main__':
    db.create_all()
    app.run(host='0.0.0.0')
