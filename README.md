# gouchicao-video
基于OpenCV开发的，用于图像识别展示。支持图片、图片目录、视频文件、实时视频等。目前是使用的[darknet-serving](https://github.com/gouchicao/darknet-serving)的gPRC接口来对接的服务器端，后面考虑做成插件的形式，解除这种耦合关系。

## 功能列表
1. 支持展示图片、图片目录、视频文件、实时视频；
2. 按q和esc键退出程序；
3. 时间间隔过长的情况下，按任意键可以路过间隔；

## 显示界面
![](predict/image-helmet.jpg)

## 使用示例
>  
* 设置服务地址
```bash
# 192.168.0.130:7713 需要换成你们的服务地址
$ server_address=192.168.0.130:7713
```

1. 图片
```bash
$ python3 gouchicao_video.py -a $server_address -f test/image-helmet.jpg
```

2. 图片目录
```bash
# 默认按任意键继续识别下一张图片
$ python3 gouchicao_video.py -a $server_address -d test/images-helmet/

# 1秒后继续识别下一张图片
$ python3 gouchicao_video.py -a $server_address -d test/images-helmet/ -t 1000
```

3. 视频文件
```bash
$ python3 gouchicao_video.py -a $server_address -v video-helmet.mp4
```

4. 实时视频
```bash
$ python3 gouchicao_video.py -a $server_address
```
