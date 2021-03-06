# coding=utf-8
try:
    from unittest.mock import patch
except ImportError:
    from mock import patch

from django.core.exceptions import ValidationError
from django.test import TestCase

from stdnumfield.forms import StdnumField


VALID_OIB = '69435151530'
INVALID_OIB = '69435151531'


class FormFieldInitTest(TestCase):

    def test_single_format(self):
        try:
            StdnumField(formats='hr.oib')
        except Exception as e:
            self.assertIsNone(e)

    def test_multiple_formats(self):
        try:
            StdnumField(formats=['hr.oib', 'damm'])
        except Exception as e:
            self.assertIsNone(e)

    def test_invalid_single_formats(self):
        self.assertRaisesMessage(
            ValueError,
            'Unknown format for StdnumField',
            StdnumField,
            formats='damn',
        )

    def test_invalid_in_list_formats(self):
        self.assertRaisesMessage(
            ValueError,
            'Unknown format for StdnumField',
            StdnumField,
            formats=['damm', 'damn'],
        )

    def test_no_formats(self):
        self.assertRaisesMessage(
            ValueError,
            'StdnumField defined without formats',
            StdnumField,
        )

    def test_alphabet_list_wrong_len(self):
        self.assertRaisesMessage(
            ValueError,
            'StdnumField got alphabets and formats of different length',
            StdnumField,
            formats=['damm', 'oib'],
            alphabets=['12345'],
        )

    def test_error_message_override(self):
        field = StdnumField(
            formats='cz.dic',
            error_messages={'stdnum_format': 'test_exception'},
        )

        self.assertRaisesRegexp(
            ValidationError,
            'test_exception',
            field.clean,
            '01234',
        )


class FormFieldValidateTest(TestCase):
    formats = ['hr.oib']

    @patch('stdnumfield.forms.StdnumFormatValidator')
    def test_validate(self, validator_class):
        field = StdnumField(formats=self.formats)
        field.run_validators(VALID_OIB)
        validator_class.assert_called_once_with(self.formats, None)
        validator_instance = validator_class.return_value
        validator_instance.assert_called_once_with(VALID_OIB)
