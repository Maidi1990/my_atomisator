===============================
atomisator.parser
===============================

The parser knows how to return a feed content, with the 'Parse' function, available as a top-level function::

    >>> from atomisator.parser import Parse

This function takes the feed url and returns an iterator over its content. A second parameter can specify a maximum number of entries to return. If not given, it is fixed to 10.
::

    >>> import os
    >>> res = Parse(os.path.join(test_dir, 'ifeng_world.xml'))
    >>> res
    <itertools.islice object at ...>

Each item is a dictionary the contain the entry:
::
    >>> entry = res.next()
    >>> entry['title']
    u'...'

The keys available are:
::
    >>> keys = sorted(entry.keys())
    >>> list(keys)
    [...]