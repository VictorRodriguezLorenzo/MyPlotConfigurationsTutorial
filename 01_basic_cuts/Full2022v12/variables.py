# variables

# 0 = not fold (default)
# 1 = fold underflow bin
# 2 = fold overflow bin
# 3 = fold underflow and overflow bins

# Toggle SR data blinding on/off
blindSR = True

blindCuts = {
    f'ttdm_sr_{category}': 'full'
    for category in cuts['ttdm_sr']['categories']
} if blindSR else {}

# variables
variables = {}

variables['events'] = {
    'name'  : '1',      
    'range' : (1,0,2),  
    'xaxis' : 'events', 
    'fold'  : 3,
    'blind' : blindCuts
}

#variables['nvtx'] = {     
#    'name'  : 'PV_npvsGood',      
#    'range' : (100, 0, 100),  
#    'xaxis' : 'number of vertices', 
#    'fold'  : 3,
#    'blind' : blindCuts
#}

variables['mll'] = {
    'name': 'mll',    
    'range' : (60,60,120), 
    'xaxis' : 'm_{ll} [GeV]',
    'fold' : 0,
    'blind' : blindCuts
}

variables['mth'] = {
    'name': 'mth',
    'range' : (60,0,300),
    'xaxis' : 'm_{T}^{H} [GeV]',
    'fold' : 0,
    'blind' : blindCuts
}

variables['mtw1']  = {
    'name': 'mtw1',
    'range' : (50, 0,200),
    'xaxis' : 'm_{T}^{W_{1}} [GeV]',
    'fold' : 0,
    'blind' : blindCuts
}

variables['mtw2']  = {
    'name': 'mtw2',
    'range' : (50, 0,100),
    'xaxis' : 'm_{T}^{W_{2}} [GeV]',
    'fold' : 0,
    'blind' : blindCuts
}

variables['ptll']  = {  
    'name': 'ptll',     
    'range' : (20, 0,200),   
    'xaxis' : 'p_{T}^{ll} [GeV]',
    'fold' : 0,
    'blind' : blindCuts
}

variables['drll']  = {
    'name': 'drll',
    'range' : (50, 0,5),
    'xaxis' : '#Delta R_{ll}',
    'fold' : 0,
    'blind' : blindCuts
}

variables['dphill']  = {
    'name': 'abs(dphill)',
    'range' : (50, 0,3.15),
    'xaxis' : '#Delta #phi_{ll}',
    'fold' : 0,
    'blind' : blindCuts
}

variables['detall'] = {
    'name'  : 'abs(detall)',
    'range' : (40, 0., 3.15),
    'xaxis' : '|#Delta#eta_{ll}|',
    'fold'  : 3,
    'blind' : blindCuts
}

variables['pt1']  = { 
    'name': 'Lepton_pt[0]',     
    'range' : (20,25,150),
    'xaxis' : 'p_{T} 1st lep',
    'fold'  : 3,                         
    'blind' : blindCuts
}

variables['pt2']  = {
    'name': 'Lepton_pt[1]',     
    'range' : (20,0,125),   
    'xaxis' : 'p_{T} 2nd lep',
    'fold'  : 3,                        
    'blind' : blindCuts
}

variables['pt3']  = {
    'name': 'Lepton_pt[2]',
    'range' : (20,0,100),
    'xaxis' : 'p_{T} 3rd lep',
    'fold'  : 3,
    'blind' : blindCuts
}

variables['eta1']  = {
    'name': 'Lepton_eta[0]',     
    'range' : (40,-3,3),   
    'xaxis' : '#eta 1st lep',
    'fold'  : 3,                         
    'blind' : blindCuts
}

variables['eta2']  = {
    'name': 'Lepton_eta[1]',     
    'range' : (40,-3,3),   
    'xaxis' : '#eta 2nd lep',
    'fold'  : 3,                        
    'blind' : blindCuts
}

                        
variables['phi1']  = {
    'name': 'Lepton_phi[0]',
    'range' : (20,-3.2,3.2),
    'xaxis' : '#phi 1st lep',
    'fold'  : 3,
    'blind' : blindCuts
}

variables['phi2']  = {
    'name': 'Lepton_phi[1]',
    'range' : (20,-3.2,3.2),
    'xaxis' : '#phi 2nd lep',
    'fold'  : 3,
    'blind' : blindCuts
}


# MET

variables['puppimet']  = {
    'name': 'PuppiMET_pt',
    'range' : (20,0,200),
    'xaxis' : 'Puppi MET p_{T} [GeV]',
    'fold' : 3,
    'blind' : blindCuts
}

variables['mpmet']  = {
    'name': 'mpmet',
    'range' : (40,0,100),
    'xaxis' : 'Min. proj. MET p_{T} [GeV]',
    'fold' : 3,
    'blind' : blindCuts
}

variables['njet']  = {
    'name': 'njets',
    'range' : (5,1,5),
    'xaxis' : 'Number of jets',
    'fold' : 2,
    'blind' : blindCuts
}

variables['nbjet']  = {
    'name': 'nbjets',
    'range' : (5,1,5),
    'xaxis' : 'Number of b-jets',
    'fold' : 2,
    'blind' : blindCuts
}

variables['vht_pt'] = {
    'name': 'vht_pt',
    'range': (40, 0, 800),
    'xaxis': 'p_{T}(#ell#ell + jets) [GeV]',
    'fold': 2,
    'blind' : blindCuts
}

variables['jetpt1']  = {
    #'name': 'Alt(CleanJet_pt, 0, -99) - 9999.9*(CleanJet_pt[0]<30)',
    'name': 'Alt(CleanJet_pt, 0, -99)',
    'range' : (40,0,200),
    'xaxis' : 'p_{T} 1st jet',
    'fold' : 0,
    'blind' : blindCuts
}

variables['jetpt2']  = {
    #'name': 'Alt(CleanJet_pt, 1, -99)  - 9999.9*(CleanJet_pt[1]<30)',
    'name': 'Alt(CleanJet_pt, 1, -99)',
    'range' : (40,0,200),
    'xaxis' : 'p_{T} 2nd jet',
    'fold' : 0,
    'blind' : blindCuts
}

variables['jeteta1']  = {
    #'name': 'Alt(CleanJet_eta, 0, -99) - 9999.9*(CleanJet_pt[0]<30)',
    'name': 'Alt(CleanJet_eta, 0, -99)',
    'range' : (30,-4.7,4.7),
    'xaxis' : '#eta 1st jet',
    'fold' : 0,
    'blind' : blindCuts
}

variables['jeteta2']  = {
    #'name': 'Alt(CleanJet_eta, 1, -99) - 9999.9*(CleanJet_pt[1]<30)',
    'name': 'Alt(CleanJet_eta, 1, -99)',
    'range' : (30,-4.7,4.7),
    'xaxis' : '#eta 2nd jet',
    'fold' : 0,
    'blind' : blindCuts
}

