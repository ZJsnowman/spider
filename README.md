# 这是什么
- 知乎
- 伯乐在线(没有任何反爬,随便玩)
- 天眼查

具体代码进入 spiders目录下对应的 py 文件


*这里数据库采取的 mysql.pipline和 middleware 也都有常用的实现.可以根据自己需求更改一下 setting 文件中的设置*



具体一些学习经验可以移步[我的博客](http://zjsnowman.com/2017/12/05/%E7%88%AC%E8%99%AB/)
## 知乎
通过 selenuim模拟登陆拿到 cookie, 支持后续页面使用
解决知乎插入数据库的时候主键冲突问题,通过 ` ON DUPLICATE KEY UPDATE ` 语句来实现更新
自行配置自己的账号密码

## 天眼查
这里提供了一个公司的列表文件.通过具体的公司名来进行索引的.你也可以替换成其他的.这里仅供展示

## pipline
- json 本地
- mysql 异步同步

__如果使用数据库,需要setting中配置自己的数据库信息__



## middleware
- 随机更换 use_agent
- 代理
- selenium 模拟加载
__知乎和天眼查均使用了 selenium模拟登陆,需要使用自己的账号密码进行替换__


## 执行
进入`main`文件中,取消注释具体的行,来执行对应的爬虫,建议 Pycharm 运行

## 可能的问题
提交 issue 吧