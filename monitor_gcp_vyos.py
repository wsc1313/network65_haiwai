from pythonping import ping
from netmiko import ConnectHandler
import time
from datetime import datetime
import threading

"""
需要监控的目前在用的用于和GCP网关建立VPN隧道的海外vyos
# 10.147.132.0/23 阿里云海外SDK vyos:47.89.255.28
# 10.148.114.0/23 腾讯云 泰国神魔手游 vyos:43.128.88.46
# 10.148.116.0/23 腾讯云 马来诛仙移动 vyos:43.156.23.58
# 10.147.146.0/23 阿里云 神魔国际 vyos:47.253.58.21
# 10.147.152.0/23 阿里云 韩国幻塔 vyos:8.213.136.83
"""

key_file = '/root/.ssh/id_rsa'
# device_dict = {'aliyun_SDK': '47.89.255.28', 'tx_taiguoshenmo': '43.128.88.46', 'tx_malaizhuxian': '43.156.23.58',
#                'aliyun_shenmoguoji': '47.253.58.21', 'aliyun_hanguohuanta': '8.213.136.83'}
ip_dict = {'10.147.132.10': 'aliyun_SDK', '10.148.114.10': 'tx_taiguoshenmo', '10.148.116.10': 'tx_malaizhuxian',
           '10.147.146.10': 'aliyun_shenmoguoji', '10.147.152.10': 'aliyun_hanguohuanta', '10.9.13.222': 'vyos1',
           '10.9.13.223': 'vyos2', }
vyos_aliyun_SDK = {'device_type': 'vyos', 'host': '47.89.255.28', 'username': 'vyos', 'use_keys': True,
                   'key_file': key_file, 'port': 30022, }
vyos_tx_taiguoshenmo = {'device_type': 'vyos', 'host': '43.128.88.46', 'username': 'vyos', 'use_keys': True,
                        'key_file': key_file, 'port': 30022, }
vyos_tx_malaizhuxian = {'device_type': 'vyos', 'host': '43.156.23.58', 'username': 'vyos', 'use_keys': True,
                        'key_file': key_file, 'port': 30022, }
vyos_aliyun_shenmoguoji = {'device_type': 'vyos', 'host': '47.253.58.21', 'username': 'vyos', 'use_keys': True,
                           'key_file': key_file, 'port': 30022, }
vyos_aliyun_hanguohuanta = {'device_type': 'vyos', 'host': '8.213.136.83', 'username': 'vyos', 'use_keys': True,
                            'key_file': key_file, 'port': 30022, }
vyos_eve_test1 = {'device_type': 'vyos', 'host': '10.9.13.220', 'username': 'vyos', 'use_keys': True,
                  'key_file': key_file, 'port': 30022, }
vyos_eve_test2 = {'device_type': 'vyos', 'host': '10.9.13.221', 'username': 'vyos', 'use_keys': True,
                  'key_file': key_file, 'port': 30022, }


# 重新刷配置函数
def reconf_vyos_vpn_interface(**kwargs):
    command_list1 = ['delete vpn ipsec ipsec-interfaces interface eth0', ]
    command_list2 = ['set vpn ipsec ipsec-interfaces interface eth0', ]
    with ConnectHandler(**kwargs) as connect:
        output1 = connect.send_config_set(command_list1, exit_config_mode=False)
        output1_commit = connect.commit()
        output2 = connect.send_config_set(command_list2, exit_config_mode=False)
        output2_commit = connect.commit()
    result = output1 + '\n' + output1_commit + '\n' + output2 + '\n' + output2_commit
    return result


# 监控逻辑函数
def monitor_ping(ip, devinfo):
    logfile_name = ip + '_' + 'monitor_result.log'
    with open(logfile_name, 'a') as f:
        f.write(datetime.now().ctime() + ": " + str(ip_dict.get(ip)) + '开始被监控...\n')
    while True:
        ping_result = ping(ip)

        if 'Reply' in str(ping_result):
            time.sleep(10)
            continue
        else:
            reconf_result = reconf_vyos_vpn_interface(**devinfo)
            with open(logfile_name, 'a') as f:
                f.write('#' * 10 + datetime.now().ctime() + '#' * 10 + '\n' + '重刷vpn接口配置，结果如下...\n'
                        + reconf_result + '\n')


t1 = threading.Thread(target=monitor_ping, args=('10.147.132.10', vyos_aliyun_SDK))
t2 = threading.Thread(target=monitor_ping, args=('10.148.114.10', vyos_tx_taiguoshenmo))
t3 = threading.Thread(target=monitor_ping, args=('10.148.116.10', vyos_tx_malaizhuxian))
t4 = threading.Thread(target=monitor_ping, args=('10.147.146.10', vyos_aliyun_shenmoguoji))
t5 = threading.Thread(target=monitor_ping, args=('10.147.152.10', vyos_aliyun_hanguohuanta))
t1.setDaemon(True)
t2.setDaemon(True)
t3.setDaemon(True)
t4.setDaemon(True)
t5.setDaemon(True)

t1.start()
t2.start()
t3.start()
t4.start()
t5.start()

"""测试使用"""
# t6 = threading.Thread(target=monitor_ping, args=('10.9.13.222', vyos_eve_test1))
#
# t7 = threading.Thread(target=monitor_ping, args=('10.9.13.223', vyos_eve_test2))
#
# t6.setDaemon(True)
# t6.start()
# t7.setDaemon(True)
# t7.start()

while True:
    time.sleep(31536000)
    break




# result = reconf_vyos_vpn_interface(**vyos_eve_test)
# print(result)
