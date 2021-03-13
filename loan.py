from functools import cached_property

from pydantic import BaseModel

from chart import line_plot, layout


class Loan:
    def __init__(self, loan_amount_yuan, yearly_interest_rate, year_limit):
        '''money unit:
        loan_amount: in yuan
        self.loan_amount and all, until output: in cent
        '''
        self.loan_amount_yuan = loan_amount_yuan
        self.yearly_interest_rate = yearly_interest_rate
        self.year_limit = year_limit

    @property
    def loan_amount(self):
        return self.loan_amount_yuan * 100

    @property
    def ir(self):
        # period interest rate
        return self.yearly_interest_rate / 12

    @property
    def p_num(self):
        # num of periods
        return self.year_limit * 12

    @property
    def practice_principal_interest(self):
        # in industrial practice, in const principal-interest mode,
        # this calculates the period payment
        value =\
            self.loan_amount * (
                self.ir * (1 + self.ir) ** self.p_num
            ) / (
                (1 + self.ir) ** self.p_num - 1
            )
        return round(value)

    def const_pi(self):
        # constant-principal-interest mode
        pi = self.practice_principal_interest
        self.principal_interest = pi
        self.remain = self.loan_amount
        principals = []
        interests = []
        for period in range(1, self.p_num + 1):
            interest = round(self.remain * self.ir)
            interests.append(interest)
            if period == self.p_num:
                principal = self.remain
            else:
                principal = pi - interest
            principals.append(principal)
            self.remain -= principal
        self.const_pi_principals = principals
        self.const_pi_interests = interests

    def const_p(self):
        # constant-principal mode
        self.remain = self.loan_amount
        principal = round(self.loan_amount / self.p_num)
        last_principal = self.loan_amount - (self.p_num - 1) * principal
        principals = [principal for i in range(self.p_num)]
        principals[-1] = last_principal
        interests = []
        for principal in principals:
            interest = self.remain * self.ir
            interests.append(interest)
            self.remain -= principal
        self.const_p_principals = principals
        self.const_p_interests = interests

    def calc_plot_values(self):
        self.const_pi()
        self.const_p()
        self.plot_values = yuan([
            self.const_pi_principals,
            self.const_pi_interests,
            self.const_p_principals,
            self.const_p_interests
        ])
        return self.plot_values

    def plot(self):
        plot_loan = PlotLoan(
            p_num=self.p_num,
            values_lists=self.calc_plot_values())
        return plot_loan.plot()


class PlotLoan(BaseModel):
    p_num: int
    values_lists: list

    def plot(self):
        periods = [p for p in range(1, self.p_num + 1)]
        line_result = line_plot(
            x=periods,
            y_values=self.values_lists,
            y_names=[
                '等额本息还款 - 本金曲线',
                '等额本息还款 - 利息曲线',
                '等额本金还款 - 本金曲线',
                '等额本金还款 - 利息曲线'
            ]
        )
        layout(line_result)
        return line_result


def yuan(in_cent):
    if isinstance(in_cent, list):
        return [yuan(item) for item in in_cent]
    out = round(in_cent / 100, 2)
    return out


if __name__ == '__main__':
    loan = Loan(
        loan_amount_yuan = 100000,
        yearly_interest_rate = 0.2,
        year_limit = 50)
    print(loan.practice_principal_interest)
    loan.plot()
