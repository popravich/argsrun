import unittest
import argparse
from unittest import mock

from argsrun import Entry


class TestEntry(unittest.TestCase):

    def dummy_handler(self, opts):
        self.assertIsInstance(opts, argparse.Namespace)

    def handler_with_docstring(self, opts):
        """Short docstring."""
        pass

    def handler_long_docstring(self, opts):
        """Line 1.

        Extra line 1.
        Extra line 2.
        """

    def test_simple(self):
        entry = Entry(self.dummy_handler)
        self.assertEqual(entry.handler, self.dummy_handler)
        self.assertIsNone(entry.argparser_setup)
        self.assertIsNone(entry.short_help)
        self.assertIsNone(entry.description)
        self.assertTrue(callable(entry))

        entry(['script'])

        with self.assertRaisesRegex(ValueError,
                                    "need more than 0 values to unpack"):
            entry([])

    def test_argparse_setup(self):
        ap_mock_inst = mock.MagicMock()
        ap_mock_inst.parse_args.return_value = ns = object()

        ap_mock = mock.MagicMock()
        ap_mock.return_value = ap_mock_inst

        handler = mock.MagicMock(__doc__=None)

        setup = mock.MagicMock()

        with mock.patch('argparse.ArgumentParser', ap_mock):
            Entry(handler, setup)(['script'])

        ap_mock.assert_called_once_with(description=None)
        setup.assert_called_once_with(ap_mock_inst)
        ap_mock_inst.parse_args.assert_called_once_with([])
        handler.assert_called_once_with(ns)

    def test_docstring(self):
        entry = Entry(self.handler_with_docstring)
        self.assertEqual(entry.handler, self.handler_with_docstring)
        self.assertIsNone(entry.argparser_setup)
        self.assertEqual(entry.short_help, "Short docstring.")
        self.assertEqual(entry.description, "Short docstring.")

        entry = Entry(self.handler_long_docstring)
        self.assertEqual(entry.handler, self.handler_long_docstring)
        self.assertIsNone(entry.argparser_setup)
        self.assertEqual(entry.short_help, "Line 1.")
        self.assertEqual(entry.description, ("Line 1.\n\n" + " " * 8 +
                                             "Extra line 1.\n" + " " * 8 +
                                             "Extra line 2.\n" + " " * 8))

    def test_short_help(self):
        entry = Entry(self.dummy_handler, short_help="Short help")
        self.assertEqual(entry.handler, self.dummy_handler)
        self.assertIsNone(entry.argparser_setup)
        self.assertEqual(entry.short_help, "Short help")
        self.assertIsNone(entry.description)

        entry = Entry(self.handler_with_docstring, short_help="Short help")
        self.assertEqual(entry.handler, self.handler_with_docstring)
        self.assertIsNone(entry.argparser_setup)
        self.assertEqual(entry.short_help, "Short help")
        self.assertEqual(entry.description, "Short docstring.")

    def test_description(self):
        entry = Entry(self.dummy_handler, description="Description")
        self.assertEqual(entry.handler, self.dummy_handler)
        self.assertIsNone(entry.argparser_setup)
        self.assertIsNone(entry.short_help)
        self.assertEqual(entry.description, "Description")

        entry = Entry(self.handler_with_docstring, description="Description")
        self.assertEqual(entry.handler, self.handler_with_docstring)
        self.assertIsNone(entry.argparser_setup)
        self.assertEqual(entry.short_help, "Short docstring.")
        self.assertEqual(entry.description, "Description")

    def test_assertions(self):
        with self.assertRaises(AssertionError):
            Entry(None)
        with self.assertRaises(AssertionError):
            Entry(self.dummy_handler, object())
        with self.assertRaises(AssertionError):
            Entry(self.dummy_handler, short_help=['Short', 'help'])
        with self.assertRaises(AssertionError):
            Entry(self.dummy_handler, description=['Short', 'help'])
