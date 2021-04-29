import sys
from argparse import ArgumentParser
from math import log, ceil


def get_periods(principal, payment, interest):
    nominal_rate = interest / (12 * 100)
    x = payment / (payment - nominal_rate * principal)
    periods = ceil(log(x, 1 + nominal_rate))
    num_years, rem_months = divmod(periods, 12)
    y_suffix = ''
    m_suffix = ''
    if num_years > 1:
        y_suffix = 's'
    if rem_months > 1:
        m_suffix = 's'
    if rem_months > 0:
        print(f'It will take {num_years} year{y_suffix} and {rem_months} month{m_suffix} to repay this loan!')
    else:
        print(f'It will take {num_years} year{y_suffix} to repay this loan!')

    total = payment * periods
    print(f'Overpayment = {int(total - principal)}')


def get_payment(principal, periods, interest):
    nominal_rate = interest / (12 * 100)
    nominator = nominal_rate * ((1 + nominal_rate) ** periods)
    dominator = ((1 + nominal_rate) ** periods) - 1
    payment = ceil(principal * (nominator / dominator))
    print(f'Your monthly payment = {payment}!')

    total = payment * periods
    print(f'Overpayment = {int(total - principal)}')


def get_principal(payment, periods, interest):
    nominal_rate = interest / (12 * 100)
    nominator = nominal_rate * ((1 + nominal_rate) ** periods)
    dominator = ((1 + nominal_rate) ** periods) - 1
    principal = ceil(payment / (nominator / dominator))
    print(f'Your loan principal = {principal}!')

    total = payment * periods
    print(f'Overpayment = {int(total - principal)}')


def get_args_dict():
    parser = ArgumentParser()
    parser.add_argument('--type')
    parser.add_argument('--principal', type=float)
    parser.add_argument('--periods', type=int)
    parser.add_argument('--interest', type=float)
    parser.add_argument('--payment', type=float)
    args = parser.parse_args()
    return {'type': args.type, 'principal': args.principal, 'periods': args.periods,
            'interest': args.interest, 'payment': args.payment}


def check_args(args):
    if args['type'] != 'diff' and args['type'] != 'annuity':
        return False
    if args['type'] == 'diff' and args['payment'] is not None:
        return False
    if args['interest'] is None:
        return False
    if len(sys.argv) < 5:
        return False

    integer_args = [args['principal'], args['periods'], args['interest'], args['payment']]
    for arg in integer_args:
        if arg is not None and arg < 0:
            return False

    return True


def annuity_calc(args):
    required = None
    functions = {'payment': get_payment, 'principal': get_principal, 'periods': get_periods}
    for arg, value in args.items():
        if value is None:
            required = arg

    args.pop('type')
    args.pop(required)
    functions[required](**args)


def diff_calc(principal, periods, interest):
    total = 0
    i = interest / 1200
    for m in range(1, periods+1):
        payment = ceil((principal / periods) + i * (principal - ((principal * (m - 1)) / periods)))
        total += payment
        print(f'Month {m}: payment is {payment}')

    print(f'\nOverpayment = {int(total - principal)}')


def main():
    args = get_args_dict()
    args_okay = check_args(args)

    if not args_okay:
        print('Incorrect parameters')
        return

    if args['type'] == 'annuity':
        annuity_calc(args)
    else:
        args.pop('type')
        args.pop('payment')
        diff_calc(**args)

if __name__ == '__main__':
    main()

