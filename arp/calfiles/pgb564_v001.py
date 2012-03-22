'''This is a calibration file for data collected at PAPER in Green Bank
on JD 2454564.'''

import aipy as a, numpy as n

class XTalkAntennaArray(a.fit.AntennaArray):
    '''Add xtalk fitting capability to AntennaArray.'''
    def __init__(self, *args, **kwargs):
        a.fit.AntennaArray.__init__(self, *args, **kwargs)
        self.xtalk = {}
        for bl in self.bl_order:
            i,j = a.miriad.bl2ij(bl)
            if i == j: continue
            self.xtalk['xr_%d' % bl] = [0]
            self.xtalk['xi_%d' % bl] = [0]
    def get_params(self, ant_prms={'*':'*','aa':'*'}):
        prms = a.fit.AntennaArray.get_params(self, ant_prms=ant_prms)
        if not ant_prms.has_key('aa'): return prms
        for p in ant_prms['aa']:
            if p.startswith('*'): prms.update(self.xtalk)
            else:
                try: 
                    if len(self.xtalk[p]) > 0: prms[p] = self.xtalk[p]
                except(KeyError): pass
        return prms
    def set_params(self, prms):
        a.fit.AntennaArray.set_params(self, prms)
        for key in self.xtalk:
            try: self.xtalk[key] = prms[key]
            except(KeyError): pass
    def sim_cache(self, *args, **kwargs):
        a.fit.AntennaArray.sim_cache(self, *args, **kwargs)
        afreqs = self.ants[0].beam.afreqs
        for bl in self.bl_order:
            i,j = a.miriad.bl2ij(bl)
            if i == j: continue
            rpoly = self.xtalk['xr_%d' % bl]
            ipoly = self.xtalk['xi_%d' % bl]
            try: len(rpoly)
            except(TypeError): rpoly = [rpoly]
            try: len(ipoly)
            except(TypeError): ipoly = [ipoly]
            x = n.polyval(rpoly, afreqs) + 1j * n.polyval(ipoly, afreqs)
            self._cache['x_%d' % bl] = x
    def sim(self, i, j, pol='xx'):
        Vij_f = a.fit.AntennaArray.sim(self, i, j, pol=pol)
        bl = 'x_%d' % a.miriad.ij2bl(i,j)
        return Vij_f + self._cache[bl] 

prms = {
    'aa': {},
    #'aa': {
    #    'xi_258':  [ 0.02298], 'xr_258':  [-0.01414],   # 0-1 
    #    'xi_259':  [-0.00290], 'xr_259':  [ 0.00614],   # 0-2
    #    'xi_515':  [ 0.00160], 'xr_515':  [ 0.00818],   # 1-2
    #    'xi_260':  [ 0.00502], 'xr_260':  [-0.00288],   # 0-3
    #    'xi_516':  [ 0.00208], 'xr_516':  [ 0.00446],   # 1-3
    #    'xi_772':  [ 0.03483], 'xr_772':  [-0.03566],   # 2-3
    #    'xi_261':  [ 0.00414], 'xr_261':  [ 0.00031],   # 0-4
    #    'xi_517':  [ 0.00150], 'xr_517':  [ 0.00692],   # 1-4
    #    'xi_773':  [-0.00308], 'xr_773':  [ 0.00162],   # 2-4
    #    'xi_1029': [-0.00725], 'xr_1029': [ 0.00581],   # 3-4
    #    'xi_262':  [-0.00606], 'xr_262':  [ 0.00252],   # 0-5
    #    'xi_518':  [ 0.00002], 'xr_518':  [-0.00218],   # 1-5
    #    'xi_774':  [-0.00367], 'xr_774':  [ 0.00274],   # 2-5
    #    'xi_1030': [-0.00106], 'xr_1030': [-0.00158],   # 3-5
    #    'xi_1286': [ 0.02663], 'xr_1286': [-0.04670],   # 4-5
    #    'xi_263':  [-0.00731], 'xr_263':  [ 0.02906],   # 0-6
    #    'xi_519':  [-0.02789], 'xr_519':  [-0.01304],   # 1-6
    #    'xi_775':  [ 0.05303], 'xr_775':  [-0.00905],   # 2-6
    #    'xi_1031': [-0.05614], 'xr_1031': [-0.00026],   # 3-6
    #    'xi_1287': [-0.10662], 'xr_1287': [-0.18912],   # 4-6
    #    'xi_1543': [-0.06061], 'xr_1543': [ 0.06819],   # 5-6
    #    'xi_264':  [ 0.00305], 'xr_264':  [-0.00332],   # 0-7
    #    'xi_520':  [-0.00648], 'xr_520':  [-0.00398],   # 1-7
    #    'xi_776':  [ 0.00676], 'xr_776':  [-0.00260],   # 2-7
    #    'xi_1032': [-0.00597], 'xr_1032': [ 0.00100],   # 3-7
    #    'xi_1288': [-0.00844], 'xr_1288': [ 0.01210],   # 4-7
    #    'xi_1544': [-0.00153], 'xr_1544': [ 0.00724],   # 5-7
    #    'xi_1800': [-0.16381], 'xr_1800': [-0.37440],   # 6-7
    #},
    'loc': ('38:25:59.24',  '-79:51:02.1'), # Green Bank, WV
    'antpos':
        [[   0.07,    0.06,    0.03],
         [ 213.87, -136.12, -261.90],
         [ 196.56, -809.80, -253.10],
         [-254.90, -673.84,  307.94],
         [-285.21, -462.72,  349.48],
         [-277.56, -361.59,  342.70],
         [-174.97, -102.46,  217.75],
         [ -74.85,  -20.89,   97.60]],
    'delays': [2.53, -7.17, 7.78, 8.90, 7.70, 4.12, 4.97, 2.47],
    'offsets': [ 0., .473, .475, .475, .476, .975, .434, .354],
    'amps': [ .00201, .00217, .00217, .00267, .00246, .00196, .00219, .00183],
    'bp_r': n.array([
        #[128.12906345033159, -44.61404765263751, 4.8261550152959227],
        [114.8586309611448, -45.537561849271214, 5.0631498434141058],
        [126.34981219596385, -43.441052034381578, 4.6810033789987706],
        [125.52273633514608, -43.409671546391294, 4.7359882308265],
        #[120.35668358378256, -44.212401433687589, 4.916082041935292],
        [114.8586309611448, -45.537561849271214, 5.0631498434141058],
        [124.41422355131323, -43.494320910355597, 4.7545280205220459],
        [126.75027185409526, -44.289681609995966, 4.8196973390160807],
        [144.39417973046017, -48.689673335340132, 5.0248048566175587],
        [308.50928403235281, -101.05303653693821, 9.1860402431803632],
    ]),
    'bp_i': n.array([
        [0.000],
        [0.000],
        [0.000],
        [0.000],
        [0.000],
        [0.000],
        [0.000],
        [0.000],
    ]),
    'beam': a.fit.BeamAlm,
    'bm_prms': {
        'alm7': n.array(
            [4612071155.2894506, 0.0, 2660797673.6772165, 0.0, 1161721.1344027107, 2354045.8749443963, -12784425479.442125, 0.0, 3700175.3171041263, -44051668.726448923, 13123626556.234783, 386108.57603105111, -2382174694.3013382, 0.0, -1081503.172449097, -29373692.554453604, 14777964715.783834, -1683427.9239359437, 813110.46435451764, -3812691.91110727, 3466997281.5646472, 0.0, -2563551.5188832283, -23139273.10660582, 25388148.416929513, -1965486.4608830863, 3513120.0804395834, -11570200.153496237, 2161072058.4462113, -439577.96917891677, -4951901214.9342003, 0.0, -1032441.7298190107, 3328836.4205635795, 8081589030.4136114, -1652719.4749472591, -1865400.9673852893, 9460416.1435883362, -9003756747.1014824, -440678.5565718984, 5995646.7677083118, -2758821.6293319426, -2242247365.2360134, 0.0, 35802.852213499253, -3834162.2811773354, -4154424145.467073, -405335.4046451351, -3127070.9733344573, 23566305.63948356, -3040200826.2414427, 1867334.2545262163, 8301019.5258571869, 6375051.8484759713, 22538291486.80566, 1727875.6836446917, -9332856169.9584389, 0.0, 4515524.3357601939, -15330649.30626248, 697565905.02544594, 759427.63141970627, -1597887.5944947028, 6695420.8635642696, 7530074244.6463604, -1695298.8674410046, 6876737.5551369777, -30016586.734049782, 10838917326.930387, -1368748.1588819041, -2211483.5054679615, 16363916.894629348, 2254051536.2288723, 0.0, -844123.59855173004, -6318563.7460689889, -4775777502.1429157, 2105882.6053301627, 1048794.493872385, 392223.35177980154, -840084031.8077637, 315219.00145331019, 3070221.2410643268, 2977937.2160425321, 6091180054.3179331, -4849442.5528052635, -2260931.9766342323, 2056775.0411615514, 6261252526.3521967, 1524900.4638124937]
        ),
        'alm6': n.array(
            [-4660525762.0618916, 0.0, -2524890129.3105264, 0.0, -1288053.6696820909, -5083570.7894053329, 13074127578.215466, 0.0, -3843734.1072726971, 41838529.835572749, -13287605038.327871, -374878.19136397942, 1779561136.6909738, 0.0, 1232730.5681239129, 27721991.548800118, -14769756696.219017, 1709288.4541402, -829764.90898081381, 3883655.4642970669, -3934899187.7849774, 0.0, 2666091.1772242272, 22388798.962203968, -383323894.30470109, 2041848.6854621968, -3614947.6423701607, 11906257.638707671, -1895975502.3235941, 414285.79176819004, 4805541904.9948368, 0.0, 1115323.5394004742, -4098873.8598298375, -8454905331.8552265, 1682103.789805315, 1903373.3122605609, -9210170.5329762902, 9429554125.4597111, 371514.44134703698, -6171819.346218694, 2554621.7245216309, 2222458777.2463121, 0.0, -28033.601801204029, 3357793.6252534725, 4182208787.4988604, 426943.56427818362, 3051507.7973345676, -23576677.580001909, 3029877709.9712315, -1930295.2471745659, -8409437.4182829298, -6380262.4946679408, -23024520653.360035, -1740336.0798304661, 9509010460.2392845, 0.0, -4589020.7641511755, 15093129.517367754, -809447861.33019698, -765879.60283120919, 1610424.0836333304, -6578108.3622543653, -7591692639.7837982, 1641113.9951021133, -6962778.9110845523, 29804047.403391641, -10923026279.730234, 1380523.1820658837, 2200336.6016231636, -16880038.399566274, -2331205930.7162404, 0.0, 901143.80021250108, 6271599.2307371255, 4870523153.9875412, -2169318.1456044139, -1112708.2030017427, -273455.84895363171, 889505752.29839969, -360665.75765656878, -3110103.8200725177, -2888273.855283292, -6225414116.1088743, 4998123.2448276188, 2238430.041231615, -1514003.0940831164, -6450153883.6085825, -1544226.9758838417]
        ),
        'alm5': n.array(
            [2000613027.8279903, 0.0, 1018238622.3845403, 0.0, 605935.20965658664, 3319275.9010224836, -5693672854.4147568, 0.0, 1701794.0416455823, -16921029.556687884, 5738154203.1173496, 154700.77681752911, -484557481.05352682, 0.0, -592983.57791285939, -11140137.843231769, 6290808342.7556877, -740224.91826591489, 360429.10347643693, -1686731.2683651219, 1888262503.120419, 0.0, -1180765.1456131535, -9245594.9995583985, 325359268.5831455, -904835.49789935781, 1585383.3530467458, -5224178.1971860183, 691187090.57217813, -165574.90811751323, -1980870659.7346985, 0.0, -511292.24821972975, 2069297.6473076863, 3770799876.7677817, -729880.586746766, -828501.58549510827, 3827045.9518685001, -4207353993.0697498, -127668.90409938717, 2709282.266121435, -1009566.6715455201, -937424590.67227674, 0.0, 9127.6477640160301, -1233373.4490243541, -1793968083.0962284, -191930.35810445016, -1267545.9513495872, 10061002.628571579, -1284509223.1069193, 850745.15071548033, 3633329.0002213414, 2721452.5361638726, 10028796428.584394, 747575.73615000909, -4132309688.249692, 0.0, 1989333.6220171619, -6340050.2086616829, 394964876.90217537, 329517.87814981828, -693090.71307415573, 2759406.39940143, 3263312432.7659307, -675516.39964893158, 3007132.7711852584, -12623201.13027487, 4692501802.8551073, -593536.96315676381, -932786.60316191812, 7415028.54342381, 1027514882.5806189, 0.0, -409763.13897304144, -2656027.4656846928, -2118600434.7125831, 953555.55430847895, 503026.57549084548, 63835.388396419701, -399845809.01566052, 173455.97994096085, 1343514.3672959872, 1190868.208055431, 2714203949.626617, -2197624.5087932283, -944919.09882599779, 417603.72559638921, 2833731137.0090189, 667018.35889184312]
        ),
        'alm4': n.array(
            [-472705153.79630864, 0.0, -226277548.11326784, 0.0, -156823.91044780484, -1050739.4209504947, 1368474472.2610881, 0.0, -416207.71791725501, 3777542.8447143021, -1369962980.7335038, -35161.504738610325, 45526710.849112004, 0.0, 156291.2564905773, 2470944.4711584421, -1480108647.6585567, 177221.05033756132, -86387.950357281472, 404909.18026773882, -497115305.1430434, 0.0, 288648.01062011754, 2112664.1498833774, -116966053.45113739, 221682.87934853596, -384115.86811409809, 1266887.0414421808, -134320556.82436466, 36355.257062945027, 449384307.25573397, 0.0, 128975.58914248558, -561873.70069813484, -929179155.09209764, 175007.84034247737, 199385.29442266418, -879950.47750782571, 1036617620.2335608, 22563.775062596655, -657367.16300686472, 220793.44978668334, 218023005.07133546, 0.0, -1625.5042730743153, 245173.36125491245, 425021396.80396283, 47721.307257849519, 290513.2401987614, -2374059.9077714798, 300231538.23629451, -207198.16821463103, -867774.17264364555, -641474.80744476465, -2414101358.0045009, -177528.12780855937, 992770686.84910822, 0.0, -476832.57711953099, 1473097.8249593058, -105301292.45336658, -78400.401722838345, 165124.59988932207, -640797.35531368863, -775218396.77591097, 153231.76605332966, -718068.34280003724, 2956370.3209095616, -1113894237.0074077, 140997.04091913308, 218398.69117413339, -1798138.4844994908, -250221101.12979904, 0.0, 102849.13157476055, 622172.62511981395, 509486380.23911119, -231813.31826591649, -125587.74181196494, -2154.4401809618575, 98913838.009322032, -45564.507600808327, -320811.72915885417, -270523.78091801633, -654314439.19440067, 534285.97290599276, 220467.74064416732, -45675.61805208688, -688130487.99420595, -159291.89814790915]
        ),
        'alm3': n.array(
            [66366493.898537025, 0.0, 29937865.819118127, 0.0, 24122.455498186038, 185182.71248470346, -196015062.39642286, 0.0, 60718.08323431859, -502723.46659269946, 195279169.51576266, 4752.112130425965, 3808786.4096666439, 0.0, -24404.274172146594, -326703.2309572387, 207751786.43281889, -25332.132014480532, 12339.527121688569, -58022.784168315433, 77598001.606791347, 0.0, -42062.337719492731, -288535.22046921117, 22406589.290301725, -32423.152548474849, 55524.833964190468, -183372.53729020539, 14753457.149977723, -4733.2458229009353, -60570074.11441537, 0.0, -19341.356870199255, 89264.230286899648, 136603715.39673379, -25041.453636301732, -28645.28702756175, 120925.8218766167, -152295519.64386839, -2079.5279989323394, 95202.355571582229, -28867.721968531561, -30184700.609124184, 0.0, 176.97553659225832, -28279.736336152768, -60060784.402532235, -7085.5095039474745, -39676.495285058205, 334563.30071202444, -41777026.670031279, 30112.210501623093, 123726.0427246332, 90261.751677776381, 346814462.22416574, 25170.101611859583, -142394654.07177839, 0.0, 68250.699136349023, -204477.04956758025, 16594755.396964403, 11139.801675523471, -23519.407301991407, 88987.022303578997, 109907247.4540256, -20683.381406560042, 102381.08971738617, -413503.93257166049, 157784680.50699273, -19986.487880128851, -30500.577819558694, 259988.21910233772, 36361287.479784779, 0.0, -15385.688563566848, -87068.954080335752, -73150497.949354276, 33655.420331296998, 18698.123880794952, -1567.8485690510279, -14543700.967304347, 7073.0374506777689, 45729.791790457661, 36560.126345148543, 94185460.579878584, -77558.787692904269, -30706.490498933286, -837.20012620565649, 99741150.306491256, 22712.92590832412]
        ),
        'alm2': n.array(
            [-5534111.4406580171, 0.0, -2359636.1676500821, 0.0, -2205.7532308254113, -18656.825145785682, 16729455.700741626, 0.0, -5283.037277813065, 39880.219358676637, -16618431.14913078, -381.77565851865779, -1221820.577647465, 0.0, 2259.3729339124225, 25747.593075833771, -17396333.468695574, 2161.8098173159697, -1050.4932926707702, 4963.2148214670669, -7186068.2667962899, 0.0, 3653.6669748337004, 23555.477089647931, -2403388.5139174573, 2830.4892770032311, -4788.4706552851712, 15841.428898720276, -881807.27640277834, 365.1271934083901, 4848253.8002490085, 0.0, 1724.8504468895921, -8336.7339560523724, -11980221.377087209, 2138.1302794781814, 2456.3168652460922, -9932.9393869552441, 13340357.082732324, 79.988608852904818, -8228.6769098103996, 2256.9207377050971, 2486821.3162235492, 0.0, -12.521346661551206, 1870.028063196404, 5062138.4044400519, 628.04295022695169, 3228.9811117118429, -28159.229713785768, 3460423.1254681228, -2611.0343718841214, -10530.304623255284, -7583.4875562734514, -29733488.250478297, -2130.6383139040718, 12192790.241233261, 0.0, -5833.3391904591153, 16957.195652148399, -1547776.9064277983, -945.22570504292571, 2002.679544346116, -7391.1010185732775, -9299133.8997094799, 1661.0702594128015, -8715.5345291432131, 34541.922814900048, -13336987.773623958, 1690.5314088890661, 2540.7361739040512, -22415.051215727792, -3153211.1757115237, 0.0, 1371.5210750303586, 7279.7372453637417, 6270076.525104085, -2917.6070505291104, -1659.8664424815909, 293.09469448682512, 1271082.7062015571, -649.69521835990781, -3891.0739049324056, -2938.9748313023729, -8094621.3204188142, 6721.5110798619789, 2553.1326670059821, 665.72408560589531, -8628199.770040581, -1933.524695248718]
        ),
        'alm1': n.array(
            [253666.65870267522, 0.0, 102667.59255725727, 0.0, 111.04271628746029, 1008.7805290970934, -787649.84956658015, 0.0, 253.83840057537637, -1745.9556951362183, 781746.0653777126, 16.876643805653767, 100503.43409879797, 0.0, -114.90236550686564, -1119.8280275751331, 804671.10387874639, -101.98121012355863, 49.357599860962651, -234.64779389669314, 365742.25307159655, 0.0, -175.16562087753948, -1064.4698256625886, 136675.25395339276, -136.53821075280479, 228.11986405942812, -756.29550119181033, 23987.525660317689, -15.438289732774839, -213292.16960161735, 0.0, -84.723639282943367, 425.19723436283982, 580278.78372075933, -100.86609612067454, -116.38274511947233, 451.57619781284757, -645059.92840529734, 0.78787014908808395, 393.0042709993935, -97.720907234361221, -112854.16535221542, 0.0, 0.56916702076267356, -64.175545652252666, -235615.91719765219, -30.761942741106324, -144.99359668095195, 1310.7297429341727, -157967.85788584157, 125.06219018166389, 495.34176832403085, 352.31709055270369, 1408511.1001707762, 99.707562053208605, -577082.51217922091, 0.0, 275.64980314853614, -777.9580456040884, 79183.098578497738, 44.345787692248841, -94.384798959565245, 340.02120213761771, 434747.33111214248, -73.48025434000192, 410.15732849245057, -1595.7024397592129, 622874.14447282674, -79.00536096770864, -116.89526854313844, 1067.0875405506767, 151095.91826963722, 0.0, -67.44916492686086, -336.7198008659513, -297062.31121488288, 139.81775884815883, 81.336870857668345, -21.274593279197973, -61147.728146458918, 32.732898829132004, 182.9875701747136, 130.09807346974486, 384561.63606517582, -321.96077516780645, -117.35028382435407, -57.816636322176429, 412425.22472223977, 90.986630287862383]
        ),
        'alm0': n.array(
            [-4925.7958935346087, 0.0, -1902.2417934735508, 0.0, -2.3746250425828008, -22.767942724423307, 15781.071565182221, 0.0, -5.1954274520833366, 32.539100190901614, -15680.520647333175, -0.31660178378223819, -2890.1980999116831, 0.0, 2.477332106857677, 20.732129540566579, -15861.544546163326, 2.0515160152607725, -0.98744354945725255, 4.7297721147513023, -7895.5944619915845, 0.0, 3.5756460914529065, 20.542928269017423, -3217.3065987898608, 2.8071371186707292, -4.6311343221211514, 15.393113018470766, -133.6443830757068, 0.27563786120492173, 3976.57141733445, 0.0, 1.7686869248809574, -9.1575181405420079, -11974.102178101124, 2.028097742517442, 2.3502165200822667, -8.7656775026319131, 13281.815604591029, -0.10646873520390937, -8.0006067729399621, 1.8082384204282533, 2175.5546070714668, 0.0, -0.012975773576513361, 0.83870278766705642, 4671.9803950615105, 0.64212146386115254, 2.7713846306570877, -26.029570388946681, 3065.6559089452094, -2.5525352452759584, -9.9343788410764855, -6.9832966052786531, -28439.93363675462, -1.9900051910050358, 11646.201945786968, 0.0, -5.5553350055911563, 15.232267813669125, -1715.4112452773434, -0.88738793454143705, 1.8990620371672058, -6.6843474287487004, -8663.7289327848757, 1.3809447396152703, -8.2314516887106137, 31.449158261976809, -12399.336292725655, 1.5738267989284873, 2.2916348802571478, -21.641005881537744, -3086.2923096537161, 0.0, 1.4115522729848289, 6.6472201001285907, 6000.8464446290591, -2.8568932289040538, -1.6970166533337772, 0.57593634509976344, 1249.2911705694951, -0.69862274173754357, -3.6689381391771292, -2.4459395780040385, -7790.3648962766792, 6.5748470596485307, 2.3003743137674548, 1.6620347670442328, -8402.7090079943864, -1.8257404386133465]
        ),
    }
}

def get_aa(freqs):
    '''Return the AntennaArray to be used fro simulation.'''
    location = prms['loc']
    antennas = []
    nants = len(prms['antpos'])
    assert(len(prms['delays']) == nants and len(prms['amps']) == nants \
        and len(prms['bp_r']) == nants and len(prms['bp_i']) == nants)
    for i in range(len(prms['antpos'])):
        beam = prms['beam'](freqs, nside=128, deg=7)
        #bm_poly = n.reshape(n.array(prms['bm_poly'][i]), (6,3))
        try: beam.set_params(prms['bm_prms'])
        except(AttributeError): pass
        #beam = a.fit.BeamFlat(freqs)
        pos = prms['antpos'][i]
        dly = prms['delays'][i]
        amp = prms['amps'][i]
        bp_r = prms['bp_r'][i]
        bp_i = prms['bp_i'][i]
        off = prms['offsets'][i]
        antennas.append(
            a.fit.Antenna(pos[0],pos[1],pos[2], beam, delay=dly, offset=off,
                amp=amp, bp_r=bp_r, bp_i=bp_i)
        )
    #aa = a.fit.AntennaArray(prms['loc'], antennas)
    aa = XTalkAntennaArray(prms['loc'], antennas)
    aa.set_params(prms['aa'])
    return aa

src_prms = {
        'cyg': {
            'str': 10500,
            'index':-0.69
        },
        'cas': {
            'str': 9150,
            'index':-0.73,
        },
        'Sun': {
            'str': 56800,
            'index':0.55,
            'angsize':0.00875,
        },
        'vir': {
            'str': 1446,
            'index': -0.86,
        },
        'crab': {
            'str':  1838,
            'index': -0.30,
        },
}
