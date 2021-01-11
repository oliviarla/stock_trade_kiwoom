from pykiwoom_usage import *

def momentumCalc():
    #dailyPriceAll()
    #mergeAll()
    df = pd.read_excel("merge.xlsx")

    #pandas에서 사용하기 쉽게 datetime타입으로 변환
    df['일자'] = pd.to_datetime(df['일자'], format="%Y%m%d")
    df = df.set_index('일자')

    #3개월 가격 모멘텀 -> 60일전 종가와 오늘 종가 사이의 수익률 계산
    return_df = df.pct_change(60)
    #return_df.tail()

    # 데이터 프레임으로 만들기
    s = return_df.loc["2021-01-11"]
    momentum_df = pd.DataFrame(s)
    momentum_df.columns = ["모멘텀"]

    momentum_df['순위'] = momentum_df['모멘텀'].rank(ascending=False)
    #momentum_df.head(n=10)

    #3개월 모멘텀 기준 상위 30개 종목
    momentum_df = momentum_df.sort_values(by='순위')
    momentum_df[:30]

    momentum_df[:30].to_excel("momentum_list.xlsx")

def main():
    momentumCalc()
    df = pd.read_excel("momentum_list.xlsx")
    df.columns = ["종목코드", "모멘텀", "순위"]

    # 종목명 추가하기
    kiwoom = Kiwoom()
    kiwoom.CommConnect(block=True)
    codes = df["종목코드"]
    names = [kiwoom.GetMasterCodeName(code) for code in codes]
    df['종목명'] = pd.Series(data=names)


    # 매수하기
    accounts = kiwoom.GetLoginInfo('ACCNO')
    account = accounts[0]

    for code in codes:
        ret = kiwoom.SendOrder("시장가매수", "0101", account, 1, code, 100, 0, "03", "")
        time.sleep(0.2)
        print(code, "종목 시장가 주문 완료")


if __name__ == "__main__":
    main()