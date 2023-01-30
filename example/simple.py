from fancy_table import FancyTable

t = FancyTable(['Name', 'Age', 'Job Title', 'Comment'])
t.add_section('Singapore')
t.add_row(['Alice', '25', 'Designer', 'Dog lover'])
t.add_row(['Bob', '35', 'Developer', 'Anime nerd'])
t.add_row(['Carl', '33', 'Manager', 'Plays football'])
t.add_section('Boston')
t.add_row(['Alice', '25', 'Designer', 'Dog lover'])
t.add_row(['Bob', '35', 'Developer', 'Anime nerd'])
t.add_section('San Francisco')
t.add_row(['Carl', '33', 'Manager', 'Plays football'])

print(t)
