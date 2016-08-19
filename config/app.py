"""This module defines classes to retrieve the rest app configuration."""
import os


class Config(object):
    """Serves the application configuration."""

    def __init__(self):
        """Initilize the config.

        Retrieves the configuration from a settings.py file in the running
        directory and serves for the application.
        """
        dirname, _ = os.path.split(os.path.abspath(__file__))
        self.settings_file = os.path.join(dirname, 'settings.py')
