import requests
import json
import os

# 1. 설정
# 이 파일은 깃허브 블로그가 읽을 데이터 파일이 저장될 경로입니다.
# 실제 깃허브 리포지토리 구조와 동일하게 설정합니다.
DATA_FILE_PATH = "fetched_coin_data.json" 

def fetch_data():
    """외부 API에서 코인 데이터를 가져오는 함수"""
    try:
        # CoinGecko에서 비트코인, 이더리움, 도지코인의 현재 가격을 가져오는 API 예시
        api_url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin%2Cethereum%2Cdogecoin&vs_currencies=usd"
        
        response = requests.get(api_url)
        response.raise_for_status() # HTTP 오류 발생 시 예외 처리
        
        data = response.json()
        
        # 데이터를 웹사이트에 표시하기 좋게 정리
        coin_data_list = [
            {"name": "Bitcoin", "price_usd": data.get("bitcoin", {}).get("usd", "N/A")},
            {"name": "Ethereum", "price_usd": data.get("ethereum", {}).get("usd", "N/A")},
            {"name": "Dogecoin (Meme)", "price_usd": data.get("dogecoin", {}).get("usd", "N/A")}
        ]

        return coin_data_list

    except Exception as e:
        print(f"데이터를 가져오는 중 오류 발생: {e}")
        return []

def save_data(data):
    """가져온 데이터를 JSON 파일로 저장하는 함수"""
    with open(DATA_FILE_PATH, 'w', encoding='utf-8') as f:
        # JSON 파일에 예쁘게 저장
        json.dump(data, f, ensure_ascii=False, indent=4)
    print(f"데이터가 성공적으로 {DATA_FILE_PATH}에 저장되었습니다.")

if __name__ == "__main__":
    collected_data = fetch_data()
    save_data(collected_data)

# ... (기존 import 및 설정 코드 유지) ...

# ⚠️ 실제 EVM 노드 URL로 교체해야 합니다.
ETH_NODE_URL = "YOUR_ETHEREUM_OR_BSC_RPC_URL" 

def get_meme_coin_data(coin_address, router_address, chain_name):
    """특정 밈 코인의 거래량 및 유동성 데이터를 가져옵니다."""
    
    # ⚠️ 이 부분은 실제 Uniswap V2/V3 ABI를 사용하여 쿼리하는 복잡한 로직이 필요합니다.
    # 여기서는 개념 이해를 돕기 위해 임의의 데이터와 API를 사용합니다.
    
    try:
        # CoinGecko에서 코인의 가격을 가져오는 API (간단 예시)
        # 실제로는 거래량(Volume)을 가져와야 합니다.
        coin_id = coin_address[:10] # 주소 기반 임의 ID
        price_data = requests.get(f"https://api.coingecko.com/api/v3/simple/price?ids=dogecoin&vs_currencies=usd").json()
        
        # 임의의 데이터 생성
        trade_volume = hash(coin_address) % 1000000 + 50000 # 가짜 거래량 생성
        
        return {
            "name": f"MemeCoin-{chain_name}",
            "chain": chain_name,
            "address": coin_address,
            "volume_24h": trade_volume,
            "liquidity": trade_volume * 5,
            "price_usd": price_data.get('dogecoin', {}).get('usd', 'N/A')
        }
    except Exception as e:
        print(f"[{chain_name}] 데이터 쿼리 오류: {e}")
        return None

def collect_and_save_data():
    """여러 밈 코인의 데이터를 수집하고 JSON 파일로 저장합니다."""
    
    # ⚠️ 실제 밈 코인 주소와 체인 정보를 사용하여 리스트를 만드세요.
    target_coins = [
        {"addr": "0x1A2B3...", "router": "0xRouterA...", "chain": "Ethereum"},
        {"addr": "0x4C5D6...", "router": "0xRouterB...", "chain": "BNB Chain"},
        # ... 추가 밈 코인 정보 ...
    ]
    
    trending_data = []
    for coin in target_coins:
        data = get_meme_coin_data(coin['addr'], coin['router'], coin['chain'])
        if data:
            trending_data.append(data)
            
    # 거래량 기준으로 내림차순 정렬 (트렌딩 기능)
    trending_data.sort(key=lambda x: x['volume_24h'], reverse=True)
    
    # JSON 파일로 저장
    DATA_FILE_PATH = "fetched_coin_data.json"
    with open(DATA_FILE_PATH, 'w', encoding='utf-8') as f:
        json.dump(trending_data, f, ensure_ascii=False, indent=4)
        
    print(f"수집된 코인 데이터 수: {len(trending_data)}")

if __name__ == "__main__":
    collect_and_save_data()