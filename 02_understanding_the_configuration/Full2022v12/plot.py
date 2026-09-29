import ROOT

def C(hex_code):
    return ROOT.TColor.GetColor(hex_code)

###########################################
######## CMS / CVD-FRIENDLY COLORS ########
###########################################

cms_cb = {
    # Official 10-color CVD-friendly sequence https://arxiv.org/pdf/2107.02270
    'blue'        : C('#3F90DA'),  # 63, 144, 218
    'orange'      : C('#FFA90E'),  # 255, 169, 14
    'red'         : C('#BD1F01'),  # 189, 31, 1
    'gray'        : C('#94A4A2'),  # 148, 164, 162
    'purple'      : C('#832DB6'),  # 131, 45, 182
    'brown'       : C('#A96B59'),  # 169, 107, 89
    'dark_orange' : C('#E76300'),  # 231, 99, 0
    'tan'         : C('#B9AC70'),  # 185, 172, 112
    'dark_gray'   : C('#717581'),  # 113, 117, 129
    'light_blue'  : C('#92DADD'),  # 146, 218, 221
    'extra_pink'  : C('#C849A9'),  # 200, 73, 169

    'sig_red_1'   : C('#FF0000'),  # pure red
    'sig_red_2'   : C('#990000'),  # dark red
    'sig_red_3'   : C('#FF4500'),  # orange red
    'sig_red_4'   : C('#B00050'),  # wine / magenta-red
    'sig_red_5'   : C('#FF1493'),  # deep pink
    'sig_red_6'   : C('#8B0000'),  # dark red
    'sig_red_7'   : C('#DC143C'),  # crimson

    'black'       : C('#000000'),
}


###########################################
############### GROUP PLOT ################
###########################################

groupPlot = {}

###########################################
#############  BACKGROUNDS  ###############
###########################################

# smaller backgrounds first -> lower in stack and first in legend

groupPlot['VVV']  = {
    'nameHR'   : 'VVV',
    'isSignal' : 0,
    'color'    : cms_cb['light_blue'],
    'samples'  : ['WWW', 'WWZ', 'WZZ', 'ZZZ']
}

groupPlot['VV']  = {
    'nameHR'   : 'VV',
    'isSignal' : 0,
    'color'    : cms_cb['blue'],
    'samples'  : ['WW', 'WZ', 'ZZ']
}

groupPlot['TXX']  = {
    'nameHR'   : 't + X',
    'isSignal' : 0,
    'color'    : cms_cb['purple'],
    'samples'  : ['tHW', 'tHQ']
}

groupPlot['TTToSemiLeptonic']  = {
    'nameHR'   : 't#bar{t}(1l)',
    'isSignal' : 0,
    'color'    : cms_cb['gray'],
    'samples'  : ['TTToSemiLeptonic']
}

groupPlot['ttH'] = {
    'nameHR'   : 'ttH',
    'isSignal' : 0,
    'color'    : cms_cb['dark_orange'],
    'samples'  : ['ttH']
}

groupPlot['ttW'] = {
    'nameHR'   : 'ttW',
    'isSignal' : 0,
    'color'    : cms_cb['brown'],
    'samples'  : ['ttW']
}

groupPlot['ttZ'] = {
    'nameHR'   : 'ttZ',
    'isSignal' : 0,
    'color'    : cms_cb['extra_pink'],
    'samples'  : ['ttZ']
    #'samples'  : ['TTNuNu', 'TTLL_MLL-4to50', 'TTLL_MLL-50', 'TTZ-ZtoQQ']
    #'samples'  : ['TTLL_MLL-4to50', 'TTLL_MLL-50', 'TTZ-ZtoQQ']
    #'samples'  : ['TTNuNu']
}

groupPlot['DY']  = {
    'nameHR'   : 'DY',
    'isSignal' : 0,
    'color'    : cms_cb['tan'],
    'samples'  : ['DY']
}

groupPlot['ST']  = {
    'nameHR'   : 'Single Top',
    'isSignal' : 0,
    'color'    : cms_cb['orange'],
    'samples'  : ['ST']
}

groupPlot['TTTo2L2Nu']  = {
    'nameHR'   : 't#bar{t}(2l)',
    'isSignal' : 0,
    'color'    : cms_cb['red'],
    'samples'  : ['TTTo2L2Nu']
}

groupPlot['Fake'] = {
        'nameHR': 'Nonprompt',
        'isSignal': 0,
        'color': 921,
        'samples': ['Fake']
}

###########################################
################## PLOT ###################
###########################################

plot = {}

###########################################
#############  BACKGROUNDS  ###############
###########################################

# smaller backgrounds first -> lower in stack

plot['WWW']  = {
    'color'    : cms_cb['light_blue'],
    'isSignal' : 0,
    'isData'   : 0,
    'scale'    : 1.0,
}

plot['WWZ']  = {
    'color'    : cms_cb['light_blue'],
    'isSignal' : 0,
    'isData'   : 0,
    'scale'    : 1.0,
}

plot['WZZ']  = {
    'color'    : cms_cb['light_blue'],
    'isSignal' : 0,
    'isData'   : 0,
    'scale'    : 1.0,
}

plot['ZZZ']  = {
    'color'    : cms_cb['light_blue'],
    'isSignal' : 0,
    'isData'   : 0,
    'scale'    : 1.0,
}

plot['WW']  = {
    'color'    : cms_cb['blue'],
    'isSignal' : 0,
    'isData'   : 0,
    'scale'    : 1.0,
}

plot['WZ']  = {
    'color'    : cms_cb['blue'],
    'isSignal' : 0,
    'isData'   : 0,
    'scale'    : 1.0,
}

plot['ZZ']  = {
    'color'    : cms_cb['blue'],
    'isSignal' : 0,
    'isData'   : 0,
    'scale'    : 1.0,
}

plot['tHW']  = {
    'color'    : cms_cb['purple'],
    'isSignal' : 0,
    'isData'   : 0,
    'scale'    : 1.0,
}

plot['tHQ']  = {
    'color'    : cms_cb['purple'],
    'isSignal' : 0,
    'isData'   : 0,
    'scale'    : 1.0,
}

plot['TTToSemiLeptonic']  = {
    'color'    : cms_cb['gray'],
    'isSignal' : 0,
    'isData'   : 0,
    'scale'    : 1.0,
}

plot['ttH']  = {
    'color'    : cms_cb['dark_orange'],
    'isSignal' : 0,
    'isData'   : 0,
    'scale'    : 1.0,
}

plot['ttW']  = {
    'color'    : cms_cb['brown'],
    'isSignal' : 0,
    'isData'   : 0,
    'scale'    : 1.0,
}

plot['ttZ'] = {
    'color'    : cms_cb['extra_pink'],
    'isSignal' : 0,
    'isData'   : 0,
    'scale'    : 1.0,
}

#plot['TTNuNu'] = {
#    'color'    : cms_cb['extra_pink'],
#    'isSignal' : 0,
#    'isData'   : 0,
#    'scale'    : 1.0,
#}
#
#plot['TTLL_MLL-4to50'] = {
#    'color'    : cms_cb['extra_pink'],
#    'isSignal' : 0,
#    'isData'   : 0,
#    'scale'    : 1.0,
#}
#
#plot['TTLL_MLL-50'] = {
#    'color'    : cms_cb['extra_pink'],
#    'isSignal' : 0,
#    'isData'   : 0,
#    'scale'    : 1.0,
#}
#
#plot['TTZ-ZtoQQ'] = {
#    'color'    : cms_cb['extra_pink'],
#    'isSignal' : 0,
#    'isData'   : 0,
#    'scale'    : 1.0,
#}

plot['DY']  = {
    'color'    : cms_cb['tan'],
    'isSignal' : 0,
    'isData'   : 0,
    'scale'    : 1.0,
}

plot['ST']  = {
    'color'    : cms_cb['orange'],
    'isSignal' : 0,
    'isData'   : 0,
    'scale'    : 1.0,
}

plot['TTTo2L2Nu']  = {
    'color'    : cms_cb['red'],
    'isSignal' : 0,
    'isData'   : 0,
    'scale'    : 1.0,
}

plot['Fake'] = {
        'color': 921,
        'isSignal': 0,
        'isData': 0,
        'scale': 1.0
        }

###########################################
#################  DATA  ##################
###########################################

plot['DATA']  = {
    'nameHR'   : 'Data',
    'color'    : cms_cb['black'],
    'isSignal' : 0,
    'isData'   : 1,
    'isBlind'  : 0
}

###########################################
################ LEGEND ###################
###########################################

legend = {}
legend['lumi'] = 'L = 7.98 fb^{-1}'
legend['sqrt'] = '#sqrt{s} = 13.6 TeV'
