# nmeasnitch
nmeasnitch is a tool to detect GPS spoofing by looking at the nmea sentences. This was presented at [Defcon 25 2017](https://www.defcon.org/html/defcon-25/dc-25-speakers.html#Robinson)

## Requirements
1. python3-serial
1. A GPS Device that will talk to [GPSd](http://www.catb.org/gpsd/)
1. GPSd installed

## Running
1. Configure options in nmeasnitch.cfg
1. Run nmeasnitch `./nmeasnitch.py`
1. Use rate.sql to see if the rates are changing.
