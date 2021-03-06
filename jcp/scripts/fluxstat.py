#! /usr/bin/env python
import numpy as n, pylab as p,optparse, sys

o = optparse.OptionParser()
o.add_option('-d','--diff',dest='diff',type='string',
    help='Difference two files rather than compare to catalog.')
opts,args = o.parse_args(sys.argv[1:])

src_prms = {
    '1:08:54.37_13:19:28.8':{ 'jys': 58.},
    '1:36:19.69_20:58:54.8':{ 'jys': 27.},
    '1:37:22.97_33:09:10.4':{ 'jys': 50.},
    '1:57:25.31_28:53:10.6':{ 'jys': 7.5},
    '3:19:41.25_41:30:38.7':{ 'jys': 50.},
    '4:18:02.81_38:00:58.6':{ 'jys': 60.},
    '4:37:01.87_29:44:30.8':{ 'jys': 204.},
    '5:04:48.28_38:06:39.8':{ 'jys': 85.},
    '5:42:50.23_49:53:49.1':{ 'jys': 63.},
    '8:13:17.32_48:14:20.5':{ 'jys': 66.},
    '9:21:18.65_45:41:07.2':{ 'jys': 42.},
    '10:01:31.41_28:48:04.0':{ 'jys': 30.},
    '11:14:38.91_40:37:12.7':{ 'jys': 21.5},
    '14:11:21.08_52:07:34.8':{ 'jys': 74.},
    '15:04:55.31_26:01:38.9':{ 'jys': 72.},
    '16:28:35.62_39:32:51.3':{ 'jys': 49.},
    '16:51:05.63_5:00:17.4':{ 'jys': 306.55},
    '17:20:37.50_-0:58:11.6':{ 'jys': 180.},
    '18:56:36.10_1:20:34.8':{ 'jys': 200.}, #special: resolved
    '20:19:55.31_29:44:30.8':{ 'jys': 36.},
    '21:55:53.91_37:55:17.9':{ 'jys': 43.},
    '22:45:49.22_39:38:39.8':{ 'jys': 50.},
    'cyg' : { 'jys': 10622.92},
    'cas' : { 'jys': 8914.3854135739166},
    'vir' : { 'jys': 1400.7651852892755},
    'crab' : { 'jys': 1817.0860545717171},
}

fluxes = n.loadtxt(args[0],usecols=[2])
srcnames = n.loadtxt(args[0],usecols=[1],dtype='string')

if opts.diff:
    fluxes2 = n.loadtxt(opts.diff,usecols=[2])
    srcnames2 = n.loadtxt(opts.diff,usecols=[1],dtype='string')

badsrcs = ['1:57:25.31_28:53:10.6']
if opts.diff:
    badsrcs.append('9:21:18.65_45:41:07.2')
    badsrcs.append('1:08:54.37_13:19:28.8')

dict = {}
res = []
for f,k in zip(fluxes,srcnames):
    if k in badsrcs: continue
    dict[k] = f
    if opts.diff:
        diff = float(fluxes2[n.where(srcnames2==k)]) - dict[k]
        print k, float(fluxes2[n.where(srcnames2==k)]), f, diff
        res.append(diff/f)
    else:
        diff = src_prms[k]['jys'] - dict[k]
        print k, src_prms[k]['jys'], f, diff
        res.append(diff/src_prms[k]['jys'])

res = n.array(res)
print n.mean(res), n.std(res), n.mean(n.abs(res))

p.hist(res)
p.show()
