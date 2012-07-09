import sqlite3
import os
from stuff import *
from config_gats import *
from contextlib import closing
from flask import Flask, jsonify, render_template, request, g , redirect, url_for, session, send_from_directory
from werkzeug import secure_filename


UPLOAD_FOLDER =  'static/files/images'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

###### DATABASE FUNCTIONS #######################################

def connect_db():
    return sqlite3.connect(DATABASE)

@app.before_request
def before_request():
    g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
    if hasattr(g, 'db'):
        g.db.close()

def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql') as schema:
            db.cursor().executescript(schema.read())
        db.commit()

#################################################################

####### FILE UPLOAD FUNCTIONS ###################################

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == "POST":
        file = request.files['file']
        print "yes"
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            
    return filename


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
    

##############################################################

######## JAVASCRIPT FALLBACK ROUTES##############################

@app.route('/')
def link_root():
    return render_template("gats_home.html")

@app.route('/news')
def gats_news():
    posts = get_news()
    return render_template("gats_news.html",posts=posts)

@app.route('/music')
def gats_music():
    return render_template("gats_music.html")

@app.route('/videos')
def gats_videos():
    return render_template("gats_videos.html")

@app.route('/the_band')
def gats_band():
    return render_template("gats_band.html")

@app.route('/tour')
def gats_shows():
    return render_template("gats_shows.html")
#################################################################



####### CONTENT NAVIGATION WITH AJAX ############################

@app.route('/navigate', methods=['GET','POST'])
def navigate():
    page = request.form["p"]
    print page
    if "home" in page:
        return render_template("gats_home.html")

    elif "news" in page:
        posts = get_news()
        return render_template("gats_news.html",posts=posts)

    elif "music" in page:
        return render_template("gats_music.html")

    elif "video" in page:
        return render_template("gats_videos.html")

    elif "band" in page:
        return render_template("gats_band.html")

    elif "tour" in page:
        return render_template("gats_shows.html")
#####################################################################



####### ROUTES FOR EDITING THE SITE #############################

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        user = request.form['username']
        passwd = request.form['password']
        if authenticate(user,passwd):
            session['username'] = user
            return redirect(url_for('edit'))
        
    return render_template("admin_templates/login.html")


@app.route('/logout', methods=['GET','POST'])
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))


### SECRET KEY ############################
app.secret_key = 'development key'

########################################

def create_account(username, password):
    temp = account(username, password)
    with closing(connect_db()) as db:
        db.execute(
            'insert into accounts(username,password) values(?,?)',
            [temp.username,temp.password])
        db.commit()


def authenticate(username, password):
    authenticate_account = account(username, password)
    accounts = []
    raw = g.db.execute('select * from accounts where username=?',
                       [username])
    users = raw.fetchall()
    for user in users:
        if user[1] == authenticate_account.password:
            print 'true'
            return True
    print 'false'
    return False

def get_news():
    posts = []
    raw_data = g.db.execute('select id, rich_text, filename from news')
    post_list = raw_data.fetchall();
    
    for post in post_list:
        posts.append(news_post(post[0], post[1], 
                               url_for('uploaded_file',filename=post[2])))
        
    return reversed(posts)


@app.route('/edit')
def edit():
    if 'username' in session:
        return render_template("admin_templates/edit_layout.html",
                               name=session['username'])
    return redirect(url_for('login'))


@app.route('/edit/news', methods=['GET','POST'])
def edit_news():
    if 'username' in session:
        posts = get_news()
        return render_template("admin_templates/edit_news.html", 
                               posts=posts,name=session['username'])
    return redirect(url_for('login'))


@app.route('/edit/videos')
def edit_videos():
    return render_template("admin_templates/edit_videos.html")

@app.route('/edit/tour') 
def edit_tour():
    return render_template("admin_templates/edit_tour.html")

@app.route('/edit/add_news', methods=['POST'])
def add_news():

    print request.form['filename']
    g.db.execute('insert into news(rich_text, filename) values(?,?)', 
                 [request.form['news_post'], request.form['filename']])
    g.db.commit()
    print 'wassup'
    return redirect(url_for('edit_news'))

@app.route('/edit/delete_news', methods=['POST'])
def delete_news():
    g.db.execute('delete from news where id=?',
                 [request.form['del']])
    g.db.commit()
    return redirect(url_for('edit_news'))


#################################################################
if __name__ == '__main__':
    app.debug = True
    app.run()
