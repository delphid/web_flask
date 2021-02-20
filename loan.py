from chart import bar_plot, layout

class Loan:
    def __init__(self, loan_amount, yearly_interest_rate, year_limit):
        '''money unit:
        loan_amount: in yuan
        self.loan_amount and all, until output: in cent
        '''
        self.loan_amount = loan_amount * 100
        self.remain = self.loan_amount
        self.yearly_interest_rate = yearly_interest_rate
        self.interest_rate = self.yearly_interest_rate / 12
        self.year_limit = year_limit
        self.p_num = year_limit * 12  # num of periods

        self.p1_interest = self.loan_amount * self.interest_rate

    @property
    def p1_principal_trial_range(self):
        range_min = int(self.p1_interest * 10)
        range_max = int(self.p1_interest * 30)
        return [range_min, range_max]

    def equal_principal_interest(self):
        p1_principal = self.p1_interest * 19.59
        actual_p_num= self.actual_p_num(p1_principal)

    def actual_p_num(self, p1_principal):
        principal_interest = p1_principal + self.p1_interest
        self.remain = self.loan_amount - p1_principal
        p_num = 1
        while True:
            if self.remain <= 0:
                break
            interest = self.remain * self.interest_rate
            principal = principal_interest - interest
            self.remain -= principal
            p_num += 1
        print('finish one calc')
        print(p_num, round(self.remain / 100, 2))
        return p_num

    def plot(self):
        p1_principals = []
        remains = []
        p_nums = []
        for p1_principal in range(
            self.p1_principal_trial_range[0],
            self.p1_principal_trial_range[1] + 1):

            p1_principals.append(round(p1_principal / 100, 2))
            p_num = self.actual_p_num(p1_principal)
            p_nums.append(p_num)
            remains.append(round(self.remain / 100, 2))
        layout(
            bar_plot(p1_principals, remains),
            bar_plot(p1_principals, p_nums)
        )

    def find_min(x_range, func):
        # ex: x_range = [1, 8]
        self.plot(self.p1_principal_trial_range, self.actual_p_num)


if __name__ == '__main__':
    loan = Loan(
        loan_amount = 10000,
        yearly_interest_rate = 0.05,
        year_limit = 1)
    loan.equal_principal_interest()
    loan.plot()
