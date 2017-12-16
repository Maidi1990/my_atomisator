from sqlalchemy import DateTime
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import ForeignKey
from sqlalchemy import Text

from sqlalchemy.orm import relationship

from sqlalchemy.ext.declarative import declarative_base

from datetime import datetime

Base = declarative_base()

class Link(Base):

    __tablename__ = 'atomisator_link'
    id = Column(Integer, primary_key=True)
    url = Column(String(300))
    atomisator_entry_id = Column(Integer, ForeignKey('atomisator_entry.id'))
    entry = relationship('Entry', back_populates='links')
    def __init__(self, url):
        super(Link, self).__init__()
        self.url = url
    def __repr__(self):
        return "<Link('%s')>" % self.url

class Tag(Base):

    __tablename__ = 'atomisator_tag'
    id = Column(Integer, primary_key=True)
    value = Column(String(100))
    atomisator_entry_id = Column(Integer, ForeignKey('atomisator_entry.id'))
    entry = relationship('Entry', back_populates='tags')
    def __init__(self, value):
        super(Tag, self).__init__()
        self.value = value
    def __repr__(self):
        return "<Tag('%s')>" % self.value

class Entry(Base):

    __tablename__ = 'atomisator_entry'
    id = Column(Integer, primary_key=True)
    link = Column(Text())
    date = Column(DateTime, default=datetime.now)
    updated = Column(DateTime, default=datetime.now)
    summary = Column(Text())
    summary_detail = Column('summary_detail', Text())
    title = Column(Text())
    title_detail = Column(Text())
    root_link = Column(Text())

    links = relationship("Link", order_by=Link.id, back_populates="entry")
    tags = relationship("Tag", order_by=Tag.id, back_populates="entry")

    def __init__(self, **kw):
        super(Entry, self).__init__()
        self.update(**kw)
    def update(self, **kw):
        if 'link' in kw:
            self.link = kw['link']
        if 'date' in kw:
            self.date = kw['date']
        if 'updated' in kw:
            self.updated = kw['updated']
        if 'summary' in kw:
            self.summary = kw['summary']
        if 'summary_detail' in kw:
            self.summary_detail = kw['summary_detail']
        if 'title_detail' in kw:
            self.title_detail = kw['title_detail']
        if 'title' in kw:
            self.title = kw['title']
        if 'links' in kw:
            self.add_links(kw['links'])
        if 'tags' in kw:
            self.add_tags(kw['tags'])
        if 'rook_link' in kw:
            self.rook_link = kw['rook_link']

    def add_links(self, links):
        self.links = [Link(link) for link in links if link]
    def add_tags(self, tags):
        self.tags = [Tag(tag) for tag in tags if tag]
    def __repr__(self):
        return "<Entry('%s')>" % self.title

