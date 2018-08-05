# server monitor（服务器监控程序）

可登陆管理自己的多台服务器，实现实时监控。
后端使用Django框架。

部分运行图可在该项目的source目录中下载。


### 运行首页如图：

![](https://github.com/zwq-qianyu/server_monitor/raw/master/source/index.png)  

### 详情页如图：

![](https://github.com/zwq-qianyu/server_monitor/raw/master/source/detail.png)  

### 使用方法：
首先导入 auto.sql 数据库或执行 create_monitor.sql 中的部分代码生成数据库。<br>
然后需要对 settings 文件进行数据库配置。<br>
如果是使用的 auto.sql 导入数据库，可以使用 ziyichen 登录进行测试，密码为 123456


最后：
![](https://github.com/zwq-qianyu/server_monitor/raw/master/source/use.png)  

### 运行环境：
Python3

### 安全性：
采用hash算法加密用户密码，数据库user数据表案例如图：
![](https://github.com/zwq-qianyu/server_monitor/raw/master/source/safe.png)  

#### 注意：
添加管理的服务器必须要支持Python3可以正常添加进行管理

详细实现过程过一段时间可以看我博客：https://www.runtofuture.cn 

最近较忙，有时间将这个项目的思路写在博客上。

