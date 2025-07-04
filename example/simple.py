from fancy_table import FancyTable
from colorama import Fore

t = FancyTable(['Name', 'Age', 'Job Title', 'Comment'], 'first table')
t.add_section('Singapore')
t.add_row(['Alice', 25, 'Designer', 'Dog lover'])
t.add_row(['Bob', 35, 'Developer', 'Anime nerd'], Fore.GREEN)
t.add_row(['Carl', '33', 'Manager', 'Plays football'], Fore.RED)
t.add_section('Boston')
t.add_row(['Alice', '25', 'Designer', 'Dog lover'])
t.add_row(['Bob', '35', 'Developer', 'Anime nerd'])
t.add_section('San Francisco')
t.add_section('San Francisco 2')
t.add_row(['Carl', '33', 'Manager', 'Plays football'])
print(t)


t2 = FancyTable(['Name', 'Age', 'Job Title', 'Comment'])
t2.border_color = Fore.MAGENTA
t2.add_row(['Alice', '25', 'Designer', 'Dog lover'])
t2.add_row(['Bob', '35', 'Developer', 'Anime nerd'])
t2.add_section('Singapore')
print(t2)


t3 = FancyTable(['Name', 'Age', 'Job Title', 'Comment'])
t3.add_row(['Alice', '25', 'Designer', 'Dog lover'])
t3.add_row([Fore.GREEN + 'Bob' + Fore.RESET, '35', 'Developer', 'Anime nerd'])
t3.add_row(['Carl', '33', 'Manager', 'Plays football'])
print(t3)
