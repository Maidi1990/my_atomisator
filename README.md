# 《python高级编程×第六章》关于atomisator.parser等各个包的初始构建

-   具体构建细节可查看各个包根目录的*README.md*
-   此处以atomisator.parser为例讲解

##  1.利用已经创建好的包模板*mao_bao*，迅速创建parser包的文件结构。包模板的文件结构如下：

```
    $ cd my_atomisator
    $ paster create -t mao_bao atomisator.parser
    
    $ cd atomisator.parseer
    $ find atomisator
    atomisator
    atomisator/__init__.py
    atomisator/parser
    atomisator/parser/docs
    atomisator/parser/docs/READMED.txt
    atomisator/parser/__init__.py
    atomisator/parser/tests
    atomisator/parser/tests/__init__.py
    atomisator/parser/tests/test_docs.py
```
##  2.添加 *依赖* ：

```
    $ vim ./atomisator.parser/setup.py
    ...
    install_requires=[
        'setuptools',
        'feedparser'],
    ...
```
##  3.添加测试插件，使用 *nose*：

```
    $ vim ./atomisator.parser/setup.py
    ...
    test_suite = 'nose.collector',
    test_requires = ['Nose'],
    ...
```
##  4.创建初始的 *doctest* ：

```
    $ vim ./atomisator.parser/atomisator/parser/docs/README.txt
    ...
    可参见具体的文件。
```
*补充：不得不说，doctest是个很好玩却并不强大的东西。这里，tests/test_docs.py中有直接 **import doctest** ，可以琢磨。*  

##  5.配置*~/.noserc*文件：

```
    - 在根目录（即~/）创建并设置.noserc文件
        $ vim ~/.noserc
        [nosetests]
        verbosity=3
        with-doctest=1
        doctest-extension=.txt
    - 在命令行输入命令 **nosetests** ——勿忘了末尾的 *s* ，哈哈。
```
*补充：由于目前，我们还没有在atomisator.parser中放置任何有用的代码，是以在命令行输入**nosetests** 后,会看到报错，即出现 **failure** 字样。*   

##  6.在atomisator.parser中编写代码：

```
    $ vim ./atomisator.parser/__init__.py
    ...
```
*补充：其中 atomisator.parser中的代码不一定要放在__init__.py中。事实上，工作中更常见的是，保持__init__.py空白，然后将代码编写在其它文件中，当然这个代码文件得在./atomisator.parser/atomisator/parser/目录下。* 
 
##  7.在本地安装包并测试它

编码完毕后，保存。  
1. 安装模块：回到包的根目录（即./atomisator.parser/ 下），在命令行输入  
```
    $ python setup.py develop
```
*补充：使用develop命令安装包，方便开发并测试*  
2. 安装成功后，如果没有报错，则在命令行输入（确保还在包的根目录下）：  
```
    $ nosetests
```
 *nosetests* ——如果编写的代码无误，不会报错，显示 **ok** 字样；如果编写的代码有误，可以做两个选择：  
```
    1) 修改./docs/README.txt中的测试用例；
    2) 修改方才写在__init__.py中的代码；
```

