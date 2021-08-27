
import requests
import xml.etree.ElementTree

# api 인증키
key = 'dswkIzbtmtoaVJONYr8kMHJBceWsS8B9SPs8zshw7LlAnQzhDCnNFSI48oQUeHTJBqtn%2FmD6S4i6HDSAUPQ2tQ%3D%3D'
# 버스 노선 아이디 입력
busRouteId = "100100112" # -> 721번 버스

# getRouteByStation api 호출
queryParams = 'ServiceKey=' + key + '&busRouteId=' + busRouteId
url = 'http://ws.bus.go.kr/api/rest/arrive/getArrInfoByRouteAll?' + queryParams

# xml 파싱을 위한 코드
req = requests.get(url)
tree = xml.etree.ElementTree.fromstring(req.text)
msgBody = tree.find("msgBody")
itemList = msgBody.findall("itemList")

num=1 # mp3파일명을 위한 변수
print("tts mp3 생성중...")
for i in itemList:
    stId = i.find("stId").text
    stNm = i.find("stNm").text
    # 음성 메세지 설정
    msg = "잠시후 " + stNm + " 정류장에서 휠체어 이용 승객이 탑승할 예정입니다. 휠체어 우선 좌석을 비워주시기 바랍니다......"
    tts_url = "https://fanyi.baidu.com/gettts?lan=kor&text=" + msg*2 + "&spd=3&source=web"
    # tts api 호출후 응답으로 저장
    response = requests.get(tts_url)

    # mp3 디렉토리에 형식에 .mp3 파일 형식으로 파일 생성후 이진파일 읽기 모드로 열기
    file = open('mp3/%04d.mp3'%num, 'wb')
    # 응답값 안의 파일을 .mp3에 저장
    file.write(response.content)
    # .mp3 파일 저장후 닫기
    file.close()
    print(".",end="")
    num+=1

print()

# 버스 아이디의 앞부분
print("unsigned int BUS_STATION_LIST_F[] = {",end="")
for i in itemList:
    stId = i.find("stId").text
    stNm = i.find("stNm").text
    print(stId[:5],end=",")
print("\b",end="")
print("}")

# 버스 아이디의 뒷부분
print("unsigned int BUS_STATION_LIST_B[] = {",end="")
for i in itemList:
    stId = i.find("stId").text
    stNm = i.find("stNm").text
    print("1"+stId[5:],end=",")
print("\b",end="")
print("}")