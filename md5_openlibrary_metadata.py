import os
import hashlib
import requests
from basedata import BaseData
import logging

logging.basicConfig(filename = 'md5_openlibrary_metadata.log', 
                    level = logging.DEBUG, 
                    format ='%(asctime)s: %(filename)s >> %(levelname)s - %(message)s')



basedata = BaseData()

def basedata_md5_request(md5):
    return basedata.get({"md5" : md5})

class Book:
    def __init__(self, filepath = "", openlibrary_id = "OL6609513M"):
        self.filepath = filepath
        self.openlibrary_id = self.set_openlibrary_id(openlibrary_id)
        self.openlibrary_data = {} 
        self.rparams = {"bibkeys" : "OLID:OL8405149M", "format" : "json", "jscmd" : "data"}
        
    def set_openlibrary_id(self, openlibrary_id):
        self.openlibrary_id = "OLID:%s" % openlibrary_id
        return self.openlibrary_id

    def get_openlibrary_data(self):
        self.rparams["bibkeys"] = self.openlibrary_id
        self.openlibrary_data = requests.get("http://openlibrary.org/api/books", params = self.rparams).json()
        return self.openlibrary_data

    def get_md5(self, filepath):
        self.filepath = filepath
        self.filename = os.path.split(filepath)[1]
        self.md5 = hashlib.md5(open(filepath).read()).hexdigest()
        return self.md5

    def get_openlibrary_id_from_md5(self, md5):
        rez = basedata_md5_request(md5)
        logging.info(rez)
        if rez != {} and rez["work"].has_key("openlibrary"):
            self.openlibrary_id = self.set_openlibrary_id(rez["work"]["openlibrary"])
            return self.openlibrary_id
        #elif rez != {} and rez["work"].has_key("libgen"):
        #    self.libgen_id = rez["work"]["libgen"]
        else:
            self.openlibrary_id = self.set_openlibrary_id("OL6609513M")
            return self.openlibrary_id
  

"""
file_list = whatever you want
book_list = []

[book_list.append(Book(file)) for file in file_list]
[book.get_md5(book.filepath) for book in book_list]
[book.get_openlibrary_id_from_md5(book.md5) for book in book_list]
[book.get_openlibrary_data() for book in book_list]
[book.openlibrary_data[book.openlibrary_id]["title"] for book in book_list]
titles = [book.openlibrary_data[book.openlibrary_id]["title"] for book in book_list]

"""
