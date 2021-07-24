import math
import argparse
import sys

def get_nominal_interest(interest):
    return (interest / 100) / 12


def get_payments_duration(principal, payment, interest):

    nominal_interest = get_nominal_interest(interest)
    x = payment / (payment - nominal_interest * principal)
    n_months = math.ceil(math.log(x, 1 + nominal_interest))
    arg_dict['periods'] = n_months
    years, months = divmod(n_months, 12)

    s = 's' if years > 1 else ''
    years_str = f'{years} year{s}' if years > 0 else ''
    s = 's' if months > 1 else ''
    months_str = f' and {months} month{s}' if months > 0 else ''
    print(f'It will take {years_str}{months_str} to repay this loan!')


def get_annuity_payment(principal, periods, interest):
    
    nominal_interest = get_nominal_interest(interest)
    annuity_payment = principal * (
            (nominal_interest * pow(1 + nominal_interest, periods)) / (pow(1 + nominal_interest, periods) - 1))
    print(f'Your annuity payment = {math.ceil(annuity_payment)}!')
    arg_dict['payment'] = math.ceil(annuity_payment)




def get_principal(payment, periods, interest):
   
    nominal_interest = get_nominal_interest(interest)
    principal = payment / (
            (nominal_interest * pow(1 + nominal_interest, periods)) / (pow(1 + nominal_interest, periods) - 1))
    print(f'Your credit principal = {round(principal)}!')
    arg_dict['principal'] = round(principal)


def get_overpayment_annuity(payment, periods, principal, **kwargs):
    total_payment = payment * periods
    over_payment = total_payment - principal
    return round(over_payment)

def valid_args(arg_dict):
    if not arg_dict['type'] or arg_dict['type'] not in ('diff', 'annuity') or len(sys.argv) < 5:
        print('Incorrect parameters.')
        return False

    for arg, value in arg_dict.items():
        if not value:
            continue
        if arg in ['principal', 'periods', 'interest', 'payment']:
            try:
                arg_dict[arg] = float(value)
                if arg_dict[arg] < 0:
                    print('Incorrect parameters')
                    return False
            except ValueError:
                print('Incorrect parameters')
                return False
    return True

def diff_calc(periods, principal, interest, **kwargs):
    total_payment = 0
    for i in range(1, int(periods) + 1):
        payment_n = (principal / periods) + (get_nominal_interest(interest) * (principal - (principal * (i - 1) / periods)))
        total_payment += math.ceil(payment_n)
        print(f'Month {i}: payment is {math.ceil(payment_n)}')
    print(f'\nOverpayment = {math.ceil(total_payment - principal)}')

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('--type')
    parser.add_argument('--principal')
    parser.add_argument('--periods')
    parser.add_argument('--interest')
    parser.add_argument('--payment')

    args = parser.parse_args()
    global arg_dict 
    arg_dict = vars(args)
    if not valid_args(arg_dict):
        return 1

    required_arg = [arg for arg in arg_dict.keys() if not arg_dict[arg]][0]
    arg_dict.pop(required_arg)
    annuity_funcs = {'principal': get_principal, 'periods': get_payments_duration, 'payment':get_annuity_payment}

    if arg_dict.pop('type') == 'annuity':
        annuity_funcs[required_arg](**arg_dict)
        print((f'Overpayment = {get_overpayment_annuity(**arg_dict)}'))
    else:
        diff_calc(**arg_dict)

main()
