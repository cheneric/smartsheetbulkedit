import logging

from smartsheetclient import Column
from smartsheetclient import RowPositionProperties
from smartsheetclient import SmartsheetClient

from smartsheetbulkedit import SmartsheetBulkEditError

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

	def addColumnInAllSheets(self, title, workspace=None, index=None, type=None, options=None, symbol=None, isPrimary=None, systemColumnType=None, autoNumberFormat=None, width=None):
		for sheetInfo in self.getSheetInfos(workspace):
			sheet = self.__getSheetIfInWorkspace(sheetInfo, workspace)
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

	def updateCell(self, sheet, rowNumber, columnIndex=None, columnTitle=None, value=None):
		if columnIndex is not None and columnTitle is not None:
			raise SmartsheetBulkEditError('one but not both "columnIndex" and "columnTitle" must be specified')
		elif columnTitle is not None:
			columnIndex = sheet.getColumnsInfo().getColumnByTitle(columnTitle).index
		elif columnIndex is None:
			raise SmartsheetBulkEditError('either "columnIndex" or "columnTitle" must be specified')
		row = sheet[rowNumber]
		row[columnIndex] = value
		row.getCellByIndex(columnIndex).save(propagate=False)

	def updateCellInAllSheets(self, rowNumber, workspace=None, columnIndex=None, columnTitle=None, value=None):
		for sheetInfo in self.getSheetInfos(workspace):
			sheet = self.__getSheetIfInWorkspace(sheetInfo, workspace)
			if sheet is not None:
				self.updateCell(sheet, rowNumber, columnIndex=columnIndex, columnTitle=columnTitle, value=value)

			# temp
			break

	def updateColumn(self, sheet, oldTitle, newTitle=None, index=None, type=None, options=None, symbol=None, systemColumnType=None, autoNumberFormat=None, width=None, format=None):
		column = sheet.getColumnsInfo().getColumnByTitle(oldTitle)
		if newTitle is not None:
			column.title = newTitle
		if index is not None:
			column.index = index
		if type is not None:
			column.type = type
		if options is not None:
			column.options = options
		if symbol is not None:
			column.symbol = symbol
		if systemColumnType is not None:
			column.systemColumnType = systemColumnType
		if autoNumberFormat is not None:
			column.autoNumberFormat = autoNumberFormat
		if width is not None:
			column.width = width
		if format is not None:
			column.format = format
		column.update()

	def updateColumnInAllSheets(self, oldTitle, workspace=None, newTitle=None, index=None, type=None, options=None, symbol=None, systemColumnType=None, autoNumberFormat=None, width=None, format=None):
		for sheetInfo in self.getSheetInfos(workspace):
			sheet = self.__getSheetIfInWorkspace(sheetInfo, workspace)
			if sheet is not None:
				self.updateColumn(
					sheet, 
					oldTitle, 
					newTitle=newTitle, 
					index=index, 
					type=type, 
					options=options, 
					symbol=symbol, 
					systemColumnType=systemColumnType, 
					autoNumberFormat=autoNumberFormat, 
					width=width, 
					format=format)

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

	def addRowInAllSheets(self, rowDictionary, workspace=None, rowNumber=None):
		for sheetInfo in self.getSheetInfos(workspace):
			sheet = self.__getSheetIfInWorkspace(sheetInfo, workspace)
			if sheet is not None:
				self.addRow(sheet, rowDictionary, rowNumber)

			# temp
			break

	def expandAllRows(self, sheet, isExpanded=True):
		# operate only on rows referenced to be parent rows
		parentRowNumbers = frozenset([row.parentRowNumber for row in sheet.rows if row.parentRowNumber])
		for parentRowNumber in parentRowNumbers:
			row = sheet[parentRowNumber]
			if row.expanded != isExpanded:
				row.expanded = isExpanded
				row.save()

	def expandAllRowsInAllSheets(self, workspace=None, isExpanded=True):
		for sheetInfo in self.getSheetInfos(workspace):
			sheet = self.__getSheetIfInWorkspace(sheetInfo, workspace)
			if sheet is not None:
				self.expandAllRows(sheet, isExpanded)

			# temp
			break

	def getSheetInfos(self, workspace=None):
		# Smartsheet Python SDK cannot filter by workspace
		return self.__smartsheetClient.fetchSheetList()

	def __getSheetIfInWorkspace(self, sheetInfo, workspace):
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

