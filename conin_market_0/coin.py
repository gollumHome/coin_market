#! usr/bin/python
# -*-coding:utf8-*-


import requests
from lxml import etree
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
import smtplib

from constant import coin_list
from constant import coin_usdt

from constant import smtp_server
from constant import from_addr
from constant import password
from constant import exchange_rate
from constant import expect_price
from constant import receive_list




def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr((Header(name, 'utf-8').encode(), addr))


def get_rmb_price(url='https://gateio.io/'):
    r = requests.get(url)
    #print r.text
    html = etree.HTML(r.text)
    result = html.xpath('//tbody/tr')
    data_list = []
    for item in result:
        id = item.attrib['id']
        for (coin_item, usdt_item) in zip(coin_list, coin_usdt):
            if id == usdt_item:
                str = etree.tostring(item)
                str_html = etree.HTML(str)
                re_ = str_html.xpath('//span')
                for class_name in re_:
                     name = class_name.attrib['class']
                     if name == 'rate_down' or name == 'rate_up':
                        rate_down_str = etree.tostring(class_name)
                        #print rate_down_str
                        ss = etree.HTML(rate_down_str)
                        try:
                            dollor_count = ss.xpath('//span/text()')[0].split('$')[1]
                            RMB = float(dollor_count) * exchange_rate
                            data_list.append({'exchange_rate': exchange_rate,
                                              'name': coin_item,
                                              'price_RMB': RMB})
                        except Exception:
                            pass
    return data_list


def price_justment(data_list, expect_price):
    price_message = ' '
    for item in data_list:
        coin_name = item['name']
        if coin_name == 'EOS':
            if item['price_RMB'] < expect_price['EOS']:
                price_text = '当前价格已低于预期，上车-'+'EOS：'+str(expect_price['EOS'])
                price_message += price_text+' ;'
            else:
                price_text = '当前价格--' + 'EOS：' + str(item['price_RMB'])
                price_message += price_text+' ;'
        elif coin_name == 'BTC':
            if item['price_RMB'] < expect_price['BTC']:
                price_text = '当前价格已低于预期，上车-'+'BTC：'+str(expect_price['BTC'])
                price_message += price_text+' ;'
            else:
                price_text = '当前价格-' + 'BTC：' + str(item['price_RMB'])
                price_message += price_text+' ;'
        elif coin_name == 'ETH':
            if item['price_RMB'] < expect_price['ETH']:
                price_text = '当前价格已低于预期，上车-'+'ETH：'+str(expect_price['ETH'])
                price_message += price_text+' ;'
            else:
                price_text = '当前价格-' + 'ETH：' + str(item['price_RMB'])
                price_message += price_text+' ;'
        elif coin_name == 'ADA':
            if item['price_RMB'] < expect_price['ADA']:
                price_text = '当前价格已低于预期，上车-'+'艾达币：'+str(expect_price['ADA'])
                price_message += price_text
            else:
                price_text = '当前价格--' + '艾达币' + str(item['price_RMB'])
                price_message += price_text+' ;'
        elif coin_name == 'XRP':
            if item['price_RMB'] < expect_price['XRP']:
                price_text = '当前价格已低于预期，上车-'+'瑞波币：'+str(expect_price['EOS'])
                price_message += price_text+' ;'
            else:
                price_text = '当前价格--' + '瑞波币：' + str(item['price_RMB'])
                price_message += price_text+' ;'
        elif coin_name == 'Stellar':
            if item['price_RMB'] < expect_price['Stellar']:
                price_text = '当前价格已低于预期，上车-'+'恒星币：'+str(expect_price['Stellar'])
                price_message += price_text+' ;'
            else:
                price_text = '当前价格--' + '恒星币：' + str(item['price_RMB'])
                price_message += price_text+' ;'
    return price_message


def get_message(rece_list, mess_text):
    msg = MIMEText(mess_text, 'plain', 'utf-8')
    msg['From'] = _format_addr('coin message <%s>' % from_addr)
    msg['To'] = _format_addr('管理员 <%s>' % rece_list[0])
    msg['Subject'] = Header('不要怂，就是梭,汇率固定为6.5', 'utf-8').encode()
    return msg


def send_message(msg, rece_list):
    try:
        server = smtplib.SMTP(smtp_server, 25)
        server.login(from_addr, password)
        server.sendmail(from_addr, [rece_list[0]], msg.as_string())
        server.quit()
    except Exception, e:
        print str(e)





if __name__ == '__main__':
    data_list = get_rmb_price()
    print data_list
    price_text = price_justment(data_list, expect_price)
    if price_text:
        msg = get_message(receive_list, price_text)
        send_message(msg, receive_list)
