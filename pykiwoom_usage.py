from pykiwoom.kiwoom import *
import time
import pandas as pd

#####로그인#####

kiwoom = Kiwoom()
kiwoom.CommConnect(block=True)

#####사용자 정보 얻기#####
def userInfo():
    account_num = kiwoom.GetLoginInfo("ACCOUNT_CNT")        # 전체 계좌수
    accounts = kiwoom.GetLoginInfo("ACCNO")                 # 전체 계좌 리스트
    user_id = kiwoom.GetLoginInfo("USER_ID")                # 사용자 ID
    user_name = kiwoom.GetLoginInfo("USER_NAME")            # 사용자명
    keyboard = kiwoom.GetLoginInfo("KEY_BSECGB")            # 키보드보안 해지여부
    firewall = kiwoom.GetLoginInfo("FIREW_SECGB")           # 방화벽 설정 여부
    print(account_num)
    print(accounts)
    print(user_id)
    print(user_name)
    print(keyboard)
    print(firewall)

#####종목 코드 얻기#####
def getCode():
    kospi = kiwoom.GetCodeListByMarket('0')
    kosdaq = kiwoom.GetCodeListByMarket('10')
    etf = kiwoom.GetCodeListByMarket('8')

    print(len(kospi))
    print(len(kosdaq))
    print(len(etf))

#####종목 이름#####

def getName():
    name = kiwoom.GetMasterCodeName("005930")
    print(name)

    감리구분 = kiwoom.GetMasterConstruction("005930")
    print(감리구분)

    전일가 = kiwoom.GetMasterLastPrice("005930")
    print(int(전일가))
    print(type(전일가))

#####테마그룹명과 id값#####
# import pprint
def theme():
    group = kiwoom.GetThemeGroupList(1)
    pprint.pprint(group)

    tickers = kiwoom.GetThemeGroupCode('850')
    for ticker in tickers:
        name = kiwoom.GetMasterCodeName(ticker)
        print(ticker, name)

#####매수, 매도: 삼성전자, 10주, 시장가주문 매수#####
def buy():
    accounts = kiwoom.GetLoginInfo("ACCNO")
    stock_account = accounts[0]
    
    kiwoom.SendOrder("시장가매수", "0101", stock_account, 1, "005930", 10, 0, "03", "")

def sell():
    accounts = kiwoom.GetLoginInfo("ACCNO")
    stock_account = accounts[0]
    kiwoom.SendOrder("시장가매도", "0101", stock_account, 2, "005930", 10, 0, "03", "")


def stockInfo():
    df = kiwoom.block_request("opt10001",
                              종목코드="005930",
                              output="주식기본정보",
                              next=0)
    print(df)

def dailyPrice():
    dfs=[]
    df = kiwoom.block_request("opt10081",
                          종목코드="005930",
                          기준일자="20200424",
                          수정주가구분=1,
                          output="주식일봉차트조회",
                          next=0)
    print(df.head())
    dfs.append(df)

    while kiwoom.tr_remained:
        df = kiwoom.block_request("opt10081",
                                      종목코드="005930",
                                  기준일자="20200424",
                                  수정주가구분=1,
                                  output="주식일봉차트조회",
                                  next=2)
        dfs.append(df)
        time.sleep(1)

    df = pd.concat(dfs)
    df.to_excel("005930.xlsx")

dailyPrice()