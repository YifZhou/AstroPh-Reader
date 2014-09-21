def Datafiles(*filenames, **kw):
    import os
    
    def datafile(path, strip_path=True):
        parts = path.split('/')
        path = name = os.path.join(*parts)
        if strip_path:
            name = os.path.basename(path)
        return name, path, 'DATA'

    strip_path = kw.get('strip_path', True)
    return (datafile(filename, strip_path=strip_path)
        for filename in filenames
        if os.path.isfile(filename))

docfiles = Datafiles('arxiv.png', 'play.png', strip_path = False)