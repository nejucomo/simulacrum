import unittest


class Recorder (object):
    """I record method calls and attribute accesses to a set of probe objects."""
    def __init__(self):
        raise NotImplementedError(`Recorder`)


class Probe (object):
    def __init__(self):
        raise NotImplementedError(`Recorder`)


# Unittests:
class SessionTests (unittest.TestCase):
    def test_empty_session(self):
        Recorder().get_verifier().verify()

    def _setupTwoAttrSession(self):
        R = Recorder()

        x = R.probe.x
        y = R.probe.y

        self.assertIsInstance(x.someattr, Probe)
        self.assertIsInstance(y.somemethod(42, flag=True), Probe)

        return (R, x, y)

    def test_basic_session_verification(self):
        '''Test that verification can verify side effects across multiple objects.'''
        (R, x, y) = self._setupTwoAttrSession()

        R.verify(
            R.spec.x.someattr,
            R.spec.y.somemethod(42, flag=True),
            )

    def test_basic_session_order_sensitivity(self):
        '''Test that verification is sensitive to side-effect order across all probes.'''
        (R, x, y) = self._setupTwoAttrSession()

        self.assertRaises(
            AssertionError,
            R.verify,
            R.spec.y.somemethod(42, flag=True),
            R.spec.x.someattr,
            )


if __name__ == '__main__':
    unittest.main()
