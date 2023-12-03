# election
Modeling election formats

This program simulates elections with one of the following three formats:
 - Partisan primary with plurality voting
 - Final four primary with plurality voting
 - Final four primary with ranked choice voting

Additionally, the user can choose the breakdown of the district (% republican/democrat), the number of voters, the number of politicians running from each party, and the number of times the simulation should be run.

The simulation will return the average result, average absolute vote, average vector istance from the median, and average scalar distance from the median.

This program makes the following assumptions: 
- Everyone who votes in the primary votes in the general
- The same number of politicians run from each party
- Each voter and candidate has a value on the ideological spectrum where positive numbers are republicans and negative numbers are democrats
- The parties are normally distributed with a mean of 1 for republicans and -1 for democrats (meaning true center is 0)
- Each voter votes for the candidate closest to their ideological value, and they rank candidates by distance for ranked choice voting