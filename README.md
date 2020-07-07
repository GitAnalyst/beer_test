# Beer-Test
This repository contains an application which searches for the best route to visit as many breweries (factories) as it can, with the following constraints:
* Route has to be from home to home
* Euclidean distances are used from one point to another
* Max trip length can be 2000 km


The application returns the following outputs:
* Which factories were visited
* How many beer types collected
* What distance was traveled
* Runtime

Additionally, an interactive map is provided. The map consists of home location and the complete route. Each location contains a popup with some supplementary information (coordinates, which brewery and what beers are available there).

To run the application, clone the repository and in the root directory run the following commands (this requires docker and was tested on Windows machine with bash console):

### 1. Execute steps in dockerfile (install dependencies) and create a docker image with a specific tag.
`docker image build --tag satalia:beer .`
### 2. Run optimization algorithm which returns above mentioned outputs.
#### 2.1. Search for factories and find the best route. This prompts for input coordinates. Runtime depends on the number of nearby factories by the input location (should be between seconds to couple of minutes).
`docker run -ti --name tmp satalia:beer /bin/true`
#### 2.2. Copy created visualization of the route from container to local machine. The last argument (in quotes) requires full path to the repository on your local machine.
`docker cp tmp:/visited_factories.html "FULL\PATH\TO\REPOSITORY\output"`
#### 2.3. Remove container "tmp". This is required if you want to rerun the search (step 2.1.) 
`docker rm tmp`
