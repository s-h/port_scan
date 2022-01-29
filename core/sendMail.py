#!/usr/bin/python3
import smtplib
from email.mime.text import MIMEText
from email.header import Header

sender = 'foo@mail.com' # 发送邮箱
password = 'youpasword'    # 邮箱密码
receivers = ['bar@mail.com']  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱


def toTHML(results):
    msg = """
    <table border="1">
    <tr>
    <td>
    IP地址
    </td>
    <td>
    描述
    </td>
    <td>
    端口
    </td>
    </tr>
    """
    for ip_index in results:
        msg += "<tr>"

        msg += "<td>"
        msg += ip_index
        msg += "</td>"

        msg += "<td>"
        msg += results[ip_index]["describe"]
        msg += "</td>"

        msg += "<td>"
        msg += str(results[ip_index]["port_status"])
        msg += "</td>"

        msg += "</tr>"

    msg += "</table>"
    return msg

def sendmail(msg):
    mail_msg = toTHML(msg)
    print(mail_msg)
    message = MIMEText(mail_msg, 'html', 'utf-8')
    message['From'] = Header("cmcc_ops", 'utf-8')
    #message['To'] =  Header("", 'utf-8')

    subject = '端口探测'
    message['Subject'] = Header(subject, 'utf-8')


    try:
        smtpObj = smtplib.SMTP('smtp.exmail.qq.com')
        smtpObj.login(sender, password)
        smtpObj.sendmail(sender, receivers, message.as_string())
        smtpObj.quit()
        print ("邮件发送成功")
    except smtplib.SMTPException as e:
        print(e)
        print ("Error: 无法发送邮件")