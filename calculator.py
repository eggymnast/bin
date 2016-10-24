variable_1 = input('enter the first number :')
operator = input('enter the operator:')
variable_2 = input('enter the second number :')
variable_1 = float(variable_1)
variable_2 = float(variable_2)

if (operator == '+'):
    print (variable_1, operator, variable_2, '=', variable_1 + variable_2)
elif (operator == '-'):
    print (variable_1, operator, variable_2, '=', variable_1 - variable_2)
elif (operator == '/'):
    print (variable_1, operator, variable_2, '=', variable_1 / variable_2)
elif (operator == '*'):
    print (variable_1, operator, variable_2, '=', variable_1 * variable_2)
elif (operator == '//):
    print (variable_1, operator, variable_2, '=', variable_1 // variable_2)
elif (operator == '**'):
    print (variable_1, operator, variable_2, '=', variable_1 ** variable_2)
else:
    print ('operator not recognized')
