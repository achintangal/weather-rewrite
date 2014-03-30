
"""
This script requests Onionoo for new details documents and caches them.

All the functions here are from Oliver Baumanno's hourly script. The main
code that uses these functions has been moved to a callable function

"""

import requests
import sqlite3
import logging 


## LOGGING ##

LOG_FMT = '%(asctime)s %(message)s'
LOG_LVL = logging.DEBUG
logging.basicConfig(filename="helper.log",format=LOG_FMT)
logger = logging.getLogger(__name__)
logger.setLevel(LOG_LVL)


def fetch_last_modified(cursor):
   
    """
    Fetch the Last-Modified-header from the database
    """

    cursor.execute("SELECT id, lastModified FROM weather ORDER BY id DESC")
    last_modified = cursor.fetchone()

    if last_modified:
        return last_modified[1].encode('utf8')

    return None
    

def cache_documents_and_headers(response, connection):
    
    # obtain the last-modified header
    last_mod = response.headers["last-modified"]
    
    #grab the details document
    
    document = response.content
    
    ## save the documents and headers to the database
    connection.execute("INSERT INTO weather(lastmodified, document) VALUES (?, ?)",
                       (last_mod, document))
    connection.commit()


def setup_database(connection):
    # todo: this should and will be handled via models in Django
    connection.execute("CREATE TABLE IF NOT EXISTS weather ("
                       "id integer PRIMARY KEY AUTOINCREMENT,"
                       "lastModified text, document text"
                       ")")
    connection.commit()


def get_documents():
    
    """
    Checks for new details document from Onionoo and saves it in the database.
    """
    
    ## CONSTANTS ##

    OO_URL = "https://onionoo.torproject.org/details"  # the url we're going to query
    
    OO_PARAMS = {           # relevant parameters:
        'type': 'relay',    # we only want relays...
        'running': 'true',  # ... which are running
        'fields': 'nickname,fingerprint,observed_bandwidth',  # limit the document to these fields
        'limit': '10'       # limits number of routers, for testing.
    }
    
    OO_HEADERS = {}  # any headers we want to send


    conn = sqlite3.connect("helper.db")
    setup_database(conn)
    c = conn.cursor()

    
    # Obtain cached last_modified header, if it exists.

    last_modified_header = fetch_last_modified(c)
    
    if last_modified_header:
        OO_HEADERS['if-modified-since'] = last_modified_header
        
    """
    request the document page. If the document was cached before, "if-modified-since"
    is passed, If a 304 is the response the cached document is used.
    """
    
    # will print headers 

    for k,v in OO_HEADERS.iteritems():
        logger.debug("OO_HEADERS: k=%s , v= %s", k, v)
        
    response = requests.get(OO_URL, params = OO_PARAMS, headers = OO_HEADERS)
    # logger.debug("response status_code %d", response.status_code)
    

    ## need to handle http errors

    if response.status_code == 304:
        logger.debug("got 304, no need to request new document. Cached version will do")
        
    elif response.status_code == 200:
        cache_documents_and_headers(response, conn)
        logger.debug("got 200, caching the new document.")
      
    else:
        logger.debug("error code %d", response.status_code)
        

def main():
    get_documents()


if __name__ == "__main__":
    main()
