from bs4 import BeautifulSoup
import glob
import os
import codecs

data_dir = '/Users/emonson/Dropbox/Sites/X_Archive_vis.duke.edu/vis.duke.edu/FridayForum'
outfile_name = 'ff_archive.tsv'

springs = glob.glob(os.path.join(data_dir,'[0-9][0-9]Spring.html'))
falls = glob.glob(os.path.join(data_dir,'[0-9][0-9]Fall.html'))

html_files = springs + falls

with codecs.open(os.path.join(data_dir, outfile_name), 'w', 'utf-8') as outfile:
    outfile.write('archive_output')
    
for file in html_files:
    
    with codecs.open(file, 'r', 'utf-8') as doc:
        content = doc.read()
        
    soup = BeautifulSoup(content)
    vff = soup.find(text="VISUALIZATION FRIDAY FORUM")
    parent_divs = vff.find_parents('div',class_='content')
    top_parent = parent_divs[-1]
    
    hrs = soup.find_all('hr')
    for hr in hrs:
        tg = soup.new_tag('span')
        tg.string = 'xoxox'
        hr.replace_with(tg)

    src = "\t".join(list(top_parent.stripped_strings))
    entries = src.split('xoxox')
    final = '\n'.join(entries) + '\n'
    print final
    
    with codecs.open(os.path.join(data_dir, outfile_name), 'a', 'utf-8') as outfile:
        outfile.write(final)