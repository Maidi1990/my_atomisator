#   关于db

##  1.安装依赖

db，database数据库的简称，所用到的两个依赖皆与数据库有关：
```
    install_requires=[
        'setuptools',   ## 这个依赖是各个包必须的
        'pysqlite',     ## 使用sqlite数据库
        'SQLAlchemy'],  ## 用以创建映射的包，此是重点
```
##  2.创建映射

1. 导入数据库相关的对象
from sqlalchemy import DateTime, Column...这些什么的略过。值得一提的是，一个表对应着一类，而这个类是继承自**declarative_base**：
```
    from sqlalchemy.ext.declarative import declarative_base
    Base = declarative_base()
    class Tablename(Base):
        __tablename__ = 'something'
```
- *declarative_base*顾名思义，声明基类，这应该不难记:-)；
- *Base*这个对象是必须要定义的，因为不仅在**映射**中会用到，待会写*session*代码时也会用到的。这个*Base*是将*class Tablename*映射成真正的数据表的必要。

2. 与书中不同的是，我在创建表的*外链*的时候，用的是**relationship**：
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
- 应注意到Link和Tag类的*atomisator_entry_id*属性，其中的*Foreignkey('atomisator_entry.id')*中的**atomisator_entry**来自Entry类的*__tablename__*；
- Entry类中的links的*back_populates='entry'*则来自Link&Tag类的entry属性；  
  
*------------------------总结----------------------*  
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
  
*------------------create_session的讲解------------------*  
指定数据库，创建引擎
```
    engine = create_engine(sqluri)
```
其中，*sqluri*用内存作数据库可以这么写： *sqlite:///:memory:*；  
ubuntu中，指定一个文件为数据库可以这么写：*sqlite:///test.db* ——即在与session.py同目录下创建一个数据库test.db。  
```
    metadata.create_all(engine)
```
且看**metadata**的来历:
```
    from atomisator.db.mappers import Base
    metadata = Base.metadata
```
上文创建映射时，同时创建了一个全局对象**Base**，还记得不？Entry、Link和Tag继承的父类，亦此处之**Base**也。原来此物是数据表和session的桥梁，哈哈。
```
    Session = sessionmaker(bind=engine, autoflush=True, autocommit=False)
```
此句就创建了一个session类——是的，只是session类，看清楚，*Session*首字母大写哦。
```
    global session
    ...
    session = Session()
```
将*Session实例*保存在一个模块全局变量session（此又是首字母小写），方便共享给模块内其它函数。  

##  4.操作数据库

这个模块可以说是整个**db**最核心最被书的作者重视的部分了——从其命名可知：core.py。  
这个模块也是定义几个函数：  
- 新建一个entry，*create_entry*；
- 删除entry,可以一次删除一个或多个entry，*purge_entries*；
- 获取entry,可以一次获取一个或多个entry，*get_entries*；  

至此，各个模块的介绍工作完毕！  
——其实，我们也可以按照上面的思路，先快速**起草**整个db用到的各个对象，然后紧接着写测试文档的。写了测试文档后，然后再来接着完善各个对象的代码。这就是我目前理解的**测试驱动开发(TDD)**。  

*--------------------------get_entries的讲解---------------------------*  
core.py中几个函数都是运用session.py中的全局变量session操作数据库的，明白了*get_entries*，即可明了其它。  
先看*get_entries*的原型:  
```
    get_entries(size=None, session=default_session, **kw)
```
这三个关键字参数，最重要的是session，这也是**整个core.py的函数**所共有的参数，其默认值为*default_session*；  
再查看  
```
    from atomisator.db import session as default_session
```
*default_session*是整个session.py模块？是的。为何要这样用？还记得session.py定义了几个对象吗（在python中，函数、变量、类，都是对象）？
- 全局变量session，保存了*create_session*返回的*session*实例；
- 函数*create_session*，创建*session*，并返回*session*实例；
- 函数*save*，添加修改到缓存；
- 函数*commit*，提交修改到数据库；  
...

上边几个函数都需要共用一个session，不是吗？那如何才能做到共有一个session呢？很明显地，只能在模块层面上调用它们，也就是在调用这些函数时，都要加前缀**session.**；  

##  5.测试

这里我们只了解下doctest就好。  
具体见 [atomisator/db/docs/README.txt](https://github.com/Maidi1990/my_atomisator/blob/db/atomisator.db/atomisator/db/docs/READMED.txt)。
