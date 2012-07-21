
import hashlib

class news_post(object):
    
    def __init__(self, news_id, title, html_text, filename):
        self.news_id = news_id
        self.title = title
        self.html_text = html_text
        self.filename = filename


class gats_image(object):
    def __init__(self, photo_id, filename):
        self.photo_id = photo_id
        self.filename = filename


class account(object):

    def __init__(self, username, password):
        self.username = username
        self.password = self.encrypt(password)
    

    def encrypt(self, password):
        salt = ""
        for letter in password:
            a = ord(letter)
            b = hex(a)
            salt = salt + b
        
        return hashlib.md5(salt+password).hexdigest()
    

    
