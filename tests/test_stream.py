from unittest import TestCase

from parser import End, Invalid, Stream


class StreamTests(TestCase):
    def test_get(self):
        s = Stream('0123')

        self.assertEqual(s.get(), '0')
        self.assertEqual(s.get(), '1')
        self.assertEqual(s.get(), '2')
        self.assertEqual(s.get(), '3')
        self.assertEqual(s.get(), None)

    def test_context_manager_valid(self):
        s = Stream('012345')

        with s as ss:
            with ss as sss:
                self.assertEqual(sss.get(), '0')
                self.assertEqual(sss.get(), '1')
            self.assertEqual(sss.get(), '2')
            self.assertEqual(sss.get(), '3')
        self.assertEqual(sss.get(), '4')
        self.assertEqual(sss.get(), '5')
        self.assertEqual(sss.get(), None)

    def test_context_manager_invalid(self):
        s = Stream('012345')

        self.assertEqual(s.get(), '0')
        self.assertEqual(s.get(), '1')
        with self.assertRaises(Invalid):
            with s as ss:
                self.assertEqual(ss.get(), '2')
                self.assertEqual(ss.get(), '3')
                with self.assertRaises(Invalid):
                    with ss as sss:
                        self.assertEqual(sss.get(), '4')
                        self.assertEqual(sss.get(), '5')
                        raise Invalid()
                with self.assertRaises(Invalid):
                    with ss as sss:
                        self.assertEqual(sss.get(), '4')
                        self.assertEqual(sss.get(), '5')
                        raise Invalid()
                self.assertEqual(ss.get(), '4')
                self.assertEqual(ss.get(), '5')
                raise Invalid()
        with self.assertRaises(Invalid):
            with s as ss:
                self.assertEqual(ss.get(), '2')
                self.assertEqual(ss.get(), '3')
                with self.assertRaises(Invalid):
                    with ss as sss:
                        self.assertEqual(sss.get(), '4')
                        self.assertEqual(sss.get(), '5')
                        raise Invalid()
                with self.assertRaises(Invalid):
                    with ss as sss:
                        self.assertEqual(sss.get(), '4')
                        self.assertEqual(sss.get(), '5')
                        raise Invalid()
                self.assertEqual(ss.get(), '4')
                self.assertEqual(ss.get(), '5')
                raise Invalid()
        self.assertEqual(s.get(), '2')
        self.assertEqual(s.get(), '3')
