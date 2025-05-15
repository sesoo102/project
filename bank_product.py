import requests
import pprint

API_KEY = ""

# 정기 예금 상품 불러오기
def fetch_deposit_products():
    URL = "http://finlife.fss.or.kr/finlifeapi/depositProductsSearch.json"
    params = {
        'auth': API_KEY,
        'topFinGrpNo': '020000',  # 은행
        'pageNo': '1'
    }

    try:
        res = requests.get(URL, params=params)

        # 🔍 디버깅 출력
        print("예금 Status Code:", res.status_code)
        print("예금 응답 일부:", res.text[:300])  # 응답 일부 출력

        response = res.json()

        deposit_products_list = []
        baseList = response['result']['baseList']
        optionList = response['result']['optionList']

        for product in baseList:
            dict_product = {}
            intr_rate_type_nm = ''
            for option in optionList:
                if product['fin_prdt_cd'] == option['fin_prdt_cd']:
                    if not intr_rate_type_nm:
                        intr_rate_type_nm = option['intr_rate_type_nm']
                    if 'options' not in dict_product:
                        dict_product['options'] = {}
                    dict_product['options'][option['save_trm']] = {
                        'intr_rate': option.get('intr_rate', 0),
                        'intr_rate2': option.get('intr_rate2', 0)
                    }

            product['intr_rate_type_nm'] = intr_rate_type_nm
            product.update(dict_product)
            deposit_products_list.append(product)

        return deposit_products_list

    except Exception as e:
        print("예금 상품 조회 중 오류 발생:", e)
        return []


# 적금 상품 불러오기
def fetch_savings_products():
    URL = "http://finlife.fss.or.kr/finlifeapi/savingProductsSearch.json"
    params = {
        'auth': API_KEY,
        'topFinGrpNo': '020000',
        'pageNo': '1'
    }

    try:
        res = requests.get(URL, params=params)

        # 🔍 디버깅 출력
        print("적금 Status Code:", res.status_code)
        print("적금 응답 일부:", res.text[:300])  # 응답 일부 출력

        response = res.json()

        savings_products_list = []
        baseList = response['result']['baseList']
        optionList = response['result']['optionList']

        for product in baseList:
            dict_product = {}
            intr_rate_type_nm = ''
            for option in optionList:
                if product['fin_prdt_cd'] == option['fin_prdt_cd']:
                    if not intr_rate_type_nm:
                        intr_rate_type_nm = option['intr_rate_type_nm']
                    plan = option.get('rsrv_type_nm', '기타')
                    if plan not in dict_product:
                        dict_product[plan] = {}
                    dict_product[plan][option['save_trm']] = {
                        'intr_rate': option.get('intr_rate', 0),
                        'intr_rate2': option.get('intr_rate2', 0)
                    }

            product['intr_rate_type_nm'] = intr_rate_type_nm
            product.update(dict_product)
            savings_products_list.append(product)

        return savings_products_list

    except Exception as e:
        print("적금 상품 조회 중 오류 발생:", e)
        return []


# 실행
if __name__ == "__main__":
    print("\n정기 예금 상품 리스트:")
    deposit_data = fetch_deposit_products()
    pprint.pprint(deposit_data[:3])  # 상위 3개 미리 보기

    print("\n적금 상품 리스트:")
    savings_data = fetch_savings_products()
    pprint.pprint(savings_data[:3])  # 상위 3개 미리 보기
