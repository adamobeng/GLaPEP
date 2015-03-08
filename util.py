# coding=utf-8
from time import sleep
import subprocess
import re
import midi
import flake8.main
import collections

arpa_to_osx = [
    ('AA','AA'),
    ('AE','AE'),
    ('AH','UX'),
    ('AO','AO'),
    ('AW','AW'),
    ('AY','AY'),
    ('B','b'),
    ('CH','C'),
    ('D','d'),
    ('DH','D'),
    ('EH','EH'),
    ('ER','UX'),
    ('EY','EY'),
    ('F','f'),
    ('G','g'),
    ('HH','h'),
    ('IH','IH'),
    ('IY','IY'),
    ('JH','j'),
    ('K','k'),
    ('L','l'),
    ('M','m'),
    ('N','n'),
    ('NG','N'),
    ('OW','OW'),
    ('OY','OY'),
    ('P','p'),
    ('R','r'),
    ('S','s'),
    ('SH','S'),
    ('T','t'),
    ('TH','T'),
    ('UH','UH'),
    ('UW','UW'),
    ('V','v'),
    ('W','w'),
    ('Y','y'),
    ('Z','z'),
    ('ZH','Z')
]
arpa_to_osx = dict(arpa_to_osx)
enpron = {}
for l in open('/Users/adam/code/hebraize/cmudict-0.7b'):
    if l[:3] != ';;;':
        w, p = l.split(' ', 1)
        pron = p.strip()
        pron = re.sub('[0-9]', '', pron)
        pron = pron.split()
        npron = [arpa_to_osx[p] for p in pron]
        enpron[w] = ' '.join(npron)

def getpron(w):
    w = re.sub('[^A-z]', '', w)
    if w:
        if w.upper() in enpron:
            return enpron[w.upper()]
    return 'UW'

def say(t):
    #  http://stackoverflow.com/questions/3516007/run-process-and-dont-wait
    subprocess.call(['say', t, '-v', 'Vicki'])

def get_report(filename):
    p = subprocess.Popen(['flake8', filename], stdout = subprocess.PIPE)
    report = p.communicate()[0]
    fformat = '(?P<file>.*):(?P<linen>[0-9]+):(?P<charn>[0-9]+): (?P<errorcode>.*?) (?P<errormessage>.*)'
    report=list(re.match(fformat, l).groupdict() for l in report.split('\n') if re.search(fformat, l))
    return report


m = midi.read_midifile('./jonathan_coulton-still_alive.mid')
#m = midi.read_midifile('./mary.mid')
notes = list(i for i in m[1] if isinstance(i, midi.NoteOnEvent))


seq = []
noteon = None
pos = 0
# TODO This monofies the track
for n in notes:
    pos = pos + n.tick
    if not noteon and (n.data[1] != 0):
        noteon = n
        noteonpos = pos
    elif noteon and (n.data[0] == noteon.data[0]):
        seq.append((noteon.tick, noteon.data, pos-noteonpos))
        noteon = None
    

phrases = []
p = []
for n in seq:
    if n[0]!=0:
        phrases.append(p)
        phrases.append([n])
        p = []
    else:
        p.append(n)
phrases = [i for i in phrases if i]


def sing(message, offset=(0, 0), silent=False):
    for nsentence, sentence in enumerate(message):
        tosay = '[[inpt TUNE]]\n'
        sentence = sentence.split()
        phons = list(getpron(j) for j in sentence)
        phrase = phrases[nsentence +offset[0]][offset[1]:]
        #print len(phrase), len(phons), phrase, sentence, phons
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

messages = {
'E231': ('SILENCE', 'Error on line three', 'SILENCE', 'There should be white space here you know', 'SILENCE', 'You just made E two hundred and thirty one happen') ,
'E113': ('SILENCE', 'This is so basic', 'SILENCE', 'Python uses tabs to mark out its blocks', 'SILENCE', 'No use in you trying to fix this indent bug on line five') ,
'E711': ('SILENCE', 'You are so so so dumb at this do you even code\nTo compare to None should not be done with equals') ,
'E303': ('SILENCE', 'And you left three blank lines') ,
'F821': ('SILENCE', 'This name has not been defined') ,
}

#sing(messages['E231'])
#sing(messages['E113'], (6, 0))
#sing(messages['E711'], (12, 0))
#sing(messages['E303'], (12, 22))
#sing(messages['F281'], (12, 28))
#sing(('SILENCE', 'I am so shocked that you could be still alive',), (12, 34))

if __name__ == '__main__':
    FILE='./wrong.py'
    filelines = open(FILE).read().split('\n')

    report = get_report(FILE)
    rindex = collections.defaultdict(list)
    for r in report:
        print r
        rindex[r['linen']].append(r)
    print rindex

