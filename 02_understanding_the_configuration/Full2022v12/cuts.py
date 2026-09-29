cuts = {}

# Common dilepton preselection. Object IDs and corrections are already configured elsewhere
# In Run3, an issue with the jets in the region of 2.6 < abs(CleanJet_eta[i]) < 3.1 (https://cms-talk.web.cern.ch/t/follow-up-on-eta-horns-in-2022/33524)
preselections = '''
    Lepton_pt[0] > 25
    && Lepton_pt[1] > 20
    && mll > 20
    && Alt(Lepton_pt, 2, 0) < 10
    && noJetInHorn     
'''

# DYtautauCR →  low mll, low ptll, b-veto
cuts['DYtautauCR'] = {
    'expr': 'ptll < 30 && mll < 85 && bVeto && Lepton_pdgId[0]*Lepton_pdgId[1] == -11*13',
    'categories': {
        '0j' : 'Alt(CleanJet_pt,0, 0.0)<30.0',
       '1j' : 'Alt(CleanJet_pt,0, 0.0)>30.0 && Alt(CleanJet_pt,1, 0.0)<30.0',
       '2j' : 'Alt(CleanJet_pt,0, 0.0)>30.0 && Alt(CleanJet_pt,1, 0.0)>30.0 && Alt(CleanJet_pt,2, 0.0)<30.0',
       '3j' : 'Sum(CleanJet_pt>30.0)>=3',
       'Inc': '1',
        },
}

# WWSR →  high mll, b-veto
cuts['WWSR'] = {
    'expr': 'mll > 85 && bVeto && Lepton_pdgId[0]*Lepton_pdgId[1] == -11*13',
    'categories': {
        '0j' : 'Alt(CleanJet_pt,0, 0.0)<30.0 ',
        '1j' : 'Alt(CleanJet_pt,0, 0.0)>30.0 && Alt(CleanJet_pt,1, 0.0)<30.0 ',
        '2j' : 'Alt(CleanJet_pt,0, 0.0)>30.0 && Alt(CleanJet_pt,1, 0.0)>30.0 && Alt(CleanJet_pt,2, 0.0)<30.0',
        '3j' : 'Sum(CleanJet_pt>30.0)>=3',
        'Inc': '1',
        },
}

# Top_CR →  high mll, b-required
cuts['Top_CR']  = {
    'expr' : 'mll > 85 && bReq && Lepton_pdgId[0]*Lepton_pdgId[1] == -11*13',
    'categories' : {
        '1j' : 'Alt(CleanJet_pt,0, 0.0)>30.0 && Alt(CleanJet_pt,1, 0.0)<30.0',
        '2j' : 'Alt(CleanJet_pt,0, 0.0)>30.0 && Alt(CleanJet_pt,1, 0.0)>30.0 && Alt(CleanJet_pt,2, 0.0)<30.0',
        '3j' : 'Sum(CleanJet_pt>30.0)>=3',
        'Inc' : '1',
    }
}
