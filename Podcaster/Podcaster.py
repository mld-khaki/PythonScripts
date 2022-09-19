#!/usr/bin/python
import fnmatch, os, sys, urllib.request

from os.path import join, getsize
try: import urllib.request as urllib2

except ImportError:
  import urllib2

from os.path import join, getsize
from datetime import datetime

#if (len(sys.argv) == 1):    print(str(sys.argv[1]))

LocalPath = os.getcwd()
Str1 = 'Public'
Str2 = str(LocalPath)
print(LocalPath)
CurrentPath = str(Str2[Str2.find(Str1)+len(Str1):]);
CurrentPath = CurrentPath.replace('\\', '/')

DROPBOX_ID = '66164008'
FOLDERNAME= 'PodcastFeed'
BASE_URL = 'https://dl.dropbox.com/u/%s%s/' % (DROPBOX_ID, CurrentPath)
PODCAST_TITLE = 'Study Music Selected by Milad'
DESCRIPTION = 'This podcast created in by Milad Khaki'
PERMALINK = "Milad-RVZ-"

feed_template = """<?xml version="1.0" encoding="UTF-8" ?>
<rss version="2.0">
    <channel>
      <description>%s</description>
      <link>%s%s.xml</link>
      <title>%s</title>
      <lastBuildDate>%s</lastBuildDate>
        <!--data-feed -->
    </channel>
  </rss>
  """ % (DESCRIPTION, BASE_URL, FOLDERNAME, PODCAST_TITLE, datetime.now())

def main():

  feed = ''
  for dirname, dirnames, files in os.walk('.'):
    dirname_enc = urllib.parse.quote(dirname[2:].replace(r'\\', r'/'))
    for filename in files:
      if not fnmatch.fnmatch(filename, '*.mp3'):
        continue
      mp3_url = urllib.parse.quote(filename)
      title = filename.replace('&','&amp;')
      size = getsize(join(dirname, filename))

      #link = '%s%s/%s' % (BASE_URL, dirname_enc, mp3_url)
      link = '%s%s' % (BASE_URL, mp3_url)

      feed += """<item>
                  <title>%s</title>
                  <link>%s</link>
                  <enclosure type="audio/mpeg" length="%s" url="%s"/>
                  <guid isPermaLink="false">%s%s</guid>
                  </item>

                  """ % (title, link, size, link,PERMALINK,datetime.now())

  feed_data = feed_template.replace('<!--data-feed -->',feed)
  f = open("%s\%s.xml" % (LocalPath, (FOLDERNAME)),'w', encoding="utf-8")
  f.write(feed_data)
  f.close()

if __name__ == '__main__':
  main()