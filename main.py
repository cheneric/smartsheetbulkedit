if __name__ == "__main__":
	import ConfigParser
	import logging

	from smartsheetbulkedit.config.unifiedconfigparser import UnifiedConfigParser
	from smartsheetbulkedit.log import logconfig

	from smartsheetclient import SmartsheetClient

	# read configuration
	config = UnifiedConfigParser()
	config.read()

	# configure logging
	logconfig.config(config)
	logger = logging.getLogger(__name__)

	smartsheetToken = config.getSmartsheetToken()
	smartsheetClient = SmartsheetClient(smartsheetToken, logger=logging.getLogger(SmartsheetClient.__name__))
	smartsheetClient.connect()
	sheets = smartsheetClient.fetchSheetList()
