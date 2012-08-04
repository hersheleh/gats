import datetime
import sqlite3
import os
import PIL
from PIL import Image
from gats_content_objects import *
from config_gats import *
from contextlib import closing
from flask import Flask, jsonify, render_template, request, g , redirect, url_for, session, send_from_directory
from werkzeug import secure_filename



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

            image = Image.open(os.path.join(app.config['UPLOAD_FOLDER'], 
                                            filename))
            image_width = image.size[0]
            
            if image_width > 900:
                resize_image(filename, (900, 900), "")
            
            resize_image(filename, (550, 800) , "resized")
            resize_image(filename, (165, 165) , "thumbnails")
            
    return filename


        
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/uploads_resized/<filename>')
def resized_images(filename):
    directory = os.path.join(app.config['UPLOAD_FOLDER'], "resized")
    return send_from_directory(directory, filename);

@app.route('/image_thumbnails/<filename>')
def thumbnails(filename):
    directory = os.path.join(app.config['UPLOAD_FOLDER'], "thumbnails")
    return send_from_directory(directory, filename)
    

#################################################################

######## JAVASCRIPT FALLBACK ROUTES##############################

@app.route('/')
def index():
    posts = get_news()
    return render_template('gats_news.html', posts=posts)

@app.route('/news')
def gats_news():
    posts = get_news()
    return render_template("gats_news.html",posts=posts)

@app.route('/photos')
def gats_photos():
    photos = get_photos()
    return render_template("gats_photos.html", photos=photos)

@app.route('/videos')
def gats_videos():
    return render_template("gats_videos.html")

@app.route('/the_band')
def gats_band():
    return render_template("gats_band.html")

@app.route('/shows')
def gats_shows():
    shows = get_shows()
    return render_template("gats_shows.html", shows=shows)

@app.route('/contact')
def gats_contact():
    return render_template("gats_contact")
#################################################################



####### CONTENT NAVIGATION WITH AJAX ############################

@app.route('/navigate', methods=['GET','POST'])
def navigate():
    page = request.form["p"]
    if "contact" in page:
        return render_template("gats_contact.html")

    elif "news" in page:
        posts = get_news()
        return render_template("gats_news.html",posts=posts)

    elif "photos" in page:
        photos = get_photos()
        return render_template("gats_photos.html", photos=photos)

    elif "video" in page:
        return render_template("gats_videos.html")

    elif "band" in page:
        return render_template("gats_band.html")

    elif "shows" in page:
        shows = get_shows()
        return render_template("gats_shows.html", shows=shows)

    else:
        return redirect(url_for('index'))

#######################################################################



###### AUTHENTICATION AND LOGIN LOGOUT ################################

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
app.secret_key = 'giraffesandcatsaredabomb'

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

##########################################################################

####### UTILITY FUNCTIONS ################################################

def get_news():
    posts = []
    raw_data = g.db.execute(
        'select id, title, rich_text, post_date, author, filename from news'
        )
    post_list = raw_data.fetchall()
    
    for post in post_list:
        if (post[5] != ""):
            posts.append(news_post(post[0], post[1], post[2], 
                                   post[3], post[4],
                                   url_for('resized_images',
                                           filename=post[5])))
        else:
            posts.append(news_post(post[0], post[1], post[2], post[3], 
                                   post[4], post[5]))
            
    return reversed(posts)


def get_photos():
    photos = []
    raw_data = g.db.execute('select id, filename from photos')
    photo_list = raw_data.fetchall()

    for photo in photo_list:
        photos.append(gats_image(photo[0], photo[1]))

    return reversed(photos)

def get_shows():
    raw_data = g.db.execute(
        'select id, show_date, venue, city_state, extra_info from shows')

    shows = show_list()
    shows.make_show_list_from_fetchall(raw_data.fetchall())
    
    return shows.get_date_sorted_show_list()
    
def delete_from_fs(delete_file_name):

    original_file_path = app.config['UPLOAD_FOLDER']
    thumbnail_file_path = os.path.join(app.config['UPLOAD_FOLDER'],
                                       "thumbnails")
    resized_file_path = os.path.join(app.config['UPLOAD_FOLDER'],
                                     "resized")

    os.remove(os.path.join(original_file_path, delete_file_name))
    os.remove(os.path.join(thumbnail_file_path, delete_file_name))
    os.remove(os.path.join(resized_file_path, delete_file_name))



def resize_image(filename, size, folder):
    
    image_file = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    save_path = os.path.join(app.config['UPLOAD_FOLDER'], folder)
    
    image = Image.open(image_file)
    print image.size
    image.thumbnail(size, Image.ANTIALIAS)
    image.save(os.path.join(save_path, filename), "JPEG")
    
    
#########################################################################


####### ROUTES FOR EDITING THE SITE ###################################
@app.route('/edit')
def edit():
    if 'username' in session:
        return redirect(url_for('edit_news'))

    return redirect(url_for('login'))


@app.route('/edit/news', methods=['GET','POST'])
def edit_news():
    if 'username' in session:
        posts = get_news()
        return render_template("admin_templates/edit_news.html", 
                               posts=posts,name=session['username'])
    return redirect(url_for('login'))

@app.route('/edit/photos')
def edit_photos():
    if 'username' in session:
        photos = get_photos()
        return render_template("admin_templates/edit_photos.html",
                               photos=photos, name=session['username'])
    
    return redirect(url_for('login'))



@app.route('/edit/shows') 
def edit_shows():
    if 'username' in session:
        shows = get_shows()
        return render_template("admin_templates/edit_shows.html",
                               shows=shows, name=session['username'])

    return redirect(url_for('login'))



@app.route('/edit/add_news', methods=['POST'])
def add_news():
    
    now = datetime.datetime.now()
    date = now.strftime("%m/%d/%Y %I:%M %p")
    poster = session['username']
    g.db.execute(
        'insert into news(title, rich_text, filename, post_date, author) values(?,?,?,?,?)', 
        [request.form['post_title'], 
         request.form['news_post'], 
         request.form['filename'],
         date, 
         poster])
    
    g.db.commit()

    return redirect(url_for('edit_news'))

@app.route('/edit/delete_news', methods=['POST'])
def delete_news():
    news_id = request.form['del']
    raw = g.db.execute('select filename from news where id=?',
                       [news_id])
    delete_file = raw.fetchall()
    # delete_from_fs(delete_file[0][0])
    g.db.execute('delete from news where id=?',
                 [request.form['del']])
    g.db.commit()
    return redirect(url_for('edit_news'))


@app.route('/edit/add_photo', methods=['POST'])
def add_photo():
    g.db.execute('insert into photos(filename) values(?)',
                 [request.form['filename']])
    g.db.commit()
    return redirect(url_for('edit_photos'))



@app.route('/edit/delete_photo', methods=['POST'])
def delete_photo():
    photo_id = request.form['photo_id_to_delete']
    raw = g.db.execute('select filename from photos where id=?',
                       [photo_id])
    delete_file = raw.fetchall()
    delete_from_fs(delete_file[0][0])


    g.db.execute('delete from photos where id=?',
                 [photo_id])
    g.db.commit()
    return redirect(url_for('edit_photos'))


@app.route('/edit/add_show', methods=['POST'])
def add_show():
    g.db.execute(
        'insert into shows(show_date, venue, city_state, extra_info) values(?,?,?,?)',
        [request.form['show_date'], 
         request.form['venue'],
         request.form['city'],
         request.form['extra_info']])
    g.db.commit()
    return redirect(url_for('edit_shows'))

@app.route('/edit/delete_show', methods=['POST'])
def delete_show():

    g.db.execute('delete from shows where id=?',
                 [request.form['show_id_to_delete']])
    g.db.commit()
    return redirect(url_for('edit_shows'))

#################################################################
if __name__ == '__main__':
    app.debug = True
    app.run()
