# Exploring official CT election data

The Secretary of the State's office published complete "real-time" election
data for the first time during the 2016 presidential election
[here](http://ctemspublic.pcctg.net/#/home). I air-quote "real-time" rather
than leave it out altogether, because the data was available as fast as the
SOTS and town clerks were able to get it into the system, but it wasn't all
available on election night. 100% of precincts were not reporting data
until a week after the election, and there were recounts required in state
legislature races. The results in the system were not marked "official"
until December. Still it was "good 'nuff for government work."

# total statewide vote results

The /output/merged_state_votes_pretty.csv file contains results (vote
counts and percents), candidate, office and party information for every
race on every ballot in every town in Connecticut for the Nov. 8
election. (It also includes write-in candidates who were not on the
ballot...).

Please feel free to use this for your own analysis. I'd be happy to hear
from you if you do, by emailing me at jkara@trendct.org, but it's not
required.

If you do any analysis, note that many candidates cross-endorsed. In those
cases, they appear in the table as separate candidates. You would need to
combine them to calculate accurate vote totals for a specific
individual. There were no cross endorsements in the presidential race.

Also note that districts don't apply to presidential, senate and other
local races. Zeros are filled in those columns.

If you want to parse out data that I haven't included in the spreadsheet
but which the SOTS' raw data includes, read on.

# /data/

There are two files that serve the state's election results interface, both
of which are in the /data/ foler of this repository:

* Electiondata_final.json
* Lookupdata_final.json

(the "_final" was added by me to denote the version of the file I
downloaded once the values were certified).

# parsing

I used these data files extensively to update data pages on [the election
blog and data portal I built for
TrendCT.org](https://blogotron.ctmirror.org/election-2016/).

It includes information on polling places, town an state election results,
lookup objects candidate names and parties.

The file election-sheets.py demonstrates how I accomplished some of the
parsing to populate these graphics. The product of this script are stored
in the /output/ foler of this repository, most notably in the file
"merged_state_votes_pretty.csv".

