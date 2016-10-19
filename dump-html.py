#!/usr/bin/env python2
# -*- coding: UTF-8 -*-
# File: dump-html.py
# Date: Wed Mar 25 17:44:20 2015 +0800
# Author: Yuxin Wu <ppwwyyxxc@gmail.com>

import sys
import argparse
import os

from common.textutil import ensure_unicode
from wechat.parser import WeChatDBParser
from wechat.res import Resource
from wechat.render import HTMLRender

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('names', metavar='name', nargs='*', help='names of contacts')
    parser.add_argument('--output', help='name or prefix of output html file(s)', default='output.html')
    parser.add_argument('--db', default='decrypted.db', help='path to decrypted database')
    parser.add_argument('--avt', default='avatar.index', help='path to avatar.index file')
    parser.add_argument('--res', default='resource', help='reseource directory')
    parser.add_argument('--all', action='store_true', help='iterate through all contacts')
    args = parser.parse_args()
    return args

if __name__ == '__main__':
    args = get_args()

    parser = WeChatDBParser(args.db)
    res = Resource(parser, args.res, args.avt)

    items = []
    if args.all:
        items += [(k, '%s%s.html' % (args.output, k)) for k in parser.msgs_by_chat.keys() if k]
    else:
        for name in args.names:
            name = ensure_unicode(name)
            if name and name in parser.msgs_by_chat:
                items.append((name, args.output if len(args.names) == 1 else '%s%s.html' % (args.output, name)))
            else:
                sys.stderr.write(u"Valid Contacts: {}\n".format(u'\n'.join(parser.msgs_by_chat.keys())))
                sys.stderr.write(u"Couldn't find that contact {}.".format(name));
    for name, output_file in items:
        msgs = parser.msgs_by_chat[name]
        print 'Writing "%s" chats to "%s"' % (name, output_file)
        print "Number of Messages: ", len(msgs)
        assert len(msgs) > 0

        render = HTMLRender(parser, res)
        htmls = render.render_msgs(msgs)

        #if len(htmls) == 1:
        #    with open(output_file, 'w') as f:
        #        print >> f, htmls[0].encode('utf-8').replace('__footer__', 'No more')
        #else:
        for idx, html in enumerate(htmls):
            with open(output_file + '.{}'.format(idx), 'w') as f:
                if True:  #idx < len(htmls):
                    footer = u'<a href="{output_file}.{next}">More messages</a>'.format(
                        output_file=os.path.basename(output_file), next=idx + 1)
                else:
                    footer = 'No more'
                print >> f, html.replace('__footer__', footer).encode('utf-8')
