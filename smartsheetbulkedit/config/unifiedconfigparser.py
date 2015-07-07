from logconfigparser import LogConfigParser
from smartsheetconfigparser import SmartsheetConfigParser

class UnifiedConfigParser(SmartsheetConfigParser, LogConfigParser):
	""" Unified ConfigParser for smartsheetservice - 
	fully understands the all configuration file sections and options
	"""

	__DEFAULT_CONFIG_FILE = "smartsheetbulkedit.cfg"

	def read(self, filenames=__DEFAULT_CONFIG_FILE):
		""" Reads the configuration file. 

		:param filenames: the configuration files to read.
		"""
		return SmartsheetConfigParser.read(self, filenames)
