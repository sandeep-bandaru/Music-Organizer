import id3reader
import os
import urllib2
import urllib
import simplejson
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, APIC, error
from bs4 import BeautifulSoup


p="E:\\test"
Mfiles=[]
for (dirname, dirs, files) in os.walk(p):
    for filename in files:
        if filename.endswith('.mp3') :
            Mfiles += [filename]
            #print Mfiles

/
#Updating Album Arts
def update_albumart(name):
    audio = MP3(name+'.mp3', ID3=ID3)

    # add ID3 tag if it doesn't exist
    try:
        audio.add_tags()
    except error:
        pass

    audio.tags.add(
        APIC(
            encoding=3, # 3 is for utf-8
            mime='image/png', # image/jpeg or image/png
            type=3, # 3 is for the cover image
            desc=u'Cover',
            data=open(name+'.png').read()
        )
    )
    audio.save()
    print "Album Art Updated.."
    print "\n\n\n"

#List Music dir
def getTags(path,nam):
    path.split('\\')
    id3r=id3reader.Reader(path)
    artist=str(id3r.getValue('performer'))
    album=str(id3r.getValue('album'))
    track=str(id3r.getValue('title'))
    search_term=artist + " " +nam
    print search_term
    nam=nam.split('.mp3')[0]
    getPic(search_term,nam)
    update_albumart(nam)

#Downloading the appropriate image from google images using ajax
def getPic(search,track):
    search= search.split()
    search='+'.join(search)
    req = urllib2.Request("http://ajax.googleapis.com/ajax/services/search/images?v=1.0&q="+search+"&start=1&imgsz=medium|large&as_filetype=png", None, {'user-agent':'Mozilla'})
    opener = urllib2.build_opener()
    f = opener.open(req)
    a=simplejson.load(f)
    imageurl=a['responseData']['results'][0]['url']
    print track
    print "Image Downloading.."
    urllib.urlretrieve(imageurl,track+".png")
    print "Image Downloaded.."

for nam in Mfiles:
    getTags(p+"\\"+nam,nam)
