# Dot2Moon
Tool that checks for path traversal traces in a given web application url using GET and POST methods, plus it is capable of multi-threading, set timeout and 5-layers verification.

## What are the 5-layers?

**1. Check HTTP response code**  
If response code is different of 200, it will be dscarted

**2. Verify response content**  
At the start, the program obtain a "default" error response from the website. At this step, it will compare the default error page to the actual payload response

**3. Verify if payload was returned**  
If the payload itself was returned in source, then probably there's an error message, like: "Could not retrieve ../../../etc/passwd"

**4. Verify specific strings**  
If strings like: "Not Found, "Not be found" and others are found, then it is discarted

**5. Verify page size**  
Similar to verification 2, but this time it uses the response size as criteria

#### On POST method, it only uses 2 Layers:   
**1. Verify response content**  
At the start, the program obtain a "default" error response from the website. At this step, it will compare the default error page to the actual payload response  

**2. Verify specific strings**  
If strings like: "Not Found, "Not be found" and others are found, then it is discarted

If the request go through all this testing layers, then it will be labed as "Potential". All resquests that return 200 will be added to a second list, so the user can verify it by himself is wish

## Dependencies
* Git (Linux)
* Python 3.x
* [Colorama](https://pypi.python.org/pypi/colorama)
 
## Installing
#### Linux
**Debian**  
`sudo apt-get install git python3 python3-pip`  
`sudo pip3 install colorama`  
**Arch**  
`sudo pacman -S git python python-pip`  
`sudo pip install colorama`  

#### Windows
Download and install [Python 3.x](https://www.python.org/downloads/windows/) and [Colorama](https://pypi.python.org/pypi/colorama)
## Running
`python dot2moon.py --help`  
```
usage: dot2moon.py [-h] -u U -w W [-v] [-t T] [-p P] [-o O] [-c C]
                   [--user-agent USERAGENT] [--ignore IGNORE]
                   [--timeout TIMEOUT] [--random-agent] [--timeset TIMESET]

Path Traversal tester and validator

optional arguments:
  -h, --help                                  show this help message and exit
  -u U                                           Target site
  -w W                                         Wordlist used to test
  -v                                               Verbose, details every step
  -t T                                             Number of threads that will be executed (default = 4)
  -p P                                            POST explotation. Inform parameter
  -o O                                           Save results to file
  -c C                                            Define how many characters of HTML will be shown
  --user-agent USERAGENT     Change requests User-Agent
  --ignore IGNORE                     Look for specific string in HTML. If found, discart page
  --timeout TIMEOUT                 Set timeout
  --random-agent                     Set random user agent
  --timeset TIMESET                  Set time between requests
```
## Exemples
* Basic Usage  
`python dot2moon.py -u website.com/catalog.php?src= -w wordlists/wl.txt`  

* Changing number of threads, enabling verbose and outputing to file  
`python dot2moon.py -u website.com/catalog.php?src= -w wordlists/wl.txt -t 7 -v -o output.txt`  

* Avoid being blocked by changing User Agent and setting a wait time between requests  
`python dot2moon.py -u website.com/catalog.php?src= -w wordlists/wl.txt --random-agent --timeset 5`  
***Note: This option does not support multi-threading***  

* If target website is lagging, try to increase timeout  
 `python dot2moon.py -u website.com/catalog.php?src= -w wordlists/wl.txt --timeout 15`  

* If the website returns some string that indicates that the url is not vulnerable, you can add it as filter  
`python dot2moon.py -u website.com/catalog.php?src= -w wordlists/wl.txt --ignore Warning`  

* Specify User Agent  
`python dot2moon.py -u website.com/catalog.php?src= -w wordlists/wl.txt --user-agent 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.119 Safari/537.36'`  

* POST Injection Method  
`python dot2moon.py -u website.com/catalog/?page=text-file-viewer.php -p 'textfile=PAYLOAD&text-file-viewer-php-submit-button=ViewFile'  -w wordlists/wl.txt`  
***Note: Injection point must be replaced with "PAYLOAD" in order to identify where the payloads shaw be injected***

## Screenshots

* Help
![print](https://imgur.com/3IMpC55)
* POST
![print](https://imgur.com/CBE18n6)
* GET
![print](https://imgur.com/YbATAre)
* Results
![print](https://imgur.com/3IMpC55)
![print](https://imgur.com/qbKuohh)

## License
check [License](https://github.com/PsiqueLabs/dot2moon/blob/master/LICENSE) for more details.  
