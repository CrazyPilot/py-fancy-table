from fancy_table import FancyTable

t = FancyTable(['Name', 'Age', 'Job Title', 'Comment'], 'first table')
t.add_section('Singapore')
t.add_row(['Alice', 25, 'Designer', 'Dog lover'])
t.add_row(['Bob', 35, 'Developer', 'Anime nerd'])
t.add_row(['Carl', '33', 'Manager', 'Plays football'])
t.add_section('Boston')
t.add_row(['Alice', '25', 'Designer', 'Dog lover'])
t.add_row(['Bob', '35', 'Developer', 'Anime nerd'])
t.add_section('San Francisco')
t.add_section('San Francisco 2')
t.add_row(['Carl', '33', 'Manager', 'Plays football'])
print(t)


t2 = FancyTable(['Name', 'Age', 'Job Title', 'Comment'])
t2.add_row(['Alice', '25', 'Designer', 'Dog lover'])
t2.add_row(['Bob', '35', 'Developer', 'Anime nerd'])
t2.add_section('Singapore')
print(t2)
