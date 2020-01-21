import re
string_lista = '[100,2,3],[4,5,6]'

regex = r'\[[0-9+,]*\]'
a = re.findall(regex, string_lista)

print(a)