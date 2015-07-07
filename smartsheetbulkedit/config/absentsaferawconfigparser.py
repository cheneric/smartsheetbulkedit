from ConfigParser import RawConfigParser

class AbsentSafeRawConfigParser(RawConfigParser):
	""" RawConfigParser that returns None for missing sections and options 
	rather than throwing NoSectionError or NoOtionError. """

	def absentSafeGet(self, section, option):
		""" Returns the string value of the input section and option, 
		or None if either does not exist. """
		return (RawConfigParser.get(self, section, option)
			if RawConfigParser.has_option(self, section, option)
			else None)
