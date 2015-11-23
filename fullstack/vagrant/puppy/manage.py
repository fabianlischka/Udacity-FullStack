#!/usr/bin/env python
from migrate.versioning.shell import main

if __name__ == '__main__':
    main(url='sqlite:///puppies.db', debug='False', repository='puppy_repository')
