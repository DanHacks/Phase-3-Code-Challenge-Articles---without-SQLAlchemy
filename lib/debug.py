#!/usr/bin/env python3

from sqlalchemy import create_engine

from models import Company, Dev

if __name__ == '__main__':
    engine = create_engine('sqlite:///freebies.db')
    import ipdb; ipdb.set_trace()
