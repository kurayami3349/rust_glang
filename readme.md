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


主要编写文件：
[rust_parser.py](src/lian/lang/parser/rust_parser.py)
参考文件:
- [java_parser.py](src/lian/lang/parser/java_parser.py) 可以借鉴java的解析方法；
- [rust_grammar.js](rust_grammar.js) 可以查看相应的grammer；
- [node-types.json](node-types.json) 可以查看node的结构；

## 第一部分 处理expression

### 进度表

- [x]  range_expression,
- [x]  unary_expression,
- [x]  reference_expression,
- [x]  try_expression,
- [x]  binary_expression,
- [x]  assignment_expression,
- [x]  compound_assignment_expr,
- [x]  type_cast_expression,
- [x]  call_expression,
- [x]  return_expression,
- [x]  yield_expression,
- [ ]  generic_function,
- [x]  await_expression,
- [x]  field_expression,
- [ ]  array_expression, 
- [ ]  tuple_expression,
- [ ]  unit_expression,
- [ ]  break_expression,
- [ ]  continue_expression,
- [ ]  index_expression,
- [ ]  closure_expression,
- [ ]  parenthesized_expression,
- [ ]  struct_expression,
- [ ]  if_expression,
- [ ]  match_expression,
- [ ]  while_expression,
- [ ]  loop_expression,
- [ ]  for_expression,



没有特别分类的expression的最终GLang IR 统一格式共用"assign_stmt"
```
statements.append({"assign_stmt": { "data_type": shadow_type, "target": shadow_target, "operator": shadow_operator,
                                   "operand": shadow1, "operand2": shadow2}})
```
assign_stmt: `data_type`  `target`  `operand` `operator` `operand2`

用于说明赋值语句，格式为target = <operand> <operator> <operand2>
- `data_type`指明赋值后的数据类型
- `target`为目标变量
- `operand`和`operand2`为源变量
- `operator`为操作符
如果`operator`和`operand2`为空，表示一元运算

例如a += 1

{"assign_stmt": {"target": "a", "operator": "+", "operand": "a", "operand2": 1}}
