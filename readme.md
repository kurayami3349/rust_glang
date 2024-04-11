# 将rust从AST翻译为Glang IR

GLang IR格式：
https://docs.qq.com/sheet/DTU9ieFhkYU1BVmN1?tab=urh0bh

编写cases测试样例以及测试python程序。

`test/cases/` 中填写测试样例(eg: assignment_expr.rs)

`test/lang_parser/`中填写测试程序py

命令行运行测试
```
python test_rs.py <case_file> 
```
或者运行`run_test_rs.sh`，**需要自行设置case_file**


