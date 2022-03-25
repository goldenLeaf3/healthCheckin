# healthCheckin
#### 使用方法：

1. 复制此项目的clone地址(https)；新建一个你自己的repository并设置为private(因为需要填入你自己的账号密码等个人信息)；在新建的repository中import code并填入复制的此项目的clone地址。

2. 在checkin.py中填入你的账号密码，以及mycontent。

3. mycontent的获取需要在安卓或者苹果上抓包。安装抓包软件(苹果 stream；安卓 HttpCanary)，走一遍正常的打卡流程，使得抓包软件能抓到此次打卡的数据包；在抓到的这些包中找到一个post请求(url为：questionAndAnser/wenjuanSubmit)，请求体中包含content内容，将“content=”后面的字符串复制粘贴到checkin.py的mycontent中。(注意：若content内容中含有"%2"等符号，需要url解码：[点此处](http://www.jsons.cn/urlencode)在线解码，粘贴含有"%2"的内容，点击UrlDecode，再将解码后的内容复制到checkin.py的mycontent里)

4. 在checkin.py里填入对应的邮件信息，就能够及时通知到你了。

5. 修改.github/workflows/autoRun.yml；去掉schedule和下一行的"#"并保存。然后大功告成了，默认的是每天早上六点(UTC：22点)自动打卡。


#### 参考教程：

- [自动化健康打卡 | 会下雪的晴天](https://yq1ng.github.io/2021/03/27/zi-dong-hua-jian-kang-da-qia/)
- [httpCanary app抓包](https://blog.csdn.net/qq_43500579/article/details/103907845)

- [使用*Stream抓包* - ycyzharry - 博客园](https://www.baidu.com/link?url=lbLejFAN8tFd5ag3_vWnyMG7IzpFfImK62rZIIoXkeo6vYMkIsoWct05mfGfOPqoSw0P4rQQZd6tqtJUnf69V_&wd=&eqid=9b44680d000d235100000003623424c5)

- [web抓包结果对应python request](https://www.jianshu.com/p/679b4a7c6b7c)
