import argparse

from smartsheetbulkedit.smartsheet.columntype import ColumnType
from smartsheetbulkedit.smartsheet.systemcolumntype import SystemColumnType
from smartsheetbulkedit.smartsheet.symbol import CheckboxSymbol, PicklistSymbol

__ADD_COLUMN_IN_ALL_SHEETS = "addColumnInAllSheets"
__ADD_ROW_IN_ALL_SHEETS = "addRowInAllSheets"
__EXPAND_ALL_ROWS_IN_ALL_SHEETS = "expandAllRowsInAllSheets"
__UPDATE_COLUMN_IN_ALL_SHEETS = "updateColumnInAllSheets"
__UPDATE_CELL_IN_ALL_SHEETS = "updateCellInAllSheets"

argParser = argparse.ArgumentParser(description="Performs bulk operations on Smartsheets.")
__subparsers = argParser.add_subparsers()

__addColumnInAllSheetsParser = __subparsers.add_parser(__ADD_COLUMN_IN_ALL_SHEETS)
__addColumnInAllSheetsParser.add_argument("title", help="column title")
__addColumnInAllSheetsParser.add_argument("--workspace", help="workspace in which to modify all sheets")
__addColumnInAllSheetsParser.add_argument("--type", 
	help="column type", 
	choices=[getattr(ColumnType, var) for var in vars(ColumnType) if not var.startswith("__")])
__addColumnInAllSheetsParser.add_argument("--options", help="options for a picklist type column", type=tuple)
__checkboxSymbols = [getattr(CheckboxSymbol, var) for var in vars(CheckboxSymbol) if not var.startswith("__")]
__addColumnInAllSheetsParser.add_argument("--symbol", 
	help="checkbox {0} or picklist (all other options) symbol set ".format(__checkboxSymbols), 
	choices=(__checkboxSymbols 
		+ [getattr(PicklistSymbol, var) for var in vars(PicklistSymbol) if not var.startswith("__")]))
__addColumnInAllSheetsParser.add_argument("--isPrimary", 
	help="whether this should be the primary column", 
	type=bool, 
	choices=(True, False))
__addColumnInAllSheetsParser.add_argument("--systemColumnType", 
	help="system autopopulated column type", 
	choices=[getattr(SystemColumnType, var) for var in vars(SystemColumnType) if not var.startswith("__")])
__addColumnInAllSheetsParser.add_argument("--autoNumberFormat", 
	metavar="{prefix:PREFIX, suffix:SUFFIX, fill:FILL}", 
	type=dict)
__addColumnInAllSheetsParser.add_argument("--width", help="column width in pixels", type=int)

__addRowInAllSheetsParser = __subparsers.add_parser(__ADD_ROW_IN_ALL_SHEETS)

__expandAllRowsInAllSheetsParser = __subparsers.add_parser(__EXPAND_ALL_ROWS_IN_ALL_SHEETS)

__updateColumnInAllSheetsParser = __subparsers.add_parser(__UPDATE_COLUMN_IN_ALL_SHEETS)

__updateCellInAllSheetsParser = __subparsers.add_parser(__UPDATE_CELL_IN_ALL_SHEETS)