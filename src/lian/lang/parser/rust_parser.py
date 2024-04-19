#!/usr/bin/env python3

from . import common_parser


class Parser(common_parser.Parser):
    def is_comment(self, node):
        # return node.type in ["line_comment", "block_comment"]
        pass

    def is_identifier(self, node):
        return node.type == "identifier"

    def number_literal(self, node, statements, replacement):
        value = self.read_node_text(node)
        value = self.common_eval(value)
        return str(value)

    
    def string_literal(self, node, statements, replacement):
        replacement = []
        for child in node.named_children:
            self.parse(child, statements, replacement)

        ret = self.read_node_text(node)
        if replacement:
            for r in replacement:
                (expr, value) = r
                ret = ret.replace(self.read_node_text(expr), value)

        #ret = self.handle_hex_string(ret)

        return self.escape_string(ret)
    
    def char_literal(self, node, statements, replacement):
        value = self.read_node_text(node)
        return "'%s'" % value
    
    def boolean_literal(self, node, statements, replacement):
        return self.read_node_text(node)

    def obtain_literal_handler(self, node):
        LITERAL_MAP = {
            "string_literal"       : self.string_literal,
            "char_literal"          : self.char_literal,
            "boolean_literal"       : self.boolean_literal,
            "integer_literal"       : self.number_literal,
            "float_literal"         : self.number_literal,
        }

        return LITERAL_MAP.get(node.type, None)

    def is_literal(self, node):
        return self.obtain_literal_handler(node) is not None

    def literal(self, node, statements, replacement):
        handler = self.obtain_literal_handler(node)
        return handler(node, statements, replacement)

    def check_declaration_handler(self, node):
        DECLARATION_HANDLER_MAP = {
        }
        return DECLARATION_HANDLER_MAP.get(node.type, None)

    def is_declaration(self, node):
        return self.check_declaration_handler(node) is not None

    def declaration(self, node, statements):
        handler = self.check_declaration_handler(node)
        return handler(node, statements)

    def check_expression_handler(self, node):
        EXPRESSION_HANDLER_MAP = {
            "range_expression"          : self.range_expression,

            # expression without range

            "unary_expression"          : self.unary_expression,
            "reference_expression"      : self.reference_expression,
            "try_expression"            : self.try_expression,
            "binary_expression"         : self.binary_expression,
            "assignment_expression"     : self.assignment_expression,
            "compound_assignment_expr"  : self.compound_assignment_expr,
            "type_cast_expression"      : self.type_cast_expression,
            "call_expression"           : self.call_expression,
            "return_expression"         : self.return_expression,
            "yield_expression"          : self.yield_expression,
            "generic_function"          : self.generic_function,
            "await_expression"          : self.await_expression,
            "field_expression"          : self.field_expression,
            "array_expression"          : self.array_expression, 
            "tuple_expression"          : self.tuple_expression,
            "unit_expression"           : self.unit_expression,
            "break_expression"          : self.break_expression,
            "continue_expression"       : self.continue_expression,
            "index_expression"          : self.index_expression,
            "closure_expression"        : self.closure_expression,
            "parenthesized_expression"  : self.parenthesized_expression,
            "struct_expression"         : self.struct_expression,
        
            # expression ending with block

            "if_expression"             : self.if_expression,
            "match_expression"          : self.match_expression,
            "while_expression"          : self.while_expression,
            "loop_expression"           : self.loop_expression,
            "for_expression"            : self.for_expression,

            # others

            # "let_condition":,
            # "else_clause" :,
            # "arguments":,
            # "field_initializer_list":,
            # "shorthand_field_initializer":,
            # "field_initializer":,
            # "base_field_initializer":,

            
        }

        return EXPRESSION_HANDLER_MAP.get(node.type, None)
    # range
    def range_expression(self, node, statements):
        return 
    # unary
    def unary_expression(self, node, statements):
        shadow_expr = node.named_children[0]

        tmp_var = self.tmp_variable(statements)
        statements.append({"assign_stmt": {"target": tmp_var, "operand": shadow_expr}})
        return tmp_var

    # reference
    def reference_expression(self, node, statements):
        return 
    # try
    def try_expression(self, node, statements):
        return 
    # binary
    def binary_expression(self, node, statements):
        left = self.find_child_by_field(node, "left")
        right = self.find_child_by_field(node, "right")
        operator = self.find_child_by_field(node, "operator")

        shadow_operator = self.read_node_text(operator)

        shadow_left = self.parse(left, statements)
        shadow_right = self.parse(right, statements)

        tmp_var = self.tmp_variable(statements)
        statements.append({"assign_stmt": {"target": tmp_var, "operator": shadow_operator, "operand": shadow_left,
                                           "operand2": shadow_right}})

        return tmp_var
    
    # assignment
    def assignment_expression(self, node, statements):
        # prec.left
        left = self.find_child_by_field(node, "left")
        right = self.find_child_by_field(node, "right")
        
        shadow_left = self.parse(left, statements)

        shadow_right = self.parse(right, statements)


        statements.append({"assign_stmt": {"target": shadow_left, "operator":"=", "operand": shadow_right}})
        
        return shadow_left 

    # compound_assignment_expr
    def compound_assignment_expr(self, node, statements):
        left = self.find_child_by_field(node, "left")
        right = self.find_child_by_field(node, "right")
        operator = self.find_child_by_field(node, "operator")
        shadow_operator = self.read_node_text(operator).replace("=", "")

        shadow_left = self.parse(left, statements)

        shadow_right = self.parse(right, statements)

        statements.append({"assign_stmt": {"target": shadow_left, "operator": shadow_operator,
                                           "operand": shadow_left, "operand2": shadow_right}})
        return shadow_left

    # type_cast   不确定正确性
    def type_cast_expression(self, node, statements):
        value = self.find_child_by_field(node, "value")
        type = self.find_child_by_field(node, "type")

        shadow_value = self.parse(value, statements)

        # 先处理这两种类型，type简单为字面值 eg: i32, container(自定义类型名)...
        if type.type == "primitive_type" or "type_identifier":
            shadow_type = self.read_node_text(type)
        
        else:
            shadow_type = self.parse(type, statements)
        

        tmp_var = self.tmp_variable(statements)
        
        statements.append({"assign_stmt": {"data_type": shadow_type, "target": tmp_var, 
                                           "operator": "type_cast", "operand": shadow_value}})

        return tmp_var

    # call
    def call_expression(self, node, statements):
        return 

    # return
    def return_expression(self, node, statements):
        shadow_target = ""
        if node.named_child_count > 0:
            child = node.named_children[0]
            shadow_name = self.parse(child, statements)

        statements.append({"return_stmt": {"target": shadow_target}})
        return shadow_target
         

    # yield
    def yield_expression(self, node, statements):
        shadow_target = ""
        if node.named_child_count > 0:
            child = node.named_children[0]
            shadow_name = self.parse(child, statements)

        statements.append({"yield_stmt": {"target": shadow_target}})
        return shadow_target 

    # generic_function
    def generic_function(self, node, statements):
        return 

    # await
    def await_expression(self, node, statements):
        return 

    # field
    def field_expression(self, node, statements):
        return 

    # array
    def array_expression(self, node, statements):
        return 

    # tuple
    def tuple_expression(self, node, statements):
        return 
    # unit
    def unit_expression(self, node, statements):
        return 
    # break
    def break_expression(self, node, statements):
        return 
    # continue
    def continue_expression(self, node, statements):
        return 
    # index
    def index_expression(self, node, statements):
        return 
    # closure
    def closure_expression(self, node, statements):
        return 
    # parenthesized
    def parenthesized_expression(self, node, statements):
        return 
    # struct
    def struct_expression(self, node, statements):
        return 
    # if
    def if_expression(self, node, statements):
        return

    # match
    def match_expression(self, node, statements):
        return

    # while
    def while_expression(self, node, statements):
        return

    # loop
    def loop_expression(self, node, statements):
        return

    # for
    def for_expression(self, node, statements):
        return
    

    def is_expression(self, node):
        return self.check_expression_handler(node) is not None

    def expression(self, node, statements):
        handler = self.check_expression_handler(node)
        return handler(node, statements)

    def check_statement_handler(self, node):
        STATEMENT_HANDLER_MAP = {
        }
        return STATEMENT_HANDLER_MAP.get(node.type, None)

    def is_statement(self, node):
        return self.check_statement_handler(node) is not None

    def statement(self, node, statements):
        handler = self.check_statement_handler(node)
        return handler(node, statements)
