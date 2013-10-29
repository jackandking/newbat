# -*- coding: utf-8 -*-
# Author: Yingjie.Liu@thomsonreuters.com
# DateTime: 2013-09-19 08:52:17.272000
# Generator: https://github.com/jackandking/newpy
# Newpy Version: 0.8
# Newpy ID: 127
# Description: I'm a lazy person, so you have to figure out the function of this script by yourself.

__version__='0.1'

'''Contributors:
    Yingjie.Liu@thomsonreuters.com
'''

# Configuration Area Start for users of newbat
_author_ = 'Yingjie.Liu@thomsonreuters.com'
# Configuration Area End

_newbat_server_='newxx.sinaapp.com'
#_newbat_server_='localhost:8080'

from datetime import datetime
from optparse import OptionParser
import sys,os
import socket
socket.setdefaulttimeout(3)

header='''@echo off
REM # Author: %s
REM # DateTime: %s
REM # Generator: https://github.com/jackandking/newbat
REM # Newbat Version: %s
REM # Newbat ID: %s
REM # Description: I'm a lazy person, so you have to figure out the function of this script by yourself.
'''

sample_blocks = dict([

    ('0' , 
['App proxy',
r'''
@python C:\Script\Python\newbat\newbat.py %*
''']),

    ('A' , 
['svnci: echo date time', 'http://newxx.sinaapp.com/newbat/6']),

])

def write_sample_to_file(newbat_id=0,
                         id_list=None,
                         filename=None,
                         comment=None):
    if id_list is None: id_list=sample_blocks.iterkeys()
    if filename is None: file=sys.stdout
    else: file=open(filename,'w')
    print >> file, header%(_author_, datetime.now(), __version__, newbat_id)
    for i in id_list:
        if i not in sample_blocks.iterkeys(): print "invalid sample ID, ignore",i; continue
        print >> file, ""
        if comment: print >> file, "'''"
        print >> file, 'REM',sample_blocks[i][0]
        print >> file, sample_blocks[i][1]
        if comment: print >> file, "'''"
        print >> file, ""
    if file != sys.stdout: file.close()

def list_sample(option, opt_str, value, parser):
    print "Here are the available samples:"
    print "---------------------------------------"
    for i in sorted(sample_blocks.iterkeys()):
        print i,"=>",sample_blocks[i][0]
    print "---------------------------------------"
    sys.exit()

def submit_record(what,verbose):
    import urllib,urllib2
    params = urllib.urlencode({'which': __version__, 'who': _author_, 'what': what})
    if verbose: sys.stdout.write("apply for newbat ID...")
    newbatid=0
    try:
        f = urllib2.urlopen("http://"+_newbat_server_+"/newbat", params)
        newbatid=f.read()
        if verbose: print "ok, got",newbatid
    #except urllib2.HTTPError, e:
        #print e.reason
    except:
        #print "Unexpected error:", sys.exc_info()[0]
        if verbose: print "ko, use 0"

    return newbatid
 
def upload_file(option, opt_str, value, parser):
    import re
    filename=value
    if not os.path.isfile(filename): sys.exit("error: "+filename+" does not exist!")
    file=open(filename,"r")
    line=file.readline()
    newbatid=0
    while line:
        line=file.readline()
        m=re.search('# Newbat ID: (\d+)',line)
        if m: 
            newbatid=int(m.group(1))
            break
    file.close
    if newbatid == 0: sys.exit("error: no valid newbat ID found for "+filename)
    sys.stdout.write("uploading "+filename+"(newbatid="+str(newbatid)+")...")
    import urllib,urllib2
    params = urllib.urlencode({'filename': filename, 'content': open(filename,'rb').read()})
    try:
        f = urllib2.urlopen("http://"+_newbat_server_+"/newbat/upload", params)
        res=f.read()
        print res
        if res[:2]=="ok":
          print "weblink: http://"+_newbat_server_+"/newbat/"+str(newbatid)
    except:
        print "Unexpected error:", sys.exc_info()[0]
    sys.exit()

def main():
    usage = "usage: %prog [options] filename"
    parser = OptionParser(usage)
    parser.add_option("-s", "--samples", type="string", dest="sample_list", metavar="sample-id-list",
                      help='''select samples to include in the new file,
                      e.g. -s 123, check -l for all ids''',default="")
    parser.add_option("-l", "--list", help="list all the available samples.", action="callback", callback=list_sample)
    parser.add_option("-u", "--upload", type="string", dest="filename",
                      help='''upload file to newbat server as sample to others. the file must have a valid newbat ID.''',
                      action="callback", callback=upload_file)
    parser.add_option("-c", "--comment", dest="comment",
                      action="store_true", help="add samples with prefix '#'" )
    parser.add_option("-q", "--quiet", help="run in silent mode",
                      action="store_false", dest="verbose", default=True)
    parser.add_option("-o", "--overwrite", help="overwrite existing file",
                      action="store_true", dest="overwrite")
    parser.add_option("-t", "--test", help="run in test mode, no file generation, only print result to screen.",
                      action="store_true", dest="test")
    parser.add_option("-r", "--record", help="submit record to improve newbat (obsolete, refer to -n)",
                      action="store_true", dest="record")
    parser.add_option("-n", "--norecord", help="don't submit record to improve newbat",
                      action="store_false", dest="record", default=True)
    (options, args) = parser.parse_args()
    verbose=options.verbose
    sample_list=options.sample_list

    if options.test is None:
        if len(args) != 1:
            parser.error("incorrect number of arguments, try -h")

        filename=args[0]+'.bat'
        if options.overwrite is None and os.path.isfile(filename): sys.exit("error: "+filename+" already exist!")

        if options.record: newbat_id=submit_record(sample_list,verbose)
        else: newbat_id=0
    else:
        newbat_id=0
        filename=None

    write_sample_to_file(newbat_id=newbat_id,
                         id_list= sample_list,
                         filename=filename,
                         comment=options.comment)
    if verbose and filename: print "generate",filename,"successfully."

if __name__ == '__main__':
    main()


