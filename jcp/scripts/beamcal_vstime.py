#! /usr/bin/env python
import aipy as a, pylab as p, numpy as n, sys, optparse

o = optparse.OptionParser()
o.set_usage('beamcal.py [options]')
a.scripting.add_standard_options(o, cal=True, pol=True, cmap=True)
o.add_option('-f', '--freq', dest='freq', type='float', default=.150,
    help='Frequency to plot beam for.  Default .150 GHz')
o.add_option('--nside', dest='nside', type='int', default=32,
    help='NSIDE parameter for HEALPix map of beam.')
             
opts,args = o.parse_args(sys.argv[1:])

cmap = p.get_cmap(opts.cmap)
print 'Plotting beam at %f GHz' % (opts.freq)

afreqs = n.load(args[0])['afreqs']
srclist = [f.split('.')[0] for f in args]

aa = a.cal.get_aa(opts.cal, afreqs)
cat = a.cal.get_catalog(opts.cal,srclist)
cat.compute(aa)

beam = a.map.Map(opts.nside,interp=True)

fluxcal = 'cyg'
srctimes = {}
srcfluxes = {}
srcgains = {}
for src, npz in zip(srclist,args):
    print 'Reading:', npz
    try: f = n.load(npz)
    except:
        print 'Load file failed.'
        continue
    if not srctimes.has_key(src):
        srctimes[src] = f['times']
    if not srcfluxes.has_key(src):
        srcfluxes[src] = f['spec']
        srcfluxes[src] = n.sum(srcfluxes[src].real,axis=1)
        if src == fluxcal:
            srcgains[src] = f['spec']
            #srcgains[src] = f['spec']/n.reshape(cat[src].jys,(1,afreqs.size))
            srcgains[src] = n.sum(srcgains[src].real,axis=1)
            offset = max(srcgains[src])
            #print offset
        else:
            srcgains[src] = f['spec']
            #srcgains[src] = f['spec']/n.reshape(cat[src].jys,(1,afreqs.size))
            srcgains[src] = n.sum(srcgains[src].real,axis=1)

alt,az,lst = {},{},{}
ha = {}
dec = {}
x,y,z = {},{},{}
#if fluxcal in srclist:
#    srclist.remove(fluxcal)
#else:
#    print 'You do not have a flux calibrator!'
#    sys.exit()

#get rich's CST beam file
B = n.loadtxt('/data1/paper/2010_beam/sdipole_05e_eg_ffx_150.txt',skiprows=2)

srclist = [s for s in ['cyg','vir','cas','crab'] if s in srclist]

cnt = 0
for k in srclist:
    fluxes = srcfluxes[k]
    gains = srcgains[k]
    if not alt.has_key(k):
        alt[k], az[k], lst[k] = [],[],[]
        x[k],y[k],z[k] = [],[],[]
    #if not dec.has_key(k): dec[k] = []
    #if not ha.has_key(k): ha[k] = []
    for i,t in enumerate(srctimes[k]):
        aa.set_jultime(t)
        lst[k].append(aa.sidereal_time())
        cat[k].compute(aa)
        #ha[k].append(aa.sidereal_time() - cat[k].ra)
        #dec[k].append(cat[k].dec)
        alt[k].append(cat[k].alt)
        az[k].append(cat[k].az)
    lst[k] = n.array(lst[k])
    alt[k] = n.array(alt[k])
    az[k] = n.array(az[k])
    lst[k] = lst[k] - lst[k][n.where(alt[k]==max(alt[k]))[0]]
    lst[k] = n.where(lst[k] > -n.pi, lst[k], lst[k]+(2*n.pi))
    lst[k] = n.where(lst[k] < n.pi, lst[k], lst[k]-(2*n.pi))
    #ha[k] = n.array(ha[k])
    #dec[k] = n.array(dec[k])
    #x,y,z = a.coord.radec2eq((ha[k],dec[k]))
    x[k],y[k],z[k] = a.coord.azalt2top((az[k], alt[k]))
    #resp = beam.map[x[k],y[k],z[k]]
    #weight = beam.wgt[x[k],y[k],z[k]]
    #crossing = n.where(weight != 0)[0]
    #if n.any(crossing):
    #    print crossing
    #    #print beam.map.px2crd(crossing)
    #    gain = n.average(beam.map.px2crd(crossing))
    #    print k, gain
    #    print n.average(gains[crossing])
    #    gains /= (n.average(gains[crossing])/gain)
    wgts = n.where(fluxes > 1,n.log10(fluxes),0)
    #wgts = n.ones_like(fluxes)
    #fluxes = n.log10(fluxes)
    gains /= n.max(gains)
    beam.add((x[k],y[k],z[k]), wgts, gains)
    #if k == 'cyg': p.plot(resp); p.show()
    if True:
        xx,yy,zz = -x[k],-y[k],z[k]
        beam.add((xx,yy,zz),wgts,gains)
    cnt+=1
    p.subplot(2,2,cnt)
    p.plot(lst[k],gains,label=k) #transit
    p.plot((n.pi/180) * B[:,0], 10**((B[:,2]-n.max(B[:,2]))/10),',',alpha=.5)
    p.legend()

p.show()

#beam.to_fits(opts.outfile, clobber=True)
