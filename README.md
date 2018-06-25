## 这是什么

这是一个personal python小工具project

## 功能介绍

- `mpfr.py` 多进程读取文件，处理数据。实际上多进程读取文件并不能加快读取速度，这里主要加速的是读取batch大小数据后的并行数据处理。可处理中文数据。

## 参考资料

- http://effbot.org/zone/wide-finder.htm#a-multi-threaded-python-solution
- https://lists.gt.net/python/bugs/750392
- http://www.blopig.com/blog/2016/08/processing-large-files-using-python/