# coding=utf-8
from time import sleep
import subprocess
import midi

def say(t):
    #  http://stackoverflow.com/questions/3516007/run-process-and-dont-wait
    subprocess.call(['say', t, '-v', 'Vicki'])

m = midi.read_midifile('./jonathan_coulton-still_alive.mid')
notes = list(i for i in m[1] if isinstance(i, midi.NoteOnEvent))

#m = midi.read_midifile('./mary.mid')
#notes = list(i for i in m[1] if isinstance(i, midi.NoteOnEvent))

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

    
lyrics = "This was a triumph. I'm making a note here: HUGE SUCCESS.  It's hard to overstate my satisfaction.".split()
#lyrics = "Mary had a little lamb, little lamb, little lamb".split()

tosay = ''
for i,j in zip(seq[:len(lyrics)], lyrics):
    #say('[[pbas %s]] test' % i.data[0], r = 1/(0.01 + i.tick * 0.005))
    #say('[[pbas %s]] [[inpt phon]] [[volm %s]] UW' % tuple(i[1]), r=100*(220.0/i[2]))
    speed = 500*(220.0/i[2])
    note = [i[1][0]-12, i[1][1]]
    #tosay +='[[ctxt WORD]] [[pmod 0]] [[pbas %s]] [[volm %s]] [[rate %s]] %s' % tuple(note + [speed,j])
    tosay +='[[inpt PHON]] [[pbas %s]] [[volm %s]] [[rate %s]] %s' % tuple(note + [speed,'UW,'])

say(tosay)

say(' '.join(lyrics))
