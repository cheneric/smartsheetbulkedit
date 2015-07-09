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
#	smartsheetService.addRowInAllSheets({"*Task Name":"my task name3", "*Data or Comment":"foobar", "*Date":now, "*Status":"Not Started"}, workspace="ERIC CHEN - API SANDBOX", rowNumber=0)

#	from smartsheetbulkedit import ColumnTypes
#	smartsheetService.addColumnInAllSheets("foo title3", type=ColumnTypes.Date, index=0)
#	smartsheetService.updateColumnInAllSheets("yello belly", workspace="ERIC CHEN - API SANDBOX", type=ColumnTypes.PickList, options=("one", "two", "three"))

	smartsheetService.updateCellInAllSheets(2, columnIndex=7, columnTitle="*Task Name", value="pewter dragon")