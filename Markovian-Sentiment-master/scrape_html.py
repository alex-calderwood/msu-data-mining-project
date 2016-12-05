from models import Blog, load

from lxml.html import parse
import sys, os, re, argparse, cPickle, string

stripwords_re = re.compile(r'http://[^\s]*|via', flags=re.IGNORECASE)

parser = argparse.ArgumentParser(description='Scrape dumped HTML into structured document features.')
parser.add_argument('blogdir', nargs='+')


def make_dataset(blogdir):
    # Find the largest number here
    blog = Blog()
    entries = [ f for f in os.listdir(blogdir) ]
    entries.sort()
    #print "Blog %s has %d pages"%(blogdir, entries[-1])

    for page in entries:
        doc_dom = os.path.join(blogdir, str(page))
        # posts = extract_posts(doc_dom)
        # print "Page %d/%d had %d posts"%(page, entries[-1], len(posts))
        # for post_dom in posts:
        #     blog.add_doc(text_from_post(post_dom))
        textfile = open(doc_dom, "r")
        blog.add_doc(textfile.read())
    
#    blog.vectorize()
    # Save it
    return blog

