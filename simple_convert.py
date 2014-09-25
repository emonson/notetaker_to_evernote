from bs4 import BeautifulSoup
from bs4 import Doctype
from bs4 import CData

from datetime import timedelta
from datetime import datetime

notetaker_file = '/Users/emonson/Dropbox/NoteTaker/ComputerNotesNTMLsingle/notebook.xml'
evernote_file = '/Users/emonson/Dropbox/NoteTaker/ComputerNotesNTMLsingle/evernote_ver.enex'

# open and parse original notetaker XML file
with open(notetaker_file, 'r') as notebook:
    content = notebook.read()

soup = BeautifulSoup(content,'xml')
pages = soup.findAll('page')

# start blank evernote XML doc
everdoc = BeautifulSoup('','xml')
outer_doctype = Doctype('en-export SYSTEM "http://xml.evernote.com/pub/evernote-export3.dtd"')
everdoc.append(outer_doctype)

# add overall header tags
en_export = everdoc.new_tag('en-export')
now = datetime.now()
en_export['export-date'] = now.strftime("%Y%m%dT%H%M%SZ") 
en_export['application'] = "simple_convert" 
en_export['version'] = "2014.09.25"
everdoc.append(en_export)

# Notes

for page in pages:
    # note headers
    note = everdoc.new_tag('note')
    title = everdoc.new_tag('title')
    title.string = page['title']
    note.append(title)
    
    # new page doc
    pagedoc = BeautifulSoup('', 'xml')
    
    # TODO: validate pagedoc
    
    # assemble content as CDATA from pagedoc
    content = everdoc.new_tag('content')
    cdata = CData(repr(pagedoc))
    content.append(cdata)
    note.append(content)
    
    



# TODO: validate everdoc

print(everdoc)
