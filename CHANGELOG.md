2.2.6 - 20.12.2015
==============

* Rename the repository 

2.2.6 - 25.08.2015
==============

* Remove the container checks from core (moved to plugins)

2.2.4 - 27.06.2015
==============

* Fix a Python shared memory permission issue on older distros

2.2.3 - 12.06.2015
==============

* Docker container module fixes


2.2.1 - 09.06.2015
==============

* Collects facts about the distro with a ported Ansible module
* Container module fixes
* Updated requirements

2.2 - 06.06.2015
==============

* Containers monitoring

2.1 - 24.04.2015
==============

* Support for custom table data from MySQL, Nginx, Apache, PostgreSQL, MongoDB

**MySQL** 
* Tables and index sizes
* Slow queries

**PostgreSQL**
* Tables and index sizes
* Slow queries
* Index Hit rate

**Nginx**
* Requests - bytes, hits, percent, url
* Not found - bytes, hits, percent, url

**Apache**
* Requests - bytes, hits, percent, url
* Not found - bytes, hits, percent, url

**MongoDB**
* Collections and index sizes
* Slow queries

2.0 - 15.02.2015
==============

* IP Address collector - collect only local info
* Checker fixes
* Custom plugins


1.9.8 - 24.10.2014
==============

* CentOS plugin dir permissions (Fixing the error when running amonpm update)
* Update from github before install

1.9.7 - 22.10.2014
==============

* CentOS improvements and bug fixes
* Simplified Distro detection


1.9.6 - 20.10.2014
==============

* Debian installation fixes


1.9.5 - 16.10.2014
==============

* Plugins check refactoring


1.9 - 04.09.2014
==============

* APT/RPM installation refactoring

1.8.1 - 01.09.2014
==============

* Plugins refactoring


1.8 - 26.08.2014
==============

* Fixed memory leak in the Plugins config reader


1.7 - 21.08.2014
==============

* Stability improvements

1.6
==============

* amonpm - Uninstall method, Install updates the plugins by default

1.5.5
==============

* Fix Memory allocation issue in loadavg

1.5.4
==============

* Fix Debian uninstall script

1.5.3
==============

* Stability bug fixes

1.5.2
==============

* API Check fixes - test using the real server key

1.5.1
==============

* Ignore curl certificate check (--insecure) option

1.5
==============

* Install plugins from the command line - /etc/init.d/amon-agent install mysql
* Security update - the daemon for the agent runs under the amonagent user instead of root


1.3
==============

* Install all available plugins with the agent

1.2
==============

* Fix installation - install both setuptools and pip
* Don't break the agent if the plugin directories doesn't exist (/etc/amoagent/plugins)

1.1
==============

* Information about package updates

1.0.3
==============

* Processes - read/write per second

0.7.5
==============

* Fix locale issues in the process collector module

0.7.4
==============

* Increase the API call timeout to 10 seconds, raise an exception if there is an error

0.7.3
==============

* Remove detailed disk usage collector - too slow on big volumes

0.7.2
==============

* Connection pooling to the API instead of posts - fixes the bug where the agent stops sending information after amon.cx is restarted
* Uptime data

0.7.1
==============

* Improved OS detection (detects Ubuntu, Debian, CentOS, Fedora and Amazon AMI)
* Uptime data

0.7
===============

* Server public IP Address
* Distro info
