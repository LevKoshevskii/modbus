from pymodbus.client.sync import ModbusTcpClient

host = '10.0.2.5'
port = 601

client = ModbusTcpClient(host, port)
client.connect()

n = 5
N = n * 100

one_bit_length = 1
one_Byte_length = 8 * one_bit_length
one_register_length = 2 * one_Byte_length

response = client.read_holding_registers(N, 7, unit = 1).registers
# response = [51377, 16959, 17734, 18248, 18762, 19276, 19790]

responseBin = []
for i in response:
    responseBin.append(bin(i)[2:].zfill(one_register_length))

def toDecimal(raw):
    if raw[0] == '1':
        res = ''

        for i in raw:
            if i == '1':
                res += '0'
            else:
                res += '1'
        return -(int(res, 2) + 1)
    else:
        return int(raw, 2)

unsignDec = response[0]
unsignBin = responseBin[0]

sign_bin = responseBin[1]
sign_dec = toDecimal(responseBin[1])


wordIndex = [2, 3, 4, 5, 6]
wordBinList = [responseBin[i] for i in wordIndex]

wordBin = ''.join(wordBinList)

charBinList = []
for i in wordBinList:
    ch1 = i[:len(i)//2]
    ch2 = i[len(i)//2:]
    charBinList.append(ch1)
    charBinList.append(ch2)

charDecodedList = [chr( int(i,2) ) for i in charBinList]
decodedString = ''.join(charDecodedList)

print('1) Прочитанные регистры: ')
for i in range(0, len(response)):
    print("  " + str(i + 1) + " - " + str(response[i]))
print('2) Число без знака: ' + str(unsignDec))
print('3) Число со знаком: ' + str(sign_dec))
print('4) Строка:', decodedString)
