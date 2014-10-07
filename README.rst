==========
Simulacrum
==========

This is currently vapor-ware.  The idea is to provide a mocking library where:

* The usage and ordering of multiple mocked objects are tracked in "sessions".  ie: The test specification can ensure ``os.mkdir`` was called prior to ``urllib.urlopen`` in the code under test.
* For a single mocked object, the `specification` of behavior, `detection and recording` of application usage, and the `verification / examination` of results are cleanly separated interfaces.

A quick sketch of the API might be something like:

..code:: python

    import simulacrum
    
    session = simulacrum.Session()
    
    (mkdir_spec, mkdir_verifier) = session.patch('os.mkdir')
    mkdir_spec.return_value = None
    
    (urlopen_spec, urlopen_verifier) = session.patch('urllib.urlopen')
    
    application_code_function() # It's use of os.mkdir and urllib.urlopen use the "probes" associated with the specifications above.
    
    assert session.interactions == [
        mkdir_verifier('/tmp/foo_app'),
        urlopen_verifier('http://example.com/foo', data=None),
        urlopen_verifier.return_value.read(),
        ]

The ``*_spec`` objects configure how the probes should behave.  The probes are implicitly installed by ``session.patch`` as with the ``mock.patch`` call, except the latter returns a conflated interface that includes specification, probing, and recording all in one.  This example code doesn't close the patches, so the api would be similar to ``mock.patch``, with context handlers and method decorators, etc...

