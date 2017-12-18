#   关于db

##  1.安装依赖

db，database数据库的简称，所用到的两个依赖皆与数据库有关：
```
    install_requires=[
        'setuptools',   ## 这个依赖是各个包必须的
        'pysqlite',     ## 使用sqlite数据库
        'SQLAlchemy'],  ## 用以创建映射
```

##  2.创建映射

1. 导入数据库相关的对象
from sqlalchemy import DateTime, Column...这些什么略过。值得一提的是，一个表对应着一类，而这个类是继承自：
```
    from sqlalchemy.ext.declarative import declarative_base
    Base = declarative_base()
    class Tablename(Base):
        __tablename__ = 'something'
```
- *declarative_base*顾名思义，声明基类很好记；
- *Base*这个对象是必须要定义的，因为不仅在**映射**中会用到，待会写*session*代码时也会用到的。这个*Base*是将*class Tablename*映射成真正的数据表的必要。

2. 与书中不同的是，我在创建表的*外链*的时候，用的是：
```
    ...
    from sqlalchemy import Integer
    from sqlalchemy import Foreignkey
    from sqlalchemy import Text
    from sqlalchemy.orm import relationship
    from sqlalchemy.ext.declarative import declarative_base
    Base = declarative_base()

    class Entry(Base):
        __tablename__ = 'atomisator_entry'
        ...
        links = relationship("Link", order_by=Link.id, back_populates="entry")
        tags = relationship("Tag", order_by=Tag.id, back_populates="entry")

    class Link(Base):
        __tablename__ = 'atomisator_link'
        atomisator_entry_id = Column(Integer, Foreignkey('atomisator_entry.id'))
        entry = relationship('Entry', back_populates='links')
        ...

    class Tag(Base):
        __tablename__ = 'atomisator_tag'
        atomisator_entry_id = Column(Integer, Foreignkey('atomisator_entry.id'))
        entry = relationship('Entry', back_populates='links')
        ...
```
- 注意到Link和Tag类的*atomisator_entry_id*，其中的*Foreignkey('atomisator_entry.id')*中的**atomisator_entry**来自Entry类的*__tablename__*；
- Entry类中的links的*back_populates='entry'*则来自Link&Tag类的entry属性；
- 为了实现外链接，Entry增加了两个属性*links & tags*;
- 为了实现外链接，Tag增加了两个属性*atomisator_entry_id & entry*;
- 为了实现外链接，Link增加了两个属性*atomisator_entry_id & entry*;

##  3.创建session

书中关于session的部分全都用函数来包装，比如：
- 创建session，用*create_session*；
- 添加，用*save*；
- 提交，用*commit*；
- 查询，用*query*；
- 执行，用*execute*；
而很巧妙的是，实现这些包装的背后逻辑是，定义一个模块全局变量session，用来保存*create_session*函数新建的session，然后交给同模块中的其它函数运用。

##  4.操作数据库

这个模块可以说是整个**db**最核心最被书的作者重视的部分了——从其命名可知：core.py。
这个模块也是定义几个函数：
- 新建一个entry，*create_entry*；
- 删除entry,可以一次删除一个或多个entry,*purge_entries*；
- 获取entry,可以一次获取一个或多个entry,*get_entries*；
至此，各个模块的介绍工作完毕——其实，我们也可以按照上面的思路，先快速*起草*整个db用到的各个对象，然后紧接着写测试文档的。写了测试文档后，然后再来接着完善各个对象的代码。这就是我目前理解的**测试驱动开发(TDD)**。

##  5.测试



