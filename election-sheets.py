# Hacking CT Election data with python
# by Jake Kara

import json, pandas as pd, numpy  as np
from dateutil.parser import parse

class CTElection:
    # read data files, final, official data from CT SOTS website

    def __init__(self, edata_filename="data/Electiondata_final.json",
                 ldata_filename="data/Lookupdata_final.json"):
        
        # edata - election data; this contains results data
        self.edata = json.loads(open(edata_filename).read())

        # ldata - lookup data; this contains meta data and information on
        # non-results, such as canidate names and polling places
        self.ldata = json.loads(open(ldata_filename).read())

    # Return the name of the election
    def name(self):
        return self.ldata["election"]["DNM"]

    # Return the date of the election as a date, not a string
    def date(self):
        return parse(self.ldata["election"]["DT"])

    def unweird(self, obj, fieldName="weird"):
        # many arrays in the election system contain a weird structure. Here's an example with ldata["officeList"]
        # the objects have one index, which is the id of the office.
        # we need to get that id to access its value, and the data in there is what we want.
        # Yep, it's weird. Why not just a dictionary with these as keys? I don't know.
        # Here's an example 
        # [{...},...,{u'306': {u'OO': u'223', u'D': u'0', u'DT': u'', u'OT': u'SM', u'ID': u'306', u'NM': u'Registrar of Voters - Danbury'}}]

        k = obj.keys()[0]

        ret = obj[k]
        ret[fieldName] = k
        return ret
    
    # Return a list of offices
    def offices(self):
        ret = []
        arr = self.ldata["officeList"]
        for obj in arr:
            ret.append(self.unweird(obj))
        return pd.read_json(json.dumps(ret)).set_index("ID")

    def stateVotes(self):
        votes = self.edata["stateVotes"]
        ret = []

        for k in votes.keys():
            obj = votes[k]
            # obj contains an object for each candidate
            for cand in obj:
                candResult = self.unweird(cand, "candId")
                candResult["officeId"] = k
                ret.append(candResult)
                
        return pd.read_json(json.dumps(ret)).set_index("candId")

    def parties(self):
        parties =  self.ldata["partyIds"]
        partyLookup = {}
        ret = []
        
        for pId in parties.keys():
            obj = parties[pId]
            obj["partyId"] = pId
            ret.append(obj)

        return pd.read_json(json.dumps(ret)).set_index("partyId")
    
    def candidates(self):
        cands = self.ldata["candidateIds"]
        ret = []
        for candId in cands.keys():
            obj = cands[candId]
            obj["candId"] = candId
            ret.append(obj)
        ret = pd.read_json(json.dumps(ret))#.set_index(candId)

        ret.set_index("candId")
        ps = self.parties()
        ret = ret.join(ps, on="P", how="left", lsuffix="_CAND", rsuffix="_PARTY")
        ret.set_index("candId")
        return ret

# Generating some reports...

e = CTElection()    

print "Parsing data for election '" + e.name() + "' which occurred on " + str(e.date())

print "Generating output/office_list.csv..."
e.offices().to_csv("output/office_list.csv",index=False)

print "Generating output/state_votes.csv..."
e.stateVotes().sort_index().to_csv("output/state_votes.csv")

print "Generating output/candidate_names.csv..."
e.candidates().sort_values(by="candId").to_csv("output/candidate_names.csv",index=False)

print "Generating output/merged_state_votes.csv..."

e.stateVotes()\
 .join(e.candidates().set_index("candId"),how="left")\
 .set_index("officeId")\
 .join(e.offices(),how="left", rsuffix="_OFFICE")\
 .sort_index().to_csv("output/merged_state_votes.csv",
                      index=False)

# Generate a prettier version of merged
# Get rid of dumb columns
print "Generating output/merged_state_votes_pretty.csv"
pretty = e.stateVotes()\
 .join(e.candidates().set_index("candId"),how="left")\
 .set_index("officeId")\
 .join(e.offices(),how="left", rsuffix="_OFFICE")\
 .sort_index()

pretty = pretty[[
    "NM","D","DT",
    "NM_CAND","LN","FN","MN","AD",
    "NM_PARTY","CD",
    "TO","V"
    ]]

pretty.columns = "office", "district_code","district_name",\
                 "cand_full_name","cand_lname","cand_fname","cand_mname","cand_address",\
                 "party_name","party_abbr",\
                 "vote_pct","vote_count"


pretty.to_csv("output/merged_state_votes_pretty.csv",
                      index=False)
