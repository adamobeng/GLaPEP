#!/usr/bin/env python
import curses
import time
from util import *
import collections
import sys
import os


if __name__ == '__main__':
    FILE = sys.argv[1] or './wrong.py'

    def main(screen):
        maxx, maxy = screen.getmaxyx() 
        curses.start_color()
        curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLUE)
        curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)

        screen.bkgd(curses.color_pair(1))
        screen.refresh()

        left = curses.newwin(maxx, maxy/2, 0, 0)
        left.bkgd(curses.color_pair(2))
        left.box()
        left.addstr(1, 1, "test")
        left.refresh()

        tright = curses.newwin(maxx/2, maxy/2, 0, maxy/2)
        tright.bkgd(curses.color_pair(2))
        tright.box()
        tright.addstr(1, 1, "test")
        tright.refresh()
        
        bright = curses.newwin(maxx/2, maxy/2, maxx/2, maxy/2)
        bright.bkgd(curses.color_pair(2))

        def set_pic(filename):
            if filename[-3:] == 'jpg':
                p = subprocess.Popen(['jp2a', filename, '--output=-', '--size=' + str(maxy/2) + 'x' + str(maxx/2), '-i'], stdout = subprocess.PIPE)
                # http://stackoverflow.com/a/14693789
                picfile = (re.sub(r'\x1b[^m]*m', '', l) for l in p.communicate()[0].split('\n'))

            elif filename[-3:] == 'ascii':
                picfile = open(filename)

            bright.erase()
            for i, line in enumerate(picfile):
                if i== ((maxx/2) -1): break
                bright.addnstr(i, 0, line, maxy/2)
            bright.refresh()


        
        filelines = open(FILE).read().split('\n')

        report = get_report(FILE)
        rindex = collections.defaultdict(list)
        for r in report:
            if int(r['linen']) in (3,5, 7, 12, 14): # TODO Remove this
                rindex[r['linen']].append(r)

        def sing(message, offset=(0, 0), silent=False):
            for nsentence, sentence in enumerate(message):
                tosay = '[[inpt TUNE]]\n'
                sentence = sentence.split()
                phons = list(getpron(j) for j in sentence)
                phrase = phrases[nsentence +offset[0]][offset[1]:]
                #print len(phrase), len(phons), phrase, sentence, phons
                if sentence!= ['SILENCE',]: 
                    tright.addnstr(2+nsentence, 1, ' '.join(sentence), maxy/2)
                    tright.refresh()
                #if sentence!= ['SILENCE',]: print ' '.join(sentence)
                for i, phon in zip(phrase, phons):
                    if i[0] != 0: 
                        tosay += ',\n%% {D %s}\n' % (float(i[0])/2)
                        continue
                    note = [i[1][0], i[1][1]]
                    dur = min(float(i[2]), 400)
                    tosay += '\n'
                    for p in phon.split():
                        tosay += p  + ' {D %s; P %s:0}\n' % (dur / len(phon.split()), str(round(2 ** ((note[0]-69.0)/12) * 440)))
                    tosay += ','
                if not silent: say(tosay)


        offsets ={'E231':(0,0),
                'E113': (6, 0),
        'E711': (12, 0),
        'E303': (12, 22),
        'F821': (12, 28)}

        pics = list('pics/'+ f for f in os.listdir('pics/'))

        if pics: set_pic(pics[0])

        for i, line in enumerate(filelines):
            if not(i % 3) and pics: set_pic(pics[i % len(pics)])
            if i== (maxx-2): break
            if rindex[str(i+1)]: 
                error = rindex[str(i+1)][0]
                tright.clear()
                tright.box()
                tright.standout()
                tright.addnstr(1, 1, error['errorcode'] + ': ' + error['errormessage'], maxy/2)
                tright.standend()
                tright.refresh()
                left.addnstr(i+1, 1, str(i+1) +': ' +line, maxy/2, curses.color_pair(3))
                left.refresh()

                lyrics = sing(messages[error['errorcode']], offsets[error['errorcode']])
            else:
                left.addnstr(i+1, 1, str(i+1) +': ' +line, maxy/2)
                left.refresh()


            time.sleep(0.5)

        tright.clear()
        tright.box()
        sing(('SILENCE', 'How did you ever even get to Hack N Y',), (12, 34))
        time.sleep(2)
            
        c = screen.getch()

    try:
        curses.wrapper(main)
    except KeyboardInterrupt:
        exit()
