from unittest import TestCase

from parser import End, Invalid, Stream


class StreamTests(TestCase):
    def test_get(self):
        s1 = Stream('0123')
        s2 = Stream()
        s2.q = list('0123')

        for s in (s1, s2):
            self.assertEqual(s.get(), '0')
            self.assertEqual(s.get(), '1')
            self.assertEqual(s.get(), '2')
            self.assertEqual(s.get(), '3')
            self.assertEqual(s.get(), None)

    def test_context_manager_valid(self):
        s1 = Stream('012345')
        s2 = Stream()
        s2.q = list('012345')

        for s in (s1, s2):
            with s as ss:
                with ss as sss:
                    self.assertEqual(sss.get(), '0')
                    self.assertEqual(sss.get(), '1')
                self.assertEqual(ss.get(), '2')
                self.assertEqual(ss.get(), '3')
            self.assertEqual(s.get(), '4')
            self.assertEqual(s.get(), '5')
            self.assertEqual(s.get(), None)

    def test_context_manager_invalid(self):
        s1 = Stream('01234567')
        s2 = Stream()
        s2.q = list('01234567')

        for s in (s1, s2):
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

    def test_context_manager_mixed(self):
        s1 = Stream('0123456789')
        s2 = Stream()
        s2.q = list('0123456789')

        for s in (s1, s2):
            self.assertEqual(s.get(), '0')
            self.assertEqual(s.get(), '1')
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
            with s as ss:
                self.assertEqual(ss.get(), '4')
                self.assertEqual(ss.get(), '5')
                with self.assertRaises(Invalid):
                    with ss as sss:
                        self.assertEqual(sss.get(), '6')
                        self.assertEqual(sss.get(), '7')
                        raise Invalid()
                with self.assertRaises(Invalid):
                    with ss as sss:
                        self.assertEqual(sss.get(), '6')
                        self.assertEqual(sss.get(), '7')
                        raise Invalid()
            self.assertEqual(s.get(), '6')
            self.assertEqual(s.get(), '7')
