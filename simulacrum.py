import unittest


class Simulacrum (object):
    """I record method calls and attribute accesses to a set of probe objects."""
    def __init__(self):
        raise NotImplementedError(`Simulacrum`)


class Probe (object):
    def __init__(self):
        raise NotImplementedError(`Simulacrum`)


# Unittests:
class SessionTests (unittest.TestCase):
    def test_empty_session(self):
        Simulacrum().verify()

    def _setup_two_attr_session(self):
        S = Simulacrum()

        x = S.probe.x
        y = S.probe.y

        self.assertIsInstance(x.someattr, Probe)
        self.assertIsInstance(y.somemethod(42, flag=True), Probe)

        return (S, x, y)

    def test_two_attr_session_verification(self):
        '''Test that verification can verify side effects across multiple objects.'''
        (S, x, y) = self._setup_two_attr_session()

        S.verify(
            S.spec.x.someattr,
            S.spec.y.somemethod(42, flag=True),
            )

    def test_two_attr_session_verification_order_sensitivity(self):
        '''Test that verification is sensitive to side-effect order across all probes.'''
        (S, x, y) = self._setup_two_attr_session()

        self.assertRaises(
            AssertionError,
            S.verify,
            S.spec.y.somemethod(42, flag=True),
            S.spec.x.someattr,
            )

    def test_two_attr_session_reprs(self):
        (S, x, y) = self._setup_two_attr_session()

        self.assertRegexpMatches('^<Simulacrum@[0-9a-f]{8,16}.probe.x>$', repr(x))
        self.assertRegexpMatches('^<Simulacrum@[0-9a-f]{8,16}.probe.y>$', repr(y))

        # TODO: assert that we can verify __repr__ was called.
        # This requires a feature of configuration, which will come after basic record/verify.

    def _setup_two_return_session(self):
        S = Simulacrum()

        x = S.probe()
        y = S.probe()

        self.assertIsInstance(x.someattr, Probe)
        self.assertIsInstance(y.somemethod(42, flag=True), Probe)

        return (S, x, y)

    def test_two_return_session_verification_with_stack_specs(self):
        (S, x, y) = self._setup_two_return_session()

        S.verify(
            S.spec().someattr,
            S.spec().somemethod(42, flag=True),
            )

    def test_two_return_session_verification_with_local_specs(self):
        (S, x, y) = self._setup_two_return_session()

        # We write the test this way for contrast to both
        # test_two_return_session_verification_with_stack_specs and
        # test_two_return_session_specification_order_sensitivity below.
        specx = S.spec()
        specy = S.spec()

        S.verify(
            specx.someattr,
            specy.somemethod(42, flag=True),
            )

    def test_two_return_session_verification_order_sensitivity(self):
        (S, x, y) = self._setup_two_return_session()

        self.assertRaises(
            AssertionError,
            S.verify,
            S.spec().somemethod(42, flag=True),
            S.spec().someattr,
            )

    def test_two_return_session_specification_order_sensitivity(self):
        (S, x, y) = self._setup_two_return_session()

        specx = S.spec()
        specy = S.spec()

        S.verify(
            specy.someattr,
            specx.somemethod(42, flag=True),
            )

    def test_two_return_session_reprs(self):
        (S, x, y) = self._setup_two_attr_session()

        self.assertRegexpMatches('^<Simulacrum@[0-9a-f]{8,16}.probe()#0>$', repr(x))
        self.assertRegexpMatches('^<Simulacrum@[0-9a-f]{8,16}.probe()#1>$', repr(y))

        # TODO: assert that we can verify __repr__ was called.
        # This requires a feature of configuration, which will come after basic record/verify.

    def test_complicated_probe_and_spec_reprs(self):
        S = Simulacrum()

        self.assertRegexpMatches(
            '^<Simulacrum@[0-9a-f]{8,16}.probe(42, flag=True)#0.thingy>$',
            repr(S.probe(42, flag=True).thingy))

        self.assertRegexpMatches(
            '^<Simulacrum@[0-9a-f]{8,16}.spec(42, flag=True)#0.thingy>$',
            repr(S.spec(42, flag=True).thingy))



if __name__ == '__main__':
    unittest.main()
