
int_var = 42
float_var = 3.14
str_var = "Hello World!"
list_var = [int_var, str_var, float_var, 7, [1, 2, 3]]

list_var[0] = 4.2
del list_var[2]

a = 0xff
a = 0b10010010

a = 8
if a == 6 {
    print(list_var[1])
} else {
    print(len(list_var))
}

put_pixel(4, 5)
clear_pixel(4, 5)

func some_function(a, b) {
    print("total")
    return a+b
}

a = some_function(a+7, 22/7)

for i in "hello":
    print(i)

b = 0
for i in [0, 1, 2, 3] {
    b += i
}
