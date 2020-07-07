# Beer-Test
This repository contains an application which searches for the best route to visit as many breweries (factories) as it can. Optimization runs a [Genetic Algorithm for Travelling Salesman Problem](https://scikit-opt.github.io/scikit-opt/#/en/README?id=_22-genetic-algorithm-for-tsptravelling-salesman-problem) with the following constraints:
* Route has to be from home to home
* Euclidean distances are used from one point to another
* Max trip length can be 2000 km


The application returns the following outputs:
* Which factories were visited
* How many beer types were collected
* What distance was traveled
* Runtime

Additionally, an interactive map is provided. The map consists of home location and the complete route. Each location contains a popup with some supplementary information (coordinates, which brewery and what beers are available there).

## Instructions:

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


## Example output:

```
$ docker image build --tag satalia:beer .
Sending build context to Docker daemon  4.322MB
Step 1/8 : FROM python:3.8
 ---> 7f5b6ccd03e9
Step 2/8 : ENV VIRTUAL_ENV=/opt/venv
 ---> Using cache
 ---> 419725f973bc
Step 3/8 : RUN python3 -m venv $VIRTUAL_ENV
 ---> Using cache
 ---> e7c7ec9d4b48
Step 4/8 : ENV PATH="$VIRTUAL_ENV/bin:$PATH"
 ---> Using cache
 ---> aa7f9062567b
Step 5/8 : COPY requirements.txt .
 ---> Using cache
 ---> cadbef69f1b8
Step 6/8 : RUN pip install -r requirements.txt
 ---> Using cache
 ---> e5a7f2245e48
Step 7/8 : COPY ./ .
 ---> Using cache
 ---> 61c4e6871cd1
Step 8/8 : ENTRYPOINT ["python", "main.py"]
 ---> Using cache
 ---> 4a629690afd6
Successfully built 4a629690afd6
Successfully tagged satalia:beer
SECURITY WARNING: You are building a Docker image from Windows against a non-Windows Docker host. All files and directories added to build context will have '-rwxr-xr-x' permissions. It is recommended to double check and reset permissions for sensitive files and directories.
```

```
$ docker run -ti --name tmp satalia:beer /bin/true
Enter latitude and longitude separated by comma and a space (leave empty to skip and go with default coordinates): 
No input provided, running with default coordinates: (51.355468, 11.10079)
Found 34 factories:
-> Hasserder Brauerei (639); distance 59km
-> Gilde Brauerei (573); distance 148km
-> Brauerei Herrenhausen (212); distance 154km
-> Einbecker Brauhaus AG (484); distance 220km
-> Martini-Brauerei (832); distance 281km
-> Htt-Brauerei Bettenhuser (681); distance 288km
-> Warsteiner Brauerei (1337); distance 367km
-> Brauerei C. & A. Veltins GmbH & Co. (207); distance 388km
-> Licher Privatbrauerei (785); distance 488km
-> Binding Brauerei AG (125); distance 536km
-> Eder & Heylands (480); distance 570km
-> Brauhaus Faust (228); distance 597km
-> Wrzburger Hofbru AG (1374); distance 646km
-> Hochstiftliches Brauhaus in Bayern (661); distance 714km
-> Schlobrauerei Reckendorf (1114); distance 800km
-> Kaiserdom Privatbrauerei Bamberg (729); distance 813km
-> Brauerei Spezial (222); distance 816km
-> Brauerei Fssla (208); distance 816km
-> Heller Bru Trum (650); distance 816km
-> Klosterbru Bamberg (746); distance 817km
-> Privater Brauereigasthof Greifenklau (1024); distance 817km
-> Keesmann Bru (733); distance 819km
-> Bamberger Mahr's-Bru (70); distance 819km
-> Maisel Bru (819); distance 819km
-> St. GeorgenBru Modschiedler KG (1188); distance 833km
-> Tucher Bru (1290); distance 870km
-> Kaiser-Bru (728); distance 909km
-> Brauerei Gbr. Maisel KG (209); distance 944km
-> Kulmbacher Brauerei AG (757); distance 964km
-> Kulmbacher Mnchshof Bru (758); distance 964km
-> Gasthaus & Gosebrauerei Bayerischer Bahnhof (567); distance 1116km
-> Radeberger Exportbierbrauerei (1037); distance 1226km
-> Berliner Kindl Brauerei AG (103); distance 1382km
-> Berliner-Kindl-Schultheiss-Brauerei (104); distance 1387km
-> HOME (0); distance 1592km

Total distance traveled: 1592

Total unique beers collected:  79
-> Aecht Schlenkerla Rauchbier MÃ¤rzen
-> Aecht Schlenkerla Rauchbier Urbock
-> Aecht Schlenkerla Rauchbier Weizen
-> Bajuvator Doppelbock
-> Bamberger Gold
-> Bamberger Herren Pils
-> Bamberger SchwÃ¤rzla
-> Benediktiner Dunkel
-> Bockbier
-> Braunbier
-> Christmas Bock
-> Der Weisse Bock
-> Dunkel
-> Dunkles Hefe Weizen
-> EKU 28
-> EKU Pils
-> Edel-Pils
-> Eine Bamberger Weisse Hell
-> Eisbock
-> Export Premium
-> Gold-Pils
-> Gose
-> HefeweiÃŸbier
-> Hell
-> Helles Hefe Weizen
-> Julius Echter Hefe-WeiÃŸbier Hell
-> Kapuziner Gold
-> Kapuziner Kristall-Weizen
-> Kapuziner Schwarz-Weizen
-> Kapuziner WeiÃŸbier
-> Kasseler Premium Pils
-> Keller-Bier
-> Kellerbier
-> Konig Ludwig Weissbier
-> Kristall Weizen
-> KrÃ¤usen NaturtrÃ¼b
-> Lager
-> Lagerbier
-> Lindener Spezial
-> Luxus Pils
-> Maisel's Weisse Kristall
-> Meister Pilsener
-> Meranier Schwarzbier
-> MÃ¶nchshof KellerbrÃ¤u
-> MÃ¶nchshof Original Pils
-> MÃ¶nchshof Premium Schwarzbier
-> Original Berliner Weisse
-> Original Lager
-> Original Pils
-> Pils
-> Pilsener
-> Pilsner
-> Premium Pils
-> Premium Pils Edelherb
-> Premium Pilsener
-> Ratskeller
-> Rauchbier
-> Rauchbier Lager
-> Rauchbier MÃ¤rzen
-> Rauchbier Weissbier
-> ReichelbrÃ¤u Eisbock
-> Schlappeseppl Export
-> Schlenkerla Helles Lagerbier
-> Schwarzbier / Dunkel
-> Ungespundet Lager Hefetrub
-> Ungespundetes
-> Ur-Bock Hell
-> Warsteiner Premium Dunkel
-> Warsteiner Premium Oktoberfest
-> Warsteiner Premium Verum
-> Weissbier
-> Weissbier Dunkel
-> Weissbier Hell
-> Weisse
-> Weizen
-> Weizen Bier
-> Weizla Hell
-> Will-BrÃ¤u Ur-Bock
-> Zwergla

Map completed, saving as visited_factories.html

Total runtime: 0 days 00:00:59.997538
```
```
$ docker cp tmp:/visited_factories.html "C:\Users\mariu\REPOS\Satalia\output"
```

```
$ docker rm tmp
tmp
```