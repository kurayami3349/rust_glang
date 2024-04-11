#!/usr/bin/env python3

import os
import sys
case_dir = "/app/experiment_2/test/cases/"
# # 获取命令行测试样例
case_file = sys.argv[1]  
#case_name = "assignment_expr.rs"

command = os.path.realpath("/app/experiment_2/src/lian/lang/main.py") + " --lang=rust -debug -print_statements " + os.path.realpath(case_dir+case_file)

print(command)

os.system(command)