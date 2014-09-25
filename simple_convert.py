from bs4 import BeautifulSoup
from bs4 import Doctype

notetaker_file = 'notebook.xml'
evernote_file = 'evernote_ver.enex'

# open and parse original notetaker XML file
with open(notetaker_file, 'r') as notebook:
    content = notebook.read()

soup = BeautifulSoup(content,'xml')
pages = soup.findAll('page')

# start blank evernote XML doc
everdoc = BeautifulSoup('','xml')
