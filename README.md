JAST v 0.3.0
============
Jast (Just Another Screenshot Tool) is a tool that can be used to automate the 
process for screenshots of webhosts. Jast uses the Selenium webdriver and the
Firefox browser for image capture and writes all results to the specified output
folder.

Requirements
------------
Jast requires Python>=3.7.1 in order to operate along with geckodriver>=0.23.0
and Firefox>=64.0.2.

Python-specific requirements can be found in the requirements.txt file.

Installation
------------
To install Jast, it's recommended to setup a Pipenv shell in order to prevent
the module installation from affecting yout other Python tools. This can be done
via the follwing:
`$ pipenv shell`

To install any requirements, once in the Pipenv shell run:
`$ pip install -r requirements.txt`

Usage
-----
Running Jast is relatively straightforward. Jast requires either a single URL or
a list of hosts to screenshot along with a directory to write the report to.
Hosts should be in the format http(s)://<host>:<port>. Hosts not in this format
will generate an error message and will be skipped.

**Single URL Example**
`$ jast.py -u https://www.example.com -o /path/for/report`

**Multiple Host File**
`$ jast.py -f /path/to/hosts -o /path/for/report`

Additionally, Jast supports a variety of flags to deal with common scenarios
that may arise with webhosts, such as redirects. If you want to have Jast follow
redirects before taking a screenshot supply the `--follow-redirects` flag.

**Following Redirects**
`$ jast.py -u http://www.example.com -o /path/for/report --follow-redirects`

If you want Jast to also document any headers that are sent from the webhost, 
use the `--headers` flag, and Jast will write all received headers below the
captured screenshot.

**Capturing Headers**
`$ jast.py -u http://www.example.com -o /path/for/report --headers`

Finally, you can control the image size by passing a `--size` parameter to 
specify the size of the browser window. By default, Jast will use a window size
of 800x600.

**Changing Window Size**
`$ jast.py -u http://www.exmaple/com -o /path/for/report --size=1024x768`

Output
------
Jast writes an HTML report in the specified output folder containing a 
*report.html* file and some associated style documents. All screenshots are
saved in the */screenshots/* subfolder. The image below shows an example report
that is created when scanning a multiple hosts using Jast and including the 
`--headers` flag:

![Example Report](./jast-report-sample.png?raw=true)

