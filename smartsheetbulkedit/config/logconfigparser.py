from absentsaferawconfigparser import AbsentSafeRawConfigParser

class LogConfigParser(AbsentSafeRawConfigParser):
	""" ConfigParser for "log" section of configuration file. """

	__LOG_CONFIG_SECTION = "log"
	__LOG_FILE_KEY = "file"
	__LOG_FORMAT_KEY = "format"
	__LOG_LEVEL_KEY = "level"

	def getLogFile(self):
		""" Returns the log file path. """
		return AbsentSafeRawConfigParser.absentSafeGet(self, 
			LogConfigParser.__LOG_CONFIG_SECTION, 
			LogConfigParser.__LOG_FILE_KEY)

	def getLogFormat(self):
		""" Returns the log record format. """
		return AbsentSafeRawConfigParser.absentSafeGet(self, 
			LogConfigParser.__LOG_CONFIG_SECTION, 
			LogConfigParser.__LOG_FORMAT_KEY)

	def getLogLevel(self):
		""" Returns the minimum logging level. """
		return AbsentSafeRawConfigParser.absentSafeGet(self, 
			LogConfigParser.__LOG_CONFIG_SECTION, 
			LogConfigParser.__LOG_LEVEL_KEY)
