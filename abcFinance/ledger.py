""" abcFinance is an implementation of a double entry book keeping system

Initialize the accounting system with, the name of the residual_account::

    accounts = Ledger(residual_account_name='equity')

Create stock and flow account:

    accounts.make_stock_account(['cash', 'claims'])
    accounts.make_flow_account(['expenditure'])

In order to book give a list of credit and debit tuples. Each tuple should be
an account and a value::

    accounts.book(
        debit=[('cash', 50), ('claims', 50)],
        credit=[('equity', 100)])

get balance gives you the balance of an account:

    assert accounts['cash'].get_balance() == (AccountSide.DEBIT, 50)

Example::

    accounts.book(debit=[('expenditure', 20)], credit=[('cash', 20)])

    assert accounts.get_total_assets() == 80, accounts.get_total_assets()

    accounts.print_profit_and_loss()
    print('--')
    accounts.make_end_of_period()

    accounts.print_profit_and_loss()

    accounts.print_balance_sheet()

    assert accounts['equity'].get_balance() == (AccountSide.CREDIT, 80)


"""

from .account import Account, AccountSide
from .svg_tools import Scene, Text, Textbox


class Ledger:
    """ The main class to be initialized """

    def __init__(self, residual_account_name='equity'):
        self.stock_accounts = {}
        self.flow_accounts = {}
        self.accounts = {}
        self.asset_accounts = {}
        self.liability_accounts = {}
        self.residual_account = None
        self.profit_history = []
        self.booking_history = []
        self.residual_account_name = residual_account_name
        self._make_residual_account(residual_account_name)

    def __getitem__(self, item):
        return self.accounts[item]

    def make_stock_accounts(self, names):
        """ Create stock accounts.

        Args:
            names, list of names for the accounts
        """
        for name in names:
            assert name not in self.accounts
            account = Account()
            self.stock_accounts[name] = account
            self.accounts[name] = account

    def make_asset_accounts(self, names):
        """ Create stock accounts. #BUG注释错误，后续的也是这样。

        Args:
            names, list of names for the accounts
        """
        for name in names:
            assert name not in self.accounts
            account = Account()
            self.asset_accounts[name] = account
            self.stock_accounts[name] = account
            self.accounts[name] = account

    def make_liability_accounts(self, names):
        """ Create stock accounts.

        Args:
            names, list of names for the accounts
        """
        for name in names:
            assert name not in self.accounts
            account = Account()
            self.liability_accounts[name] = account
            self.stock_accounts[name] = account
            self.accounts[name] = account

    def make_flow_accounts(self, names):
        """ Create flow accounts.

        Args:
            names, list of names for the accounts
        """
        for name in names:
            assert name not in self.accounts
            account = Account()
            self.flow_accounts[name] = account
            self.accounts[name] = account

    def _make_residual_account(self, name):
        assert name not in self.accounts
        account = Account()
        self.stock_accounts[name] = account
        self.accounts[name] = account
        self.residual_account = account

    def book(self, debit, credit, text=""):
        """ Book a transaction.  记录一笔明细

        Arguments:
            debit, list of tuples ('account', amount)

            credit, list of tuples ('account', amount)

            text, for booking history

        Example::

            accounts.book(debit=[('inventory', 20)],
                          credit=[('cash', 20)],
                          text="Purchase of equipment")
        """
        sum_debit = 0
        sum_credit = 0

        for name, value in debit:
            account = self.accounts[name]  # 获取科目名
            account.debit += value  # 借方累加
            if name in self.asset_accounts:  # 记录资产负债表所在边
                side, _ = account.get_balance()
                assert side != AccountSide.CREDIT
            elif name in self.liability_accounts:
                side, _ = account.get_balance()
                assert side != AccountSide.DEBIT
            sum_debit += value

        for name, value in credit:
            assert value >= 0
            account = self.accounts[name]
            account.credit += value  # 贷方累加
            if name in self.asset_accounts:
                side, _ = account.get_balance()
                assert side != AccountSide.CREDIT
            elif name in self.liability_accounts:
                side, _ = account.get_balance()
                assert side != AccountSide.DEBIT
            sum_credit += value  # 累加贷方

        assert sum_debit == sum_credit

        self.booking_history.append((debit, credit, text))

    def book_end_of_period(self):
        """ Close flow accounts and credit/debit residual (equity) account 结转当期流量、借贷账户于期末 """
        profit = 0
        debit_accounts = []
        credit_accounts = []
        for name, account in self.flow_accounts.items():
            side, balance = account.get_balance()
            if balance > 0:
                if side == AccountSide.DEBIT:  # 如果余额出现在借方，则说明损失，因此收益减少其余额量，反之亦然
                    profit -= balance
                    credit_accounts.append((name, balance))  # 贷方账户追加一笔余额
                else:
                    profit += balance
                    debit_accounts.append((name, balance))

        if profit > 0:
            credit_accounts.append((self.residual_account_name, profit))
        else:
            debit_accounts.append((self.residual_account_name, -profit))

        self.book(debit=debit_accounts,
                  credit=credit_accounts, text='Period close')
        self.profit_history.append((debit_accounts, credit_accounts))

        for account in self.flow_accounts:
            account = Account()

    def print_balance_sheet(self, show_empty_accounts=False):
        """ Print a balance sheets """
        print('Asset accounts:')
        total_assets = 0
        equity = 0
        for name, account in self.stock_accounts.items():
            side, balance = account.get_balance()
            if side == AccountSide.DEBIT or (side == AccountSide.BALANCED and name in self.asset_accounts):
                if name == self.residual_account_name:
                    equity = -balance
                else:
                    total_assets += balance
                    if balance != 0 or show_empty_accounts:
                        print("  ", name, ":", balance)
        print('Liability accounts:')
        for name, account in self.stock_accounts.items():
            side, balance = account.get_balance()
            if side == AccountSide.CREDIT or (side == AccountSide.BALANCED and name in self.liability_accounts):
                if name == self.residual_account_name:
                    equity = balance
                else:
                    if balance != 0 or show_empty_accounts:
                        print("  ", name, ":", balance)
        print('Equity: ', equity)
        print('Total Assets: ', total_assets)
        print('--')

    def print_profit_and_loss(self, show_empty_accounts=False):
        """ Print profit and loss statement """
        profit = 0
        print('Flow accounts:')
        for name, account in self.flow_accounts.items():
            side, balance = account.get_balance()
            if balance != 0 or show_empty_accounts:
                if side == AccountSide.DEBIT:
                    print("  ", name, ":", -balance)
                    profit -= balance
                else:
                    print("  ", name, ":", balance)
                    profit += balance
        print("Profit for period: ", profit)
        capital_actions = False
        for booking_statement in reversed(self.booking_history):
            debit, credit, text = booking_statement
            if text == "Period close":
                break
            for account, value in debit:
                if account == self.residual_account_name:
                    if not capital_actions:
                        print("Profit distribution and capital actions")
                        capital_actions = True
                    print("  ", text, ":", -value)
            for account, value in credit:
                if account == self.residual_account_name:
                    if not capital_actions:
                        print("Profit distribution and capital actions")
                        capital_actions = True
                    print(text, ":", value)
        print('--')

    def get_balance(self, account):
        return self.accounts[account].get_balance()

    def get_total_assets(self):
        """ Return total assets. """
        total_assets = 0
        for account in self.stock_accounts.values():
            side, balance = account.get_balance()
            if side == AccountSide.DEBIT:
                total_assets += balance
        return total_assets

    def _check_debit_eq_credit(self):
        debitsum = 0
        creditsum = 0
        for account in self.accounts.values():
            debitsum += account.debit
            creditsum += account.credit
        return debitsum == creditsum

    def draw_balance_sheet(self, title="Balance Sheet", height=None, width=350, write_file=False):
        """
        可视化资产负债表
        """
        total_assets = 0
        asset_accounts = list()
        liability_accounts = list()
        for name, account in self.stock_accounts.items():
            side, balance = account.get_balance()
            if side == AccountSide.DEBIT:
                total_assets += balance
                if balance != 0:
                    if name == self.residual_account_name:
                        asset_accounts.append(("Neg. Equity", balance))
                    else:
                        asset_accounts.append((name, balance))
            elif side == AccountSide.CREDIT:
                if balance != 0:
                    liability_accounts.append((name, balance))

        box_width = width//2
        if height is None:
            height = int(total_assets*0.8)
        plot = Scene(height=height+30, width=width+10)
        plot.add(Text(origin=(box_width, 0), text=title,
                 size=19, align_vertical="hanging"))
        left_corner = (5, 25)
        for name, balance in asset_accounts:
            if name == "Neg. Equity":
                plot.add(Textbox(left_corner, int(height*(balance/total_assets)), box_width,
                                 name + " " + str(int(balance)),
                                 color=(255, 102, 102)))
            else:
                plot.add(Textbox(left_corner, int(height*(balance/total_assets)), box_width,
                                 name + " " + str(int(balance)),
                                 color=(153, 204, 255)))
            left_corner = (5, left_corner[1] +
                           int(height*(balance/total_assets)))

        left_corner = (box_width+5, 25)
        for name, balance in liability_accounts:
            if name == self.residual_account_name:
                plot.add(Textbox(left_corner, int(height*(balance/total_assets)), box_width,
                                 name + " " + str(int(balance)),
                                 color=(204, 255, 204)))
            else:
                plot.add(Textbox(left_corner, int(height*(balance/total_assets)), box_width,
                                 name + " " + str(int(balance)),
                                 color=(255, 204, 204)))
            left_corner = (
                box_width+5, left_corner[1] + int(height*(balance/total_assets)))

        if write_file:
            plot.write_svg()

        return ' '.join(plot.strarray())
