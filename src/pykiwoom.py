from PyQt5.QAxContainer import *


class Kiwoom:
    def __init__(self):
        self.ocx = QAxWidget("KHOPENAPI.KHOpenAPICtrl.1")
        self.ocx.OnEventConnect.connect(self._handler_login)
        self.callbacks = {
            "login" : None
        }

    def CommConnect(self, fn = None):
        self.ocx.dynamicCall("CommConnect()")
        if callable(fn):      # callback 함수가 있다면 등록
            self.callbacks['login'] = fn

    def _handler_login(self, err_code):
        fn = self.callbacks['login']
        if callable(fn):      # callback 함수가 있다면 호출
            fn(err_code=err_code)