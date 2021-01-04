import sys
from PyQt5.QtWidgets import *
from PyQt5.QAxContainer import *
from PyQt5.QtCore import *


class Kiwoom(QAxWidget):  # QAxWidget 클래스로부터 dynamicCall, setControl, OnEventConnect 를 상속받음
    def __init__(self):
        super().__init__()
        self._create_kiwoom_instance()  # 키움증권 OpenAPI 를 정상적으로 사용할 수 있도록 처리함
        self._set_signal_slots()        # 이벤트 처리메소드 등록

    def _create_kiwoom_instance(self):
        self.setControl("KHOPENAPI.KHOpenAPICtrl.1")      # 이거 대신 obj = QAxWidget("KHOPENAPI.KHOpenAPICtrl.1") 가능

    def _set_signal_slots(self):
        self.OnEventConnect.connect(self._event_connect)  # 콜백함수 등록

    def _event_connect(self, err_code):
        if err_code == 0:
            print("로그인 성공")
        else:
            print("로그인 에러코드 : " + str(err_code))

        self.login_event_loop.exit()

    def comm_connect(self):
        self.dynamicCall("CommConnect()")    # 로그인창 띄우기
        self.login_event_loop = QEventLoop() # 이벤트 루프 생성
        self.login_event_loop.exec_()        # 프로그램 흐름을 일시중지하고 이벤트만 처리할 수 있는 상태로 만듬

    def get_all_codes_names(self):
        ret = self.dynamicCall("GetCodeListByMarket(QString)", ["0"])  # 맨뒤 인자는 시장구분, 모든 코드들을 가져옴
        kospi_code_list = ret.split(';')
        kospi_code_name_list = []

        for code in kospi_code_list:
            name = self.dynamicCall("GetMasterCodeName(QString)", [code])  # 맨뒤는 종목코드, 코드에 따른 종목명을 가져옴
            kospi_code_name_list.append(code + " : " + name)

        for item in kospi_code_name_list:
            print(item)

    def get_code_list_by_market(self, market):
        code_list = self.dynamicCall("GetCodeListByMarket(QString)", market)
        code_list = code_list.split(';')
        return code_list[:-1]

    def get_master_code_name(self, code):
        code_name = self.dynamicCall("GetMasterCodeName(QString)", code)
        return code_name

if __name__ == "__main__":
    '''
    Kiwoom 클래스는 QAxWidget 클래스를 상속받았기 때문에
    Kiwoom 클래스에 대한 인스턴스를 생성하려면 먼저 QApplication 클래스의 인스턴스를 생성해야함
    '''
    app = QApplication(sys.argv)
    kiwoom = Kiwoom()
    kiwoom.comm_connect()
#    kiwoom.get_all_codes_names()
    print(kiwoom.get_master_code_name("000660"))
#    code_list = kiwoom.get_code_list_by_market('10')
#    for code in code_list:
#        print(code, end=" ")
#    sys.exit(app.exec_())


#삼성전자 주가 차트그리기
'''
import pandas_datareader.data as web
import datetime
start = datetime.date(2020, 12, 19)
end = datetime.datetime(2020, 12, 30)
#gs = web.DataReader("078930.KS", "yahoo", start, end)
samsung = web.DataReader("005930.KS", "yahoo")
print(samsung.index)

import matplotlib.pyplot as plt
plt.plot(samsung['Adj Close'])
plt.show()
'''