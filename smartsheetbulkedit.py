if __name__ == "__main__":
	from smartsheetbulkedit.cli.cli import Cli
	from smartsheetbulkedit.config.unifiedconfigparser import UnifiedConfigParser
	from smartsheetbulkedit.log import logconfig

	# read configuration
	config = UnifiedConfigParser()
	config.read()

	# configure logging
	logconfig.config(config)

	# execute command line
	Cli(config.getSmartsheetToken()).execute()