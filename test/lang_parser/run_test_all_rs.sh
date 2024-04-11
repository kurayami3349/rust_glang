#!/bin/bash

# 设置测试用例目录
case_dir="/app/experiment_2/test/cases/"

# 遍历测试用例目录下的所有 .rs 文件
for case_file in "$case_dir"/*.rs; do
    
    
    # 运行 Python 脚本，并传递测试用例文件名作为参数
    python test_rs.py "$case_file"
done
