# smartsheetbulkedit

## Version history

1.0.0

* initial revision
* supports the following commands via command-line interface:
	* addColumnInAllSheets
	* addRowInAllSheets
	* expandAllRowsInAllSheets
	* collapseAllRowsInAllSheets
	* updateColumnInAllSheets
	* updateCellInAllSheets

## Using smartsheetbulkedit

0. After [intalling prerequisites](#install-prerequisites), run the smartsheetbulkedit help command:

	```
python smartsheetbulkedit.py -h
	```

	This will list the available subcommands.

0. Choose any subcommand and get help for that subcommand - for example:

	```
python smartsheetbulkedit.py addRowInAllSheets -h
	```

	This will tell you the required and optional parameters for the command.

## Installation

### Requirements

* Python 2.7.6
* pip
* [virtualenv](http://docs.python-guide.org/en/latest/dev/virtualenvs/)
* [Smartsheet Python SDK](https://github.com/smartsheet-platform/smartsheet-python-sdk)
* [Smartsheet API access token](https://www.smartsheet.com/developers/api-documentation#h.5osh0dl59e5m)

### Install prerequisites

0. Create and `cd` into a directory for this project:

	```
mkdir myproject
cd myproject
	```

0. Create a virtual environment for this project:

	```
virtualenv venv
	```

0. Activate the newly created virtual environment:

	```
source venv/bin/activate
	```

0. Install the Smartsheet Python SDK:

	```
pip install git+git://github.com/smartsheet-platform/smartsheet-python-sdk.git
	```

0. Insert your Smartsheet API access token in place of the placeholder in `smartsheetbulkedit/smartsheetbulkedit.cfg`:

	```
token=REPLACE_WITH_YOUR_SMARTSHEET_TOKEN
	```

0. That's it!

