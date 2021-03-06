#!/usr/bin/python
import logging
import sys, time

try:
	import amonagent
except:
	print 'amonagent is not installed'
	sys.exit()

from amonagent.log import initialize_logging; initialize_logging('amonagent')

from amonagent import __version__
from amonagent.daemon import Daemon
from amonagent.settings import settings
from amonagent.runner import runner
from amonagent.remote import Remote
from amonagent.check import test_checks, test_plugins # Test plugins and collectors

PIDFILE = settings.PIDFILE
log = logging.getLogger(__name__)


class AmonAgentDaemon(Daemon):

	def start(self):
		system_info = runner.info()
	
		remote = Remote()

		remote.save_system_info(system_info)

		super(AmonAgentDaemon, self).start()
		

	def run(self):
		while True:
			stats = {
				'system': runner.system(),
				'processes': runner.processes(),
				'plugins': runner.plugins(),
			}
			remote = Remote()
			remote.save_system_stats(stats)
				
			time.sleep(settings.SYSTEM_CHECK_PERIOD)

if __name__ == "__main__":

	daemon = AmonAgentDaemon(PIDFILE)

	if len(sys.argv) >= 2:
		if 'start' == sys.argv[1]:
			try:
				daemon.start()
				print "Starting amonagent {0}...".format(__version__)
			except Exception, e:
				print "amonagent couldn't be started. Please check {0} for details".format(settings.LOGFILE)
				log.exception("The agent couldn't be started")
		elif 'stop' == sys.argv[1]:
			print "Stopping amonagent ..."
			daemon.stop()
		elif 'restart' == sys.argv[1]:
			print "Restaring amonagent ..."
			daemon.restart()
		elif 'test' == sys.argv[1]:
			test_checks()
		elif 'test_plugins' == sys.argv[1]:
			try:
				name = sys.argv[2]
			except:
				name = None
			test_plugins(name=name)
		elif 'status' == sys.argv[1]:
			try:
				pf = file(PIDFILE,'r')
				pid = int(pf.read().strip())
				pf.close()
			except IOError:
				pid = None
			except SystemExit:
				pid = None

			if pid:
				print 'amonagent {0} is running as pid {1}'.format(__version__, pid)
			else:
				print 'amonagent is not running.'


