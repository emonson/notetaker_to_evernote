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

# for some reason, NoteTaker developers thought it would be a good idea to
# do timestamps as decimal secons since Jan 1, 2001...
refdate = datetime(2001,01,01)

# Notes

for page in pages:
    # note headers
    note = everdoc.new_tag('note')
    title = everdoc.new_tag('title')
    title.string = page['title']
    note.append(title)
    
    # new page doc
    pagedoc = BeautifulSoup('', 'xml')
    inner_doctype = Doctype('en-note SYSTEM "http://xml.evernote.com/pub/enml2.dtd"')
    pagedoc.append(inner_doctype)

    # add overall header tags
    en_note = pagedoc.new_tag('en-note')
    en_note['style'] = "word-wrap: break-word; -webkit-nbsp-mode: space; -webkit-line-break: after-white-space;"
    pagedoc.append(en_note)
    
    # keep track of creation and mod times to decide on both for whole page
    timestamps = []
    
    # loop through all entries on the page
    for ee, entry in enumerate(page('entry')):
        timestamps.append(int(entry['timestamp']))
        timestamps.append(int(entry['modificationTime']))
        
        # divide entries by horizontal rule on new pages
        if ee != 0:
            hr = pagedoc.new_tag('hr')
            en_note.append(hr)
        
        # for this simple version, just pull out strings from each entry,
        # wrap them in divs and replace all \n with <br/>
        # TODO: this removes <link>s!!
        for entry_string in entry.stripped_strings:
            div = pagedoc.new_tag('div')
            for ii,seg in enumerate(entry_string.split('\n')):
                if ii == 0:
                    div.string = seg
                else:
                    div.append(soup.new_tag('br'))
                    div.append(seg)
            en_note.append(div)
    
    # TODO: validate pagedoc
    
    # assemble content as CDATA from pagedoc
    content = everdoc.new_tag('content')
    cdata = CData(repr(pagedoc))
    content.append(cdata)
    note.append(content)
    
    # append creation time, mod time, and authorship to each note
    # <created>20140917T125116Z</created>
    # <updated>20140917T190630Z</updated>
    # <note-attributes><author>Eric Monson</author><reminder-order>0</reminder-order></note-attributes>
    if len(timestamps) == 0:
        timestamps.append(0)
        
    created_time_dec = min(timestamps)
    created_delta = timedelta(seconds=created_time_dec)
    updated_time_dec = max(timestamps)
    updated_delta = timedelta(seconds=updated_time_dec)
    
    created = pagedoc.new_tag('created')
    created.string = (refdate + created_delta).strftime("%Y%m%dT%H%M%SZ")
    note.append(created)
    updated = pagedoc.new_tag('updated')
    updated.string = (refdate + updated_delta).strftime("%Y%m%dT%H%M%SZ")
    note.append(updated)
    note_attributes = pagedoc.new_tag('note-attributes')
    author = pagedoc.new_tag('author')
    author.string = 'Eric E Monson'
    note_attributes.append(author)
    note.append(note_attributes)
    
    # final append of this note (page) onto pages container
    en_export.append(note)


# TODO: validate everdoc

# Save evernote doc
html = everdoc.prettify("utf-8")
with open(evernote_file, 'w') as outfile:
    outfile.write(html)
