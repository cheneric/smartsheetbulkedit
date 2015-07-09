from smartsheetclient import CellTypes

class ColumnType:
	""" Valid Smartsheet column types """
	checkbox = CellTypes.Checkbox
	contactList = CellTypes.ContactList
	date = CellTypes.Date
	picklist = CellTypes.Picklist
	textNumber = CellTypes.TextNumber