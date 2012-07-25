import datetime
import hashlib


class news_post(object):
    
    def __init__(self, news_id, title, html_text, date, author, filename):
        self.news_id = news_id
        self.title = title
        self.html_text = html_text
        self.filename = filename
        self.author = author
        self.date = date
    
    

class gats_image(object):

    def __init__(self, photo_id, filename):
        self.photo_id = photo_id
        self.filename = filename



class gats_show(object):

    def __init__(self, show_date, venue, city_state, extra_info):
        self.show_date = self.make_date(show_date)
        self.venue = venue
        self.city_state = city_state
        self.extra_info = extra_info
        # self.link = link

    def make_date(self, string_date):

        return datetime.datetime.strptime(string_date,"%m/%d/%y")
    

    def verbose_date(self):
        return datetime.datetime.strftime(self.show_date, 
                                          "%B %d, %Y")

    def numerical_date(self):
        return datetime.datetime.strftime(self.show_date,
                                          "%m/%d/%y")


        
class show_list(object):
    
    def __init__(self, show_object_list = []):
        self.show_object_list = show_object_list


    def make_show_list_from_fetchall(self, show_list):
        shows = []
        for show in show_list:
            shows.append(
                gats_show(show[0], show[1], show[2], show[3]))
            
        self.show_object_list = reversed(shows)


    def get_date_sorted_show_list(self):
        return sorted(self.show_object_list,
                      key=lambda show: show.show_date)





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
    

    
