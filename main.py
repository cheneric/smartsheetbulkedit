if __name__ == "__main__":
	import ConfigParser
	import logging

	from smartsheetbulkedit.config.unifiedconfigparser import UnifiedConfigParser
	from smartsheetbulkedit.log import logconfig
	from smartsheetbulkedit.smartsheet.smartsheetservice import SmartsheetService

	# read configuration
	config = UnifiedConfigParser()
	config.read()

	# configure logging
	logconfig.config(config)
	logger = logging.getLogger(__name__)

	smartsheetService = SmartsheetService(config.getSmartsheetToken())

#	from datetime import datetime
#	now = datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f")
#	smartsheetService.addRowToAllSheets({"*Task Name":"my task name3", "*Data or Comment":"foobar", "*Date":now, "*Status":"Not Started"}, workspace="ERIC CHEN - API SANDBOX", rowNumber=0)

	from smartsheetbulkedit import ColumnTypes
	smartsheetService.addColumnToAllSheets("foo title2", type=ColumnTypes.Date, index=0)

