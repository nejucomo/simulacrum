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

    def _setupSession(self):
        R = Recorder()

        p1 = R.make_probe()
        p2 = R.make_probe()

        self.assertIsInstance(p1.someattr, Probe)
        self.assertIsInstance(p2.somemethod(), Probe)

        V = R.get_verifier()

        return (V, p1, p2)

    def test_basic_session_verification(self):
        '''Test that verification can verify side effects across multiple objects.'''
        (V, p1, p2) = self._setupSession()

        V.verify(
            V[p1].someattr,
            V[p2].somemethod,
            )

    def test_basic_session_order_sensitivity(self):
        '''Test that verification is sensitive to side-effect order across all probes.'''
        (V, p1, p2) = self._setupSession()

        self.assertRaises(
            AssertionError,
            V.verify,
            V[p2].somemethod,
            V[p1].someattr,
            )


if __name__ == '__main__':
    unittest.main()
