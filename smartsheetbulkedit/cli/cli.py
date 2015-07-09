import argparse
from argparse import ArgumentTypeError
import json

from smartsheetbulkedit.smartsheet.columntype import ColumnType
from smartsheetbulkedit.smartsheet.smartsheetservice import SmartsheetService
from smartsheetbulkedit.smartsheet.systemcolumntype import SystemColumnType
from smartsheetbulkedit.smartsheet.symbol import CheckboxSymbol, PicklistSymbol

class Cli:
	__COMMAND_KEY = "command"
	__ADD_COLUMN_IN_ALL_SHEETS = "addColumnInAllSheets"
	__ADD_ROW_IN_ALL_SHEETS = "addRowInAllSheets"
	__EXPAND_ALL_ROWS_IN_ALL_SHEETS = "expandAllRowsInAllSheets"
	__COLLAPSE_ALL_ROWS_IN_ALL_SHEETS = "collapseAllRowsInAllSheets"
	__UPDATE_COLUMN_IN_ALL_SHEETS = "updateColumnInAllSheets"
	__UPDATE_CELL_IN_ALL_SHEETS = "updateCellInAllSheets"

	def __init__(self, smartsheetToken):
		self.__smartsheetToken = smartsheetToken
		self.__argParser = argparse.ArgumentParser(description="Performs bulk operations on Smartsheets.")
		subparsers = self.__argParser.add_subparsers(dest=Cli.__COMMAND_KEY)

		allColumnTypes = [getattr(ColumnType, var) for var in vars(ColumnType) if not var.startswith("__")]
		checkboxSymbols = [getattr(CheckboxSymbol, var) for var in vars(CheckboxSymbol) if not var.startswith("__")]
		allSymbols = checkboxSymbols + [getattr(PicklistSymbol, var) for var in vars(PicklistSymbol) if not var.startswith("__")]
		allSystemColumnTypes = [getattr(SystemColumnType, var) for var in vars(SystemColumnType) if not var.startswith("__")]

		addColumnInAllSheetsParser = subparsers.add_parser(Cli.__ADD_COLUMN_IN_ALL_SHEETS)
		addColumnInAllSheetsParser.add_argument("title", help="column title")
		addColumnInAllSheetsParser.add_argument("--workspace", help="workspace in which to modify all sheets")
		addColumnInAllSheetsParser.add_argument("--index", help="column index", type=int)
		addColumnInAllSheetsParser.add_argument("--type", help="column type", choices=allColumnTypes)
		addColumnInAllSheetsParser.add_argument("--options", help="space-separated options for picklist-type column", nargs="*")
		addColumnInAllSheetsParser.add_argument("--symbol", 
			help="checkbox {0} or picklist (all other options) symbol set ".format(checkboxSymbols), 
			choices=allSymbols)
		addColumnInAllSheetsParser.add_argument("--isPrimary", help="whether this should be the primary column", type=parseBoolean, choices=(True, False))
		addColumnInAllSheetsParser.add_argument("--systemColumnType", help="system autopopulated column type", choices=allSystemColumnTypes)
		addColumnInAllSheetsParser.add_argument("--autoNumberFormat", metavar="{prefix:PREFIX, suffix:SUFFIX, fill:FILL}", type=json.loads)
		addColumnInAllSheetsParser.add_argument("--width", help="column width in pixels", type=int)
		addColumnInAllSheetsParser.set_defaults(func=self.__addColumnInAllSheets)

		addRowInAllSheetsParser = subparsers.add_parser(Cli.__ADD_ROW_IN_ALL_SHEETS)
		addRowInAllSheetsParser.add_argument("rowData", help="row data as a dict of {column name: value} pairs", type=json.loads)
		addRowInAllSheetsParser.add_argument("--workspace", help="workspace in which to modify all sheets")
		addRowInAllSheetsParser.add_argument("--rowNumber", help="1-based row number of the new row", type=int)
		addRowInAllSheetsParser.set_defaults(func=self.__addRowInAllSheets)

		expandAllRowsInAllSheetsParser = subparsers.add_parser(Cli.__EXPAND_ALL_ROWS_IN_ALL_SHEETS)
		expandAllRowsInAllSheetsParser.add_argument("--workspace", help="workspace in which to modify all sheets")
		expandAllRowsInAllSheetsParser.set_defaults(func=self.__expandOrCollapseAllRowsInAllSheets)

		collapseAllRowsInAllSheetsParser = subparsers.add_parser(Cli.__COLLAPSE_ALL_ROWS_IN_ALL_SHEETS)
		collapseAllRowsInAllSheetsParser.add_argument("--workspace", help="workspace in which to modify all sheets")
		collapseAllRowsInAllSheetsParser.set_defaults(func=self.__expandOrCollapseAllRowsInAllSheets)

		updateColumnInAllSheetsParser = subparsers.add_parser(Cli.__UPDATE_COLUMN_IN_ALL_SHEETS)
		updateColumnInAllSheetsParser.add_argument("oldTitle", help="current column title")
		updateColumnInAllSheetsParser.add_argument("--workspace", help="workspace in which to modify all sheets")
		updateColumnInAllSheetsParser.add_argument("--newTitle", help="new column title")
		updateColumnInAllSheetsParser.add_argument("--index", help="new column index", type=int)
		updateColumnInAllSheetsParser.add_argument("--type", help="new column type", choices=allColumnTypes)
		updateColumnInAllSheetsParser.add_argument("--options", help="new space-separated options for picklist-type column", nargs="*")
		updateColumnInAllSheetsParser.add_argument("--symbol", 
			help="new checkbox {0} or picklist (all other options) symbol set ".format(checkboxSymbols), 
			choices=allSymbols)
		updateColumnInAllSheetsParser.add_argument("--systemColumnType", help="new system autopopulated column type", choices=allSystemColumnTypes)
		updateColumnInAllSheetsParser.add_argument("--autoNumberFormat", metavar="{prefix:PREFIX, suffix:SUFFIX, fill:FILL}", type=json.loads)
		updateColumnInAllSheetsParser.add_argument("--width", help="new column width in pixels", type=int)
		updateColumnInAllSheetsParser.add_argument("--format", help="new column format")
		updateColumnInAllSheetsParser.set_defaults(func=self.__updateColumnInAllSheets)

		updateCellInAllSheetsParser = subparsers.add_parser(Cli.__UPDATE_CELL_IN_ALL_SHEETS)
		updateCellInAllSheetsParser.add_argument("rowNumber", help="1-based row number of the cell to update", type=int)
		updateCellInAllSheetsParser.add_argument("--workspace", help="workspace in which to modify all sheets")
		updateCellInAllsSheetsColumnGroup = updateCellInAllSheetsParser.add_mutually_exclusive_group(required=True)
		updateCellInAllsSheetsColumnGroup.add_argument("--columnIndex", 
			help='0-based column index of the cell to update', 
			type=int)
		updateCellInAllsSheetsColumnGroup.add_argument("--columnTitle", 
			help='current column title of the cell to update')
		updateCellInAllsSheetsValueGroup = updateCellInAllSheetsParser.add_mutually_exclusive_group()
		updateCellInAllsSheetsValueGroup.add_argument("--value", help="new cell value (string or date)")
		updateCellInAllsSheetsValueGroup.add_argument("--valueInt", help="new cell value (int)", type=int)
		updateCellInAllSheetsParser.set_defaults(func=self.__updateCellInAllSheets)


	def execute(self):
		args = self.__argParser.parse_args()
		args.func(args)

	def __addColumnInAllSheets(self, args):
		self.__getSmartsheetService().addColumnInAllSheets(
			args.title, 
			workspace=args.workspace, 
			index=args.index,
			type=args.type,
			options=args.options,
			symbol=args.symbol,
			isPrimary=args.isPrimary, 
			systemColumnType=args.systemColumnType, 
			autoNumberFormat=args.autoNumberFormat, 
			width=args.width)

	def __addRowInAllSheets(self, args):
		self.__getSmartsheetService().addRowInAllSheets(
			args.rowData,
			workspace=args.workspace,
			rowNumber=args.rowNumber)

	def __expandOrCollapseAllRowsInAllSheets(self, args):
		self.__getSmartsheetService().expandAllRowsInAllSheets(
			workspace=args.workspace,
			isExpanded=(getattr(args, Cli.__COMMAND_KEY) == Cli.__EXPAND_ALL_ROWS_IN_ALL_SHEETS))

	def __updateColumnInAllSheets(self, args):
		self.__getSmartsheetService().updateColumnInAllSheets(
			args.oldTitle, 
			workspace=args.workspace, 
			newTitle=args.newTitle, 
			index=args.index, 
			type=args.type, 
			options=args.options, 
			symbol=args.symbol, 
			systemColumnType=args.systemColumnType, 
			autoNumberFormat=args.autoNumberFormat, 
			width=args.width, 
			format=args.format)

	def __updateCellInAllSheets(self, args):
		self.__getSmartsheetService().updateCellInAllSheets(
			args.rowNumber, 
			workspace=args.workspace, 
			columnIndex=args.columnIndex, 
			columnTitle=args.columnTitle, 
			value=args.value or args.valueInt)

	def __getSmartsheetService(self):
		return SmartsheetService(self.__smartsheetToken)

def parseBoolean(value):
	booleanValue = None
	if (value is not None):
		lowerValue = value.lower()
		if lowerValue in ("true", "t", "yes", "y"):
			booleanValue = True
		elif lowerValue in ("false", "f", "no", "n"):
			booleanValue = False
		else:
			raise ArgumentTypeError("invalid boolean value: {0}".format(value))
	return booleanValue
