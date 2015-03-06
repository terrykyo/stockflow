#!/bin/python
# -*- coding: utf-8 -*-

import sys
from ctrls import *
from datetime import date
from models.exampleModel import exampleModel

def main():

    drawer = CandleDrawer()

    number_list = [ line.strip() for line in open('stocknumber.csv', 'rb') ]

    this_year = str(date.today().year-1911)

    for number in number_list:

        model = exampleModel()
        reader = Reader(number)

        trader = Trader(model.infos, number)#參數是Model Description 和 number
        last_row = None

        while True:
            
            row = reader.getInput()
            if row == None: break
            last_row = row

            model.update(row)
            prediction = model.predict()
            
            data_year = row[0].split('/')[0]
            if data_year == this_year:
                trade = trader.do(float(row[6]), prediction)

        result = trader.analysis()

        # 預測為要買，而且今年為止 ROI 為正
        if prediction > 0:
            print last_row[0], number, ' @ ', float(last_row[6]), '該買囉, 今年累計：', result["ROI"], '%'
            drawer.draw(number)

if __name__ == '__main__':
    sys.exit(main())