from absentsaferawconfigparser import AbsentSafeRawConfigParser

class SmartsheetConfigParser(AbsentSafeRawConfigParser):
	""" ConfigParser for "smartsheet" section of configuration file. """

	__SMARTSHEET_CONFIG_SECTION = "smartsheet"
	__SMARTSHEET_TOKEN_KEY = "token"

	def getSmartsheetToken(self):
		""" Returns the Smartsheet authorization token. """
		return SmartsheetConfigParser.absentSafeGet(self, 
			SmartsheetConfigParser.__SMARTSHEET_CONFIG_SECTION, 
			SmartsheetConfigParser.__SMARTSHEET_TOKEN_KEY)
