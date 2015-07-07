""" Log configuration. """

import logging
from logging import StreamHandler
from logging.handlers import TimedRotatingFileHandler

from smartsheetbulkedit.config.logconfigparser import LogConfigParser
from smartsheetbulkedit.os import fileutils

def config(config=None):
	"""Configures the root logger from a parsed configuration.

	:param config: a LogConfigParser
	"""
	if config:
		DEFAULT_LOG_LEVEL = logging.DEBUG

		logger = logging.getLogger()

		# log file (with daily rotation)
		handler = None
		logFile = config.getLogFile()
		if logFile:
			try:
				fileutils.ensureDirectories(logFile)
				handler = TimedRotatingFileHandler(logFile, when="midnight")
			except Exception as exception:
				print "WARNING unable to initialize log file %s: %s" % (logFile, exception)
		if not handler:
			handler = StreamHandler()
		logger.addHandler(handler)

		# log message format
		logFormat = config.getLogFormat()
		if logFormat:
			if "%(message)s" in logFormat:
				handler.setFormatter(logging.Formatter(logFormat))
			else:
				print 'WARNING ignoring log format string without "%%(message)s": %s' % logFormat

		# log level
		logLevelName = config.getLogLevel()
		if logLevelName:
			try:
				logLevel = getattr(logging, logLevelName)
			except AttributeError:
				logLevel = DEFAULT_LOG_LEVEL
				print "WARNING unknown log level %s - using default %s" % (logLevelName, logLevel)
		logger.setLevel(logLevel)
	else:
		# console logging
		logging.basicConfig(format="%(asctime)s\t%(levelname)s\t%(name)s\t%(message)s", level=DEFAULT_LOG_LEVEL)
