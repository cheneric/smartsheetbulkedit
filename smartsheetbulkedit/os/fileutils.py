""" File utilities. """

import errno
import os

DEFAULT_DIRECTORY_PERMISSIONS = 0755

def ensureDirectories(path, mode=DEFAULT_DIRECTORY_PERMISSIONS):
	"""Ensures the existence of or creates the directories in the input path.
	The input path may optionally end with a file name which is ignored.

	:param path: the path whose directories to ensure or create.
	:param mode: the unix permissions of created directories.
	"""
	parentPath = os.path.dirname(path)
	makeDirectories(parentPath)

def makeDirectories(path, mode=DEFAULT_DIRECTORY_PERMISSIONS):
	"""Ensures the existence of or creates the directories in the input path.
	All path elements are interpreted as directories

	:param path: the directories to ensure or create.
	:param mode: the unix permissions of the created directories.
	"""
	try:
		os.makedirs(path, mode)
	except OSError as exception:
		if exception.errno != errno.EEXIST or not os.path.isdir(path):
			raise