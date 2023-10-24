import math
import argparse
import numbers


def monthly_interest(percentual_annual_interest):
    return percentual_annual_interest / (12 * 100)


def periods_interest_coefficient(periods, percentual_annual_interest):
    interest = monthly_interest(percentual_annual_interest)
    return ((interest * (1 + interest) ** periods)
            / (((1 + interest) ** periods) - 1))


def calculate_periods(principal, payment, percentual_annual_interest):
    interest = monthly_interest(percentual_annual_interest)
    return math.ceil(math.log(payment / (payment - (interest * principal)), 1 + interest))


def calculate_principal(periods, payment, percentual_annual_interest):
    return math.ceil(payment / periods_interest_coefficient(periods, percentual_annual_interest))


def calculate_payment(principal, periods, percentual_annual_interest):
    return math.ceil(principal * periods_interest_coefficient(periods, percentual_annual_interest))


def calculate_overpayment(principal, periods, payment):
    return (periods * payment) - principal


def differentiated_payment(principal, periods, percentual_annual_interest):
    interest = monthly_interest(percentual_annual_interest)
    differentiated_payments = []
    for i in range(periods):
        differentiated_payments.append(
            math.ceil(
                (principal / periods) + interest *
                (principal - ((principal * i) / periods))))

    return differentiated_payments


def remaining_periods_message(period):
    years = math.trunc(period / 12)
    months = period % 12
    years_text = ""
    months_text = ""
    period_text = ""
    if years > 0:
        years_text = f"{years} year" if years == 1 else f"{years} years"
        period_text = years_text

    if months > 0:
        months_text = f"{months} month" if months == 1 else f"{months} months"
        period_text = months_text

    if years > 0 and months > 0:
        period_text = years_text + " and " + months_text

    return "It will take " + period_text + " to repay this loan!"


def loan_principal_message(periods, payment, percentual_annual_interest):
    principal = calculate_principal(periods, payment, percentual_annual_interest)
    return f"Your loan principal = {principal}!"


def has_incorrect_values(args):
    args_dict = vars(args)
    num_args = sum(value is not None for value in args_dict.values())
    any_negative = any(value < 0 for value in args_dict.values()
                       if isinstance(value, numbers.Number) and value is not None)

    if num_args != 4 or any_negative:
        return True
    elif (args.type is None
            or args.interest is None
            or (args.type != "diff" and args.type != "annuity")):
        return True
    elif (args.type == "diff"
            and args.payment is not None):
        return True
    else:
        return False



parser = argparse.ArgumentParser(description="This program calculate /"
                                             "annuity payments of a loan")

parser.add_argument("-pay", "--payment", type=float)
parser.add_argument("-pri", "--principal", type=float)
parser.add_argument("-per", "--periods", type=int)
parser.add_argument("-int", "--interest", type=float)
parser.add_argument("-t", "--type")

args = parser.parse_args()


if has_incorrect_values(args):
    print("Incorrect Parameters")
else:
    overpayment = 0
    if args.type == "diff":
        payments = differentiated_payment(args.principal, args.periods, args.interest)
        for index, value in enumerate(payments):
            print(f"Month {index + 1}: payment is {value}")
        overpayment = sum(payments) - args.principal
    elif args.type == "annuity":
        if args.periods is None:
            period = calculate_periods(args.principal, args.payment, args.interest)
            overpayment = calculate_overpayment(args.principal, period, args.payment)
            print(remaining_periods_message(period))
        elif args.payment is None:
            payment = calculate_payment(args.principal, args.periods, args.interest)
            overpayment = calculate_overpayment(args.principal, args.periods, payment)
            print(f"Your monthly payment = {payment}!")
        elif args.principal is None:
            principal = calculate_principal(args.periods, args.payment, args.interest)
            overpayment = calculate_overpayment(principal, args.periods, args.payment)
            print(f"Your loan principal = {principal}!")
    print("Overpayment = ", overpayment)

