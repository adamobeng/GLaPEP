# coding=utf-8
from time import sleep
import subprocess
import midi

def c(x):
    return '\033[%sm' % x


def b(x):
    return unichr(0x2580 + (x % 20))



def say(t, r=220):
    #  http://stackoverflow.com/questions/3516007/run-process-and-dont-wait
    subprocess.call(['say', t, '-r', str(r)])


if 'i' not in locals():
    i = 0
i = i + 1
w = ['INTERGALACTIC', 'PLANETARY', 'PLANETARY', 'INTERGALACTIC']

#m = midi.read_midifile('./jonathan_coulton-still_alive.mid')
m = midi.read_midifile('./mary.mid')
notes = list(i for i in m[1] if isinstance(i, midi.NoteOnEvent))

seq = []
noteon = None
pos = 0
for n in notes:
    pos = pos + n.tick
    if not noteon and (n.data[1] != 0):
        noteon = n
        noteonpos = pos
    elif noteon and (n.data[0] == noteon.data[0]):
        seq.append((noteon.tick, noteon.data, pos-noteonpos))
        noteon = None

    #if noteon and (on.data[1] != 0) and (on.data[0] != noteon.data[0]): 
        #continue
    #else:
        #noteon = on.data

    #off = list(i for i in notes[ion:] if i.data[0] == n.data[0])
    #if not off: continue
    #off = off[0]
    #nlen = off.tick-on.tick
    #if nlen != 0:
        #print ( on.tick, on.data, nlen)
        #seq.append(( on.tick, on.data, nlen))

seq = [
        (0, [midi.B_4, 100], 200),
        (0, [midi.A_4, 100], 200),
        (0, [midi.G_4, 100], 200),
        (0, [midi.A_4, 100], 200),
        (0, [midi.B_4, 100], 200),
        (0, [midi.B_4, 100], 200),
        (0, [midi.B_4, 100], 200),
        ]

for i in seq:
    print i, '[[pbas %s]] [[inpt phon]] [[volm %s]] uw' % tuple(i[1])
    #say('[[pbas %s]] test' % i.data[0], r = 1/(0.01 + i.tick * 0.005))
    say('[[pbas %s]] [[inpt phon]] [[volm %s]] UW' % tuple(i[1]), r=100*(220.0/i[2]))
