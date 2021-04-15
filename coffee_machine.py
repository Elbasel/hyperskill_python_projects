class CoffeeMachine:

    def __init__(self, contents, state='idle'):
        self.state = state
        self.contents = contents

    def display_contents(self):
        print('The coffee machine has:')
        for key, value in self.contents.items():
            print(f'{value} of {key}')
        print()

    def buy(self):
        coffee_types = {1: {'water': -250, 'coffee beans': -16, 'money': 4},
                        2: {'water': -350, 'milk': -75, 'coffee beans': -20, 'money': 7},
                        3: {'water': -200, 'milk': -100, 'coffee beans': -12, 'money': 6},
                        }

        input_type = input('What do you want to buy? 1 - espresso, 2 - latte, 3 - cappuccino, back - to main menu:')
        if input_type == 'back':
            return
        coffee = coffee_types[int(input_type)]

        for key, value in coffee.items():
            if key == 'money':
                continue
            if abs(value) > self.contents[key]:
                print(f'Sorry, not enough {key}')
                return

        print('I have enough resources, making you a coffee!')
        for key, value in coffee.items():
            self.contents[key] += value
        self.contents['disposable cups'] -= 1

    def fill(self):
        measures = {'water': 'ml', 'milk': 'ml', 'coffee beans': 'grams', 'disposable cups': ''}
        for key in self.contents.keys():
            if key == 'money':
                continue
            amount = int(input(f'Write how many {measures[key]} of {key} you want to add: '))
            self.contents[key] += amount

    def take(self):
        print(f'I gave you {self.contents["money"]}')
        self.contents['money'] = 0

    def run_function(self, cmd):
        commands = {'remaining': self.display_contents, 'buy': self.buy, 'fill': self.fill, 'take': self.take}
        commands[cmd]()


coffee_machine = CoffeeMachine({'water': 400, 'milk': 540, 'coffee beans': 120, 'disposable cups': 9, 'money': 550})

while True:
    action = input('Write action (buy, fill, take, remaining, exit): ')
    if action == 'exit':
        break
    coffee_machine.run_function(action)
