from functools import cached_property

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
    def p1_interest(self):
        # interest of the 1st period
        return self.loan_amount * self.ir

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
        # pi = self.calc_principal_interest()
        pi = self.practice_principal_interest
        self.principal_interest = pi
        self.remain = self.loan_amount
        principals = []
        interests = []
        for period in range(1, self.p_num + 1):
            interest = round(self.remain * self.ir)
            interests.append(yuan(interest))
            if period == self.p_num:
                principal = self.remain
            else:
                principal = pi - interest
            principals.append(yuan(principal))
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
            interests.append(yuan(interest))
            self.remain -= principal
        self.const_p_principals = [yuan(principal) for principal in principals]
        self.const_p_interests = interests

    def calc_p1_principal_trial_range(self):
        p1_principal = self.loan_amount / self.p_num
        for i in range(self.p_num):
            p1_principal =\
                self.loan_amount / self.p_num * (
                    (self.p_num - i) / self.p_num
                )
            actual_p_num = self.actual_p_num(p1_principal)
            if actual_p_num == self.p_num - 1:
                range_max = p1_principal
            if actual_p_num == self.p_num:
                range_min = p1_principal
                break
        return [range_min, range_max]

    def calc_principal_interest(self):
        self.p1_principal_trial_range = self.calc_p1_principal_trial_range()
        p1p_min = self.p1_principal_trial_range[0]
        p1p_max = self.p1_principal_trial_range[1]
        boundary_p1ps = find_boundary(
            leftx=p1p_min,
            rightx=p1p_max,
            lefty=self.p_num,
            righty=self.p_num - 1,
            func=self.actual_p_num)
        principal_interest = round(self.p1_interest + boundary_p1ps[0])
        return round(principal_interest)

    def actual_p_num(self, p1_principal):
        principal_interest = p1_principal + self.p1_interest
        self.remain = self.loan_amount - p1_principal
        p_num = 1
        while True:
            interest = self.remain * self.ir
            principal = principal_interest - interest
            if self.remain - principal <= 0:
                break
            self.remain -= principal
            p_num += 1
        return p_num

    def plot(self):
        periods = [p for p in range(1, self.p_num + 1)]
        self.const_pi()
        self.const_p()
        line_result = line_plot(
            periods, [
                [self.const_pi_principals, 'const pi principals'],
                [self.const_pi_interests, 'const pi interests'],
                [self.const_p_principals, 'const p principals'],
                [self.const_p_interests, 'const p interests']
            ]
        )
        layout(line_result)
        return line_result


def find_boundary(leftx, rightx, lefty, righty, func):
    while True:
        if rightx - leftx <= 0.01:
            return [leftx, rightx]
            break
        x = (leftx + rightx) / 2
        if func(x) == lefty:
            leftx = x
        elif func(x) == righty:
            rightx = x


def yuan(in_cent):
    out = round(in_cent / 100, 2)
    return out


if __name__ == '__main__':
    loan = Loan(
        loan_amount_yuan = 900000,
        yearly_interest_rate = 0.04275002016749706,
        year_limit = 5)
    print(loan.practice_principal_interest)
    loan.plot()
