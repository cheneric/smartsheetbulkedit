import logging

from smartsheetclient import Column
from smartsheetclient import RowPositionProperties
from smartsheetclient import SmartsheetClient

class SmartsheetService(object):
	__logger = logging.getLogger(__name__)

	def __init__(self, token):
		self.__smartsheetClient = SmartsheetClient(token, logger=logging.getLogger(SmartsheetClient.__name__))
		self.__smartsheetClient.connect()

	def addColumn(self, sheet, title, index=None, type=None, options=None, symbol=None, isPrimary=None, systemColumnType=None, autoNumberFormat=None, width=None):
		params = {}
		if sheet is not None:
			params["sheet"] = sheet
		if index is not None:
			params["index"] = index
		if type is not None:
			params["type"] = type
		if options is not None:
			params["options"] = options
		if symbol is not None:
			params["symbol"] = symbol
		if isPrimary is not None:
			params["primary"] = isPrimary
		if systemColumnType is not None:
			params["systemColumnType"] = systemColumnType
		if autoNumberFormat is not None:
			params["autoNumberFormat"] = autoNumberFormat
		column = Column(title, **params)
		sheet.insertColumn(column, column.index)

	def addColumnToAllSheets(self, title, workspace=None, index=None, type=None, options=None, symbol=None, isPrimary=None, systemColumnType=None, autoNumberFormat=None, width=None):
		for sheetInfo in self.getSheetInfos(workspace):
			sheet = self.__getSheetInWorkspace(sheetInfo, workspace)
			if sheet is not None:
				self.addColumn(
					sheet, 
					title, 
					index=index, 
					type=type, 
					options=options, 
					symbol=symbol, 
					isPrimary=isPrimary, 
					systemColumnType=systemColumnType, 
					autoNumberFormat=autoNumberFormat, 
					width=width)

			# temp
			break

	def addRow(self, sheet, rowDictionary, rowNumber=None):
		row = sheet.makeRow(**rowDictionary)
		if rowNumber is None:
			# add as last row
			sheet.addRow(row)
		elif rowNumber == 0:
			# add as first row
			sheet.addRow(row, position=RowPositionProperties.Top)
		else:
			# new row is inserted below sibling, so get the row ID of the sibling above
			siblingId = sheet.getRowByRowNumber(rowNumber - 1)
			sheet.addRow(row, siblingId=siblingId)

	def addRowToAllSheets(self, rowDictionary, workspace=None, rowNumber=None):
		for sheetInfo in self.getSheetInfos(workspace):
			sheet = self.__getSheetInWorkspace(sheetInfo, workspace)
			if sheet is not None:
				self.addRow(sheetInfo.loadSheet(), rowDictionary, rowNumber)

			# temp
			break

	def getSheetInfos(self, workspace=None):
		# Smartsheet Python SDK cannot filter by workspace
		return self.__smartsheetClient.fetchSheetList()

	def __getSheetInWorkspace(self, sheetInfo, workspace):
		""" Returns a Sheet if it belongs to the specified workspace
		or if workspace == None.  Returns None if the sheet does not 
		belong to the workspace.

		:param sheetInfo: the SheetInfo for the desired sheet
		:param workspace: the desired workspace name, or None to 
		disable workspace checking and always return the associated Sheet.
		"""
		sheet = sheetInfo.loadSheet()
		sheetWorkspace = sheet.workspace["name"]
		isSheetInWorkspace = not workspace or sheetWorkspace == workspace
		if (not isSheetInWorkspace):
			self.__logger.debug('sheet %s workspace "%s" != "%s"' % (sheetInfo, sheetWorkspace, workspace))
		return sheet
