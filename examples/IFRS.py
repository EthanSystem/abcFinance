# -*- coding: utf-8 -*-
"""
Created on Wed May  2 15:23:48 2018

This file demonstrates how a generic IFRS-style balance sheet and profit and loss statement can be implemented in abcFinance

@author: christoph

国际财务报告准则
"""

from abcFinance import Ledger, Account, AccountSide

corporation = Ledger(residual_account_name='Retained earnings')
bank = Ledger(residual_account_name='Retained earnings')

corporation.make_asset_accounts([
        # Non-current assets
        'Property, plant and equipment',
        'Investment properties',
        'Intangible assets',
        'Deferred tax assets',
        'At-equity-accounted investments',
        'Held-to-maturity investments',
        'Available-for-sale financial assets',
        # Current assets
        'Inventories',
        'Receivables',
        'Derivative financial instruments assets',
        'Financial assets at fair value through profit or loss',
        'Cash and cash equivalents',
        'Assets classified as held for sale',
        ])

corporation.make_liability_accounts([
        # Non-current liabilities
        'Borrowings',
        'Deferred tax liabilities',
        'Employee benefit obligations',
        'Provisions',
        # Current liabilities
        'Payables',
        'Current tax liabilities',
        'Derivative financial instruments liabilities',
        'Deferred revenue',
        'Liabilities associated with assets classified as held for sale',
        # Equity
        'Share capital'
        ])

corporation.make_flow_accounts([
        # Continuing operations
        'Revenue',
        'Cost of goods sold',
        'Cost of services provided',
        # = Gross profit
        'Depreciation and amortisation',
        'Administrative expenses',
        'Other income',
        'Other gains/losses',
        # = Operationg profit
        'Finance income',
        'Finance costs',
        'Net income from at-equity investments',
        # = Profit before income tax
        'Income tax expense',
        # = Profit from continuing operations
        'Net income from discontinued operations'
        # Profit for the period
        ])

bank.make_asset_accounts([
        # Assets
        'Cash and central bank reserves',
        'Loans and advances to banks',
        'Loans and advances to customers',
        'Central bank funds sold and securities purchased under resale agreements',
        'Securities borrowed',
        'FV through PnL assets - Trading assets',
        'FV through PnL assets - Positive market values from derivatives',
        'FV through PnL assets - Financial assets',
        'Financial assets available for sale',
        'At-equity-accounted investments',
        'Held-to-maturity investments',
        'Property, plant and equipment',
        'Goodwill and other intangible assets',
        'Deferred tax assets',
        'Other assets',
        ])

bank.make_liability_accounts([
        # Liabilities
        'Deposits from customers',
        'Deposits from banks',
        'Central bank funds purchased and securities sold under repurchase agreements',
        'Securities loaned',
        'FV through PnL liabilities - Trading liabilities',
        'FV through PnL liabilities - Negative market values from derivatives',
        'FV through PnL liabilities - Financial liabilities',
        'FV through PnL liabilities - Investment contract liabilities',
        'Other short-term borrowings',
        'Provisions',
        'Deferred tax liabilities',
        'Long-term debt',
        'Other liabilities',
        # Equity
        'Share capital'
        ])

bank.make_flow_accounts([
        'Interest income',
        'Interest expenses',
        'Fee and commission income',
        'Fee and commission expenses',
        'Trading income',
        'Trading expenses',
        'Net income from financial instruments at fair value through profit or loss',
        'Net income from financial assets available for sale',
        'Net income from at-equity investments',
        'Other operating income',
        'Other operating expenses',
        # = Operating result
        'Compensation and benefits',
        'Administrative expenses',
        'Impairment of goodwill',
        'Depreciation and amortisation',
        'New provisions',
        'Impairments',
        # = Profit before taxes
        'Income tax expense'
        # = Profit from continuing operations
        'Net income from discontinued operations'
        # Profit for the period
        ])
