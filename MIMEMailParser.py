#!/usr/bin/env python
#coding=utf8
# author: winnieyang

import sys, os
import email
import email.generator


def DecodeMailArchieves(mail, debug=False):
    fp = open(mail, "rb")
    msg = email.message_from_file(fp)
  # traversaling mime-email for each part
    """
        the walk() method is an all-purpose generator which can be used to iterate
        over all the parts and sub-parts of a message object tree, in DFS order.
    """
    m = ""
    for part in msg.walk():
        if len(part.keys()):
            for key in part.keys():
                if debug:    
                    print key + ": " + part.get(key)
                else:
                    m += key + ": " + part.get(key) + "\n"
            charset = part.get_content_charset()
            #if charset is None:
            #    charset = 'utf-8'
            #print charset
            #continue
            if charset != None and charset != "chinesebig5_charset":
                if debug:
                    print unicode(part.get_payload(decode=True), 
			                      charset, 
					              errors='replace').encode('utf8','replace')
                else:
                    m += unicode(part.get_payload(decode=True),
                                 charset, 
                                 errors='replace').encode('utf8','replace') + "\n"
    return m


if __name__ == "__main__":
   if len(sys.argv) != 3:
       print len(sys.argv)
       print "Usage: python " + sys.argv[0] + " <input_dir> <output_dir>"
       exit(1)
   else:    
       input_dir = sys.argv[1]
       output_dir = os.getcwd() + "/" + sys.argv[2]
       
       if not os.path.exists(output_dir):
           os.mkdir(output_dir)
       for f in os.listdir(input_dir):
           if not os.path.isdir(f):
               mail = input_dir + "/" + f
               m = DecodeMailArchieves(mail, debug=True)
               output_file = f.split(".eml")[0]
               fp = open(output_dir + "/" + output_file, "w")
               fp.write(m)
               fp.close()


