import requests
import gspread
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials
from st_aggrid import *

class Lotto:
    scope = [
        'https://spreadsheets.google.com/feeds',
        'https://www.googleapis.com/auth/drive',
    ]
    json_file_name = '../json/crucial-summer-360503-68a2e4b85a7c.json'
    credentials = ServiceAccountCredentials.from_json_keyfile_name(json_file_name, scope)
    gc = gspread.authorize(credentials)

    # 스프레스시트 문서 가져오기
    spreadsheet_url = 'https://docs.google.com/spreadsheets/d/17s0kzokun9nifb5YVyTfUL5UO_dr1OTxkyFN0LRW-Ec/edit#gid=0'

    # 스프레드시트 가져오기
    doc = gc.open_by_url(spreadsheet_url)

    # 시트별 데이터 가져오기
    worksheet_title = doc.worksheet('제목')
    worksheet_value = doc.worksheet('회차별')

    # 스프레드시트 요청 할당량 최대 60회라 1회에 모든 데이터 가져오기
    worksheet_value_list = worksheet_value.get_all_values()
    column_title = worksheet_title.row_values(1)
    # 총계
    worksheet_row_cnt = len(worksheet_value_list)
    # 페이징처리를 위한 변수
    page_number=0
    # row 15개 씩
    N = 15

    def lotto_main(st):
        st.subheader('로또')
        last_page = Lotto.worksheet_row_cnt // Lotto.N
        now_char = Lotto.lotto_select(st, Lotto.worksheet_row_cnt)

        if now_char == None:
            # 버튼 생성
            prev, _ , next = st.columns([1,10,1])
            if next.button("Next"):
                if Lotto.page_number + 1 > last_page:
                    Lotto.page_number = 0
                else:
                    Lotto.page_number += 1
            if prev.button("Previous"):
                if Lotto.page_number - 1 < 0:
                    Lotto.page_number = last_page
                else:
                    Lotto.page_number -= 1
            start_idx = Lotto.page_number * Lotto.N
            end_idx = (1 + Lotto.page_number) * Lotto.N
            table_pageing = Lotto.worksheet_value_list[start_idx:end_idx]
            # Index into the sub dataframe
            tb_pg_df = pd.DataFrame(table_pageing,columns=Lotto.column_title)
            AgGrid(tb_pg_df, width="auto")
        else :
            table_char = Lotto.worksheet_value_list[now_char-1:now_char]
            tb_ch_df = pd.DataFrame(table_char,columns=Lotto.column_title)
            st.write(tb_ch_df)
        lotto_chart_btn = st.checkbox("번호 횟수 차트 보기")

        if lotto_chart_btn:
            number_list = []
            for row in Lotto.worksheet_value_list:
                number_list.append(int(row[12]))
                number_list.append(int(row[13]))
                number_list.append(int(row[14]))
                number_list.append(int(row[15]))
                number_list.append(int(row[16]))
                number_list.append(int(row[17]))
                number_list.append(int(row[18]))

            hist_values = np.histogram(number_list, bins=46, range=(0,46))[0]
            st.bar_chart(hist_values)

        lotto_insert_btn = st.checkbox("입력")

        if lotto_insert_btn:
            url = 'https://www.dhlottery.co.kr/common.do?method=getLottoNumber&drwNo='+str(Lotto.worksheet_row_cnt+1)
            req_result = requests.get(url)
            json_result  = req_result.json()
            if str(json_result.get('returnValue', None)) == "success" :
                st.write(str(json_result.get('drwNo', None)), " 회차를 입력해주세요. (4등,5등 금액은 자동으로 입력됩니다.)")
                date = st.date_input(label = "추첨일을 입력해주세요.", value = pd.to_datetime(json_result.get('drwNoDate', None))).strftime("%Y.%m.%d")
                cnt_1st = st.number_input(label = "당첨자수(1등)을 입력해주세요.", value = json_result.get('firstPrzwnerCo', None))
                amount_1st = st.number_input(label = "당첨금액(1등)을 입력해주세요.", value = json_result.get('firstWinamnt', None))
                cnt_2st = st.number_input(label = "당첨자수(2등)을 입력해주세요.", value = 0)
                amount_2st = st.number_input(label = "당첨금액(2등)을 입력해주세요.", value = 0)
                cnt_3st = st.number_input(label = "당첨자수(3등)을 입력해주세요.", value = 0)
                amount_3st = st.number_input(label = "당첨금액(3등)을 입력해주세요.", value = 0)
                cnt_4st = st.number_input(label = "당첨자수(4등)을 입력해주세요.", value = 0)
                cnt_5st = st.number_input(label = "당첨자수(5등)을 입력해주세요.", value = 0)
                win_1st = st.number_input(label = "당첨번호(1)을 입력해주세요.", value = json_result.get('drwtNo1', None))
                win_2st = st.number_input(label = "당첨번호(2)을 입력해주세요.", value = json_result.get('drwtNo2', None))
                win_3st = st.number_input(label = "당첨번호(3)을 입력해주세요.", value = json_result.get('drwtNo3', None))
                win_4st = st.number_input(label = "당첨번호(4)을 입력해주세요.", value = json_result.get('drwtNo4', None))
                win_5st = st.number_input(label = "당첨번호(5)을 입력해주세요.", value = json_result.get('drwtNo5', None))
                win_6st = st.number_input(label = "당첨번호(6)을 입력해주세요.", value = json_result.get('drwtNo6', None))
                win_bonus = st.number_input(label = "보너스번호를 입력해주세요.", value = json_result.get('bnusNo', None))

                if st.button("저장"):
                    with st.spinner('Wait for it...'):
                        Lotto.worksheet_value.append_row([str(json_result.get('drwNo', None)), date, cnt_1st, format(amount_1st,",")+"원", cnt_2st, format(amount_2st,",")+"원", cnt_3st, format(amount_3st,",")+"원", cnt_4st, "50,000원", cnt_5st, "5,000원",win_1st,win_2st,win_3st,win_4st,win_5st,win_6st,win_bonus])
                        st.success('저장되었습니다.')
            else :
                st.write(str(Lotto.worksheet_row_cnt+1),"회차 결과가 안나왔습니다.")

    def lotto_select(st,worksheet_row_cnt):
        select_box = [None]
        for i in reversed(range(worksheet_row_cnt+1)):
            if i > 0 : select_box.append(i)
        option = st.selectbox('조회하실 회차를 선택하여주세요.',select_box)
        return option