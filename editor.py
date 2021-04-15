def plain():
    txt = input('Text: ')
    text.append(txt)

def bold():
    txt = input('Text: ')
    text.append(f'**{txt}**')

def italic():
    txt = input('Text: ')
    text.append(f'*{txt}*')
    
def header():
    level = int(input('Level: '))
    if 0 < level < 7:
        txt = input('Text: ')
        text.append(f'{"#"*level} {txt}\n')  

def link():
    label = input('Label: ')
    url = input('URL: ')
    text.append(f'[{label}]({url})')

def code():
    txt = input('Text: ')
    text.append(f'`{txt}`')
    
def new_line():
    text.append('\n')

def uo_list():
    generate_list('uo')
    
def o_list():
    generate_list('o')

def generate_list(list_type):
    while True:
        rows = int(input('Number of rows: '))
        if rows > 0:
            break
        print('The number of rows should be greater than zero')
    if list_type == 'o':
        o_list = [f'{i}. {input("Row{i}: ")}\n' for i in range(1, rows+1)]
        text.extend(o_list)
    else:
        uo_list = [f'* {input("Row{i}: ")}\n' for i in range(1, rows+1)]
        text.extend(uo_list)

cmds = {'plain': plain, 'bold': bold, 'italic': italic, 'header': header, 'link': link,
'inline-code': code, 'ordered-list': o_list, 'unordered-list': uo_list, 'new-line': new_line}

text = []

while True:
    cmd = input('- Choose a formatter:')
    if cmd == '!done':
        with open('output.md', 'w') as output:
            output.write(''.join(text))
        break
    elif cmd == '!help':
        print('Available formatters:', ' '.join(cmds.keys()))
        print('Special commands: !help !done')
    elif cmd in cmds.keys():
        cmds[cmd]()
        print(''.join(text))        
    else:
        print('Unknown formatting type or command')
