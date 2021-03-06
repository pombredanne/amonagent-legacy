import imp
import os
import re
import logging

from decimal import Decimal
from datetime import timedelta, datetime

try:
	import json
except ImportError:
	import simplejson as json

from amonagent.settings import settings


# CONSTANTS
AMONAGENT_PATH = "/etc/amonagent"
ENABLED_PLUGINS_PATH = "{0}/plugins-enabled".format(AMONAGENT_PATH)


class PluginMount(type):
	"""
	A plugin mount point derived from:
		http://martyalchin.com/2008/jan/10/simple-plugin-framework/
	Acts as a metaclass which creates anything inheriting from Plugin
	"""
 
	def __init__(cls, name, bases, attrs):
		"""Called when a Plugin derived class is imported"""
 
		if not hasattr(cls, 'plugins'):
			# Called when the metaclass is first instantiated
			cls.plugins = []
		else:
			# Called when a plugin class is imported
			name  = attrs["__module__"]

			cls.register_plugin(cls, name)
 
	def register_plugin(cls, plugin, name):
		"""Add the plugin to the plugin list and perform any registration logic"""
 
		# create a plugin instance and store it
		# optionally you could just store the plugin class and lazily instantiate
		instance = plugin(name)
		# save the plugin reference
		cls.plugins.append(instance)
 

class AmonPlugin(object):

	__metaclass__ = PluginMount


	def __init__(self, name):
		self.name = name


		self.log = logging.getLogger('%s.%s' % (__name__, name))

		
		self.config = self._get_configuration_file()
		self.result = {'gauges': {}, 'counters': {}, 'versions': {}, 'error': False}


	def _get_configuration_file(self):
		
		filename = "{0}/{1}.conf".format(ENABLED_PLUGINS_PATH, self.name)
		config = {}
		
		
		try:
			with open(filename, 'r') as f:
				config_file = f.read()
				config = json.loads(config_file)
		except Exception, e:
			error_message = "There was an error in your configuration file ({0})".format(filename)
			self.log.error(error_message)
		
		return config


	def normalize(self, metric, prefix=None):
		"""Turn a metric into a well-formed metric name
		prefix.b.c
		"""
		name = re.sub(r"[,\+\*\-/()\[\]{}]", "_", metric)
		# Eliminate multiple _
		name = re.sub(r"__+", "_", name)
		# Don't start/end with _
		name = re.sub(r"^_", "", name)
		name = re.sub(r"_$", "", name)
		# Drop ._ and _.
		name = re.sub(r"\._", ".", name)
		name = re.sub(r"_\.", ".", name)

		if prefix is not None:
			return prefix + "." + name
		else:
			return name


	def counter(self, name, value):
		name = self.normalize(name)
		
		self.result['counters'][name] = value

	def gauge(self, name, value):
		name = self.normalize(name)

		self.result['gauges'][name] = value


	def version(self, library=None, plugin=None, **kwargs):

		if library:
			self.result['versions']['library'] = library
		if plugin:
			self.result['versions']['plugin'] = plugin

		if kwargs:
			for k,v in kwargs.items():
				self.result['versions'][k] = v

	### UTILS 
	### Used in PostgreSQL, Mysql, Mongo
	def normalize_row_value(self, value):
		if type(value) is Decimal:
			value = round(value, 2)
		elif type(value) is timedelta:
			value = value.total_seconds()
		elif type(value) is datetime:
			value =  str(value)
		elif type(value) is dict:
			to_str = ', '.join("%s=%r" % (key,val) for (key,val) in value.iteritems())
			value = to_str
		if value == None or value is False:
			value = ""
		
		return value
	### UTILS end
	
		
	def collect(self):
		raise NotImplementedError

	def error(self, error_msg):
		self.result['error'] = str(error_msg)


def find_plugin_path(plugin_name=None):

	path = False

	default_location = "{0}/{1}".format(settings.DEFAULT_PLUGINS_PATH, plugin_name)
	custom_location = "{0}/{1}".format(settings.CUSTOM_PLUGINS_PATH, plugin_name)

	if os.path.exists(default_location):
		path = default_location
	elif os.path.exists(custom_location):
		path = custom_location

	return path

def discover_plugins(plugin_paths=[]):
	""" Discover the plugin classes contained in Python files, given a
		list of directory names to scan. Return a list of plugin classes.
		
		For now this method will look only in /etc/amonagent/plugins with possible 
		future extension which will permit searching for plugins in 
		user defined directories
	"""

	if os.path.exists(ENABLED_PLUGINS_PATH):
		# Find all enabled plugins
		for filename in os.listdir(ENABLED_PLUGINS_PATH):
			plugin_name, ext = os.path.splitext(filename)
			if ext == ".conf":
				
				# Configuration file OK, load the plugin				
				plugin_path = find_plugin_path(plugin_name=plugin_name) # path or False

				if plugin_path:
					for filename in os.listdir(plugin_path):
						modname, extension = os.path.splitext(filename)
						if extension == '.py':
							
							fp, path, descr = imp.find_module(modname, [plugin_path])
							if fp:
								# Loading the module registers the plugin in
								if modname not in ['base', '__init__']:
									mod = imp.load_module(modname, fp, path, descr)
								fp.close()
			
	return AmonPlugin.plugins