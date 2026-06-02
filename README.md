# Ladybug, Ladybug, Fly Away Home 中文汉化版

**[点击这里在线访问网页道具](https://sylz25.github.io/ladybug/)**

---

本项目是解谜跑团模组《Ladybug, Ladybug, Fly Away Home》网页道具的中文汉化与本地化版本。

## 致谢与原作信息 Credits
本网页翻译自开源项目，向原作者致敬：
* **原作作者 Author:** Jeff Moeller (出自《The Things We Leave Behind》)
* **原项目仓库 Original Repo:** [点击访问原作者项目](https://github.com/JamesAlday/ladybug)

---

## 原作简介与使用说明 Original Description & Usage

网页主页包含一个使用 Flipclock 制作的倒计时时钟。初始化代码位于 `index.html` 页面中。
The homepage contains a countdown clock that uses Flipclock. The code to initialize it is in index page.

默认倒计时为从现在起 5 天后的晚上 8 点。
It is defaulted to 8pm 5 days from now.

### 如何自定义倒计时天数 How to customize
如果你在网址后面加上一个整数作为Hash（#），就可以改变倒计时的天数。
If you add an integer as a hash after the page, it will change the number of days.

**示例 Example：**
* `http://.../ladybug`    --> 默认 5 天 (5 days)
* `http://.../ladybug#2`  --> 改为 2 天 (2 days)

通过这种方式，KP 可以根据 PC 第一次访问网站的时间，自由定制倒计时剩余的时间。
This way the KP can customize how much time remains on the countdown depending on when the PCs first visit the website.

---

## 汉化说明 Localization Notes
* 本项目仅对网页文本、提示及相关解谜内容进行了中文本地化。
* 网页中央的按钮可以切换中英双语，以防在翻译时出现歧义，一切以英语原文与守密人的解读为准。
