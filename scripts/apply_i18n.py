#!/usr/bin/env python3
"""Apply bilingual lang-en / lang-zh markup to all HTML pages."""

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TITLE_EN = "Church of the Passover Angel"
TITLE_ZH = "逾越天使教会"
SCRIPT_TAG = '<script src="js/i18n.js"></script>'


def wrap_pair(en: str, zh: str, inline=False) -> str:
    cls = " lang-inline" if inline else ""
    return (
        f'<span class="lang-en">{en}</span>'
        f'<span class="lang-zh{cls}">{zh}</span>'
    )


def wrap_block(en: str, zh: str) -> str:
    return f'<div class="lang-en">{en}</div><div class="lang-zh">{zh}</div>'


def wrap_p_inner(en_inner: str, zh_plain: str) -> str:
    zh_esc = zh_plain.replace("&", "&amp;").replace("<", "&lt;")
    return (
        f'<span class="lang-en">{en_inner}</span>'
        f'<span class="lang-zh">{zh_esc}</span>'
    )


def add_scripts(html: str) -> str:
    if SCRIPT_TAG in html:
        return html
    return html.replace(
        '<script src="js/app.js"></script>',
        SCRIPT_TAG + "\n\t\t<script src=\"js/app.js\"></script>",
    )


def patch_title(html: str) -> str:
    return html.replace(
        f"<title>{TITLE_EN}</title>",
        f'<title data-title-en="{TITLE_EN}" data-title-zh="{TITLE_ZH}">{TITLE_EN}</title>',
    )


def patch_header(html: str) -> str:
    html = html.replace(
        "<h1 class=\"site-title\">Church of the Passover Angel</h1>",
        f'<h1 class="site-title">{wrap_pair(TITLE_EN, TITLE_ZH)}</h1>',
    )
    html = html.replace(
        '<button class="menu-toggle"><i class="fa fa-bars"></i> Menu</button>',
        f'<button class="menu-toggle"><i class="fa fa-bars"></i> {wrap_pair("Menu", "菜单")}</button>',
    )
    nav = [
        ("Homepage", "首页", "Lorem ipsum", "欢迎光临"),
        ("About Us", "关于我们", "About Our Church", "了解本教会"),
        ("Sermons", "讲道", "Words From On High", "来自天上的话语"),
        ("The Book", "圣书", "Donate Today", "立即捐助"),
        ("Contact", "联系", "We Want To Hear From You", "我们期待您的来信"),
    ]
    for en, zh, sub_en, sub_zh in nav:
        html = html.replace(
            f">{en} <small>{sub_en}</small></a>",
            f">{wrap_pair(en, zh, True)} <small>{wrap_pair(sub_en, sub_zh, True)}</small></a>",
        )
    return html


def patch_footer(html: str) -> str:
    html = html.replace(
        "<h3 class=\"widget-title\">Our address</h3>",
        f"<h3 class=\"widget-title\">{wrap_pair('Our address', '我们的地址')}</h3>",
    )
    quote_en = (
        "There is but one Church in which men find salvation, just as outside the ark of "
        "Noah it was not possible for anyone to be saved. (Thomas Aquinas)"
    )
    quote_zh = "人只得在一个教会里得救，正如在挪亚方舟之外，无人能得救。（托马斯·阿奎那）"
    html = html.replace(
        f"<p>{quote_en}</p>",
        wrap_block(f"<p>{quote_en}</p>", f"<p>{quote_zh}</p>"),
    )
    html = html.replace(
        "<h2 class=\"widget-title\">Free Gift With Donation!</h2>",
        f"<h2 class=\"widget-title\">{wrap_pair('Free Gift With Donation!', '捐助即赠好礼！')}</h2>",
    )
    html = html.replace('alt="Donate"', 'alt="Donate" data-alt-en="Donate" data-alt-zh="捐助"')
    html = html.replace(
        "<h3 class=\"widget-title\"><a name=\"contact\">Contact form</a></h3>",
        f"<h3 class=\"widget-title\"><a name=\"contact\">{wrap_pair('Contact form', '联系表单')}</a></h3>",
    )
    html = html.replace(
        "<h3 class=\"widget-title\">Contact form</h3>",
        f"<h3 class=\"widget-title\">{wrap_pair('Contact form', '联系表单')}</h3>",
    )
    html = html.replace(
        'placeholder="Your name..."',
        'placeholder="Your name..." data-ph-en="Your name..." data-ph-zh="您的姓名…"',
    )
    html = html.replace(
        'placeholder="Email..."',
        'placeholder="Email..." data-ph-en="Email..." data-ph-zh="电子邮箱…"',
    )
    html = html.replace(
        'placeholder="Your message..."',
        'placeholder="Your message..." data-ph-en="Your message..." data-ph-zh="您的留言…"',
    )
    html = html.replace(
        'value="Send message"',
        'value="Send message" data-val-en="Send message" data-val-zh="发送留言"',
    )
    copy = wrap_pair(
        "Church of the Passover Angel. All right reserved",
        "逾越天使教会。保留一切权利",
        True,
    )
    html = re.sub(
        r"<p class=\"colophon\">Copyright <span class=\"year-0\"></span> Church of the Passover Angel\. All right reserved\s*</p>",
        f'<p class="colophon">Copyright <span class="year-0"></span> {copy}</p>',
        html,
    )
    return html


def patch_form_script(html: str) -> str:
    if "patchFormPlaceholders" in html:
        return html
    snippet = """
        <script>
        (function(){
          function patchFormPlaceholders(){
            var zh = document.documentElement.lang === 'zh-CN';
            document.querySelectorAll('[data-ph-en]').forEach(function(el){
              el.placeholder = zh ? el.getAttribute('data-ph-zh') : el.getAttribute('data-ph-en');
            });
            document.querySelectorAll('[data-val-en]').forEach(function(el){
              el.value = zh ? el.getAttribute('data-val-zh') : el.getAttribute('data-val-en');
            });
            document.querySelectorAll('[data-alt-en]').forEach(function(el){
              el.alt = zh ? el.getAttribute('data-alt-zh') : el.getAttribute('data-alt-en');
            });
          }
          document.addEventListener('DOMContentLoaded', patchFormPlaceholders);
          var obs = new MutationObserver(patchFormPlaceholders);
          document.addEventListener('DOMContentLoaded', function(){
            obs.observe(document.documentElement, {attributes:true, attributeFilter:['lang']});
          });
        })();
        </script>"""
    return html.replace("</body>", snippet + "\n    </body>")


def patch_sermon_paragraphs(html: str, zh_map: dict) -> str:
    for sid, zh_list in zh_map.items():
        pattern = (
            rf'(<div id="{sid}" class="panel-collapse[^>]*>\s*<div class="panel-body">)'
            r"(.*?)"
            r"(</div>\s*</div>)"
        )
        m = re.search(pattern, html, re.S)
        if not m:
            print("warn: body", sid)
            continue
        if '<p><span class="lang-en">' in m.group(2):
            continue
        idx = [0]

        def repl_p(pm):
            n = idx[0]
            idx[0] += 1
            inner = pm.group(1)
            zh = zh_list[n] if n < len(zh_list) else ""
            return "<p>" + wrap_p_inner(inner, zh) + "</p>"

        new_inner = re.sub(r"<p[^>]*>(.*?)</p>", repl_p, m.group(2), flags=re.S)
        if idx[0] != len(zh_list):
            print("warn:", sid, "p count", idx[0], "zh count", len(zh_list))
        html = html[: m.start(2)] + new_inner + html[m.start(3) :]
    return html


def patch_index(html: str) -> str:
    pairs = [
        (
            "<h1 class=\"text-center\">The Angel Cometh!</h1>",
            f"<h1 class=\"text-center\">{wrap_pair('The Angel Cometh!', '天使将至！')}</h1>",
        ),
        (
            "<h3 class=\"text-center\">Now is the time to get right with God - before it's too late!</h3>",
            '<h3 class="text-center">' + wrap_pair("Now is the time to get right with God - before it's too late!", "现在正是归向上帝的时候——趁还来得及！") + "</h3>",
        ),
        ("<h2 class=\"section-title\">Recent news</h2>", f"<h2 class=\"section-title\">{wrap_pair('Recent news', '最新消息')}</h2>"),
        (">The Sun Darkens</a>", f">{wrap_pair('The Sun Darkens', '太阳变暗', True)}</a>"),
        (">Satan’s Control of U.S. Government</a>", f">{wrap_pair('Satan’s Control of U.S. Government', '撒旦对美国政府的控制', True)}</a>"),
        (">Angels of Vengeance</a>", f">{wrap_pair('Angels of Vengeance', '复仇天使', True)}</a>"),
        (">New World Disorder</a>", f">{wrap_pair('New World Disorder', '新世界失序', True)}</a>"),
        ("<h2 class=\"section-title\">Ways To Prepare</h2>", f"<h2 class=\"section-title\">{wrap_pair('Ways To Prepare', '预备之道')}</h2>"),
        (">Genesis Series Shelters</h3>", f">{wrap_pair('Genesis Series Shelters', '创世系列避难所', True)}</h3>"),
        (">The Right Stuff</h3>", f">{wrap_pair('The Right Stuff', '必备物资', True)}</h3>"),
        (">Atlas Shelters</h3>", f">{wrap_pair('Atlas Shelters', '阿特拉斯避难所', True)}</h3>"),
        (">Prepare Your Kids</h3>", f">{wrap_pair('Prepare Your Kids', '教导儿女预备', True)}</h3>"),
        (">Repent Now!</h3>", f">{wrap_pair('Repent Now!', '现在就悔改！', True)}</h3>"),
        (">Know What Is Coming</h3>", f">{wrap_pair('Know What Is Coming', '知晓将临之事', True)}</h3>"),
        ('class="button">More Ways To Prepare</a>', f'class="button">{wrap_pair("More Ways To Prepare", "更多预备方式", True)}</a>'),
        ("<h2 class=\"section-title\">Previous sermons</h2>", f"<h2 class=\"section-title\">{wrap_pair('Previous sermons', '往期讲道')}</h2>"),
        (">The Judge is At the Door</a>", f">{wrap_pair('The Judge is At the Door', '审判者已在门前', True)}</a>"),
        (">Annointed By God</a>", f">{wrap_pair('Annointed By God', '受上帝膏抹', True)}</a>"),
        (">THE TIME HAS COME!</a>", f">{wrap_pair('THE TIME HAS COME!', '时候已到！', True)}</a>"),
        (">Reverend Balfour</div>", f">{wrap_pair('Reverend Balfour', '鲍尔弗牧师', True)}</div>"),
        ('class="button">See all sermons</a>', f'class="button">{wrap_pair("See all sermons", "查看全部讲道", True)}</a>'),
    ]
    verse_en = """<p class="news news-title text-center">
                        For I will pass through the land of Egypt this night,<br>
                        and will smite all the firstborn in the land of Egypt, both man and beast;<br>
                        and against all the gods of Egypt I will execute judgment: <br>
                        I <i>am</i> the LORD.
                    </p>"""
    verse_zh = """<p class="news news-title text-center">
                        因我今夜要行经埃及全地，把埃及地一切头生的，无论是人是牲畜，都击杀了；<br>
                        又要败坏埃及一切的神。<br>
                        我乃是耶和华。
                    </p>"""
    html = html.replace(verse_en, wrap_block(verse_en, verse_zh))
    for a, b in pairs:
        html = html.replace(a, b)
    return html


def patch_about(html: str) -> str:
    html = html.replace(
        "<h2 class=\"section-title\">About The Church of the Passover Angel</h2>",
        f"<h2 class=\"section-title\">{wrap_pair('About The Church of the Passover Angel', '关于逾越天使教会')}</h2>",
    )
    blocks = [
        (
            "We are a small, non-denominational, fundamentalist Church devoted to total submission to the will of God and his herald, the Passover Angel.",
            "我们是一座小型、非宗派、基要主义的教会，全然顺服上帝的旨意及其使者逾越天使。",
        ),
        (
            "We believe that the End Times are near. Soon God will return to the world, through his messenger the Passover Angel, in order to cleanse the world of sin and restore righteousness through the Rapture.",
            "我们相信末世已近。上帝不久将借其使者逾越天使重返世界，洁净罪恶，并通过被提恢复公义。",
        ),
        (
            "Many churches will tell you that the Rapture was foretold by John in the Book of Revelations, but they are deceived. Only those who follow the true words of God’s Angel will be redeemed, and so we must all repent if we hope to be saved.",
            "许多教会告诉你被提已在《启示录》中由约翰预言，但他们受了迷惑。唯有听从上帝天使真实话语者才能得赎，因此我们若盼望得救，都必须悔改。",
        ),
        (
            '"Boast not thyself of to morrow; for thou knowest not what a day may bring forth." (Proverbs 27:1)',
            "「不要为明日自夸，因为一日要生何事，你尚且不能知道。」（箴言 27:1）",
        ),
    ]
    for en, zh in blocks:
        html = html.replace(f"<p>\n                                        {en}\n                                    </p>", wrap_block(f"<p>\n                                        {en}\n                                    </p>", f"<p>\n                                        {zh}\n                                    </p>"))
    donate_en = 'Donate to our Church now and receive <a href="book.html"><u>The Book of the Passover Angel</u></a> to learn more.  Redeem yourself now before our Lord, before it is too late!'
    donate_zh = '请立即向本教会捐助，并领取<a href="book.html"><u>《逾越天使之书》</u></a>以了解更多。趁还来得及，在主面前赎回自己！'
    html = html.replace(
        f"<p>\n                                        {donate_en}\n                                    </p>",
        wrap_block(f"<p>\n                                        {donate_en}\n                                    </p>", f"<p>\n                                        {donate_zh}\n                                    </p>"),
    )
    return html


def patch_book(html: str) -> str:
    html = html.replace(
        "<h2 class=\"section-title\">The Book of the Passover Angel</h2>",
        f"<h2 class=\"section-title\">{wrap_pair('The Book of the Passover Angel', '《逾越天使之书》')}</h2>",
    )
    p1_en = "The Rapture is soon come. Only those who repent before Our Lord will be redeemed. But do not be fooled by the churches preaching the deception of John. The world will be redeemed without Revelation. Sin will be removed from the earth as it was in Egypt before the Exodus. When the stars are right, the Pharaoh will once again pay! Donate to our Church below and we will send you this beautiful book, outlining the truth in the Scripture as revealed to our Reverend Balfour by God’s Own Angel."
    p1_zh = "被提即将来临。唯有在主面前悔改者才能得赎。勿被那些传讲约翰迷惑的教会所欺。世界将在无需《启示录》的情况下得赎。罪恶将如出埃及前在埃及地那样从地上除去。当星辰归位，法老将再次付出代价！请向本教会捐助，我们将寄赠此书，其中载有上帝的天使向鲍尔弗牧师所启示的圣经真理。"
    p2_en = "We are a small church that lives on the donations of our flock. We thank you so much for your continued support.  Know that the time is coming when we will do away with these false idols of money and material goods and live in together in the Kingdom. This is a small price to pay for the salvation when weighed against that of your immortal soul."
    p2_zh = "我们是一座依靠会众捐献维持的小教会，衷心感谢您的持续支持。要知道，废除金钱与物质这些虚假偶像、同住在国度里的日子即将来临。与不朽灵魂得救相比，这不过是微不足道的代价。"
    html = html.replace(
        f'<div class="news">\n                                    {p1_en}\n                                </div>',
        f'<div class="news">\n                                    {wrap_block(p1_en, p1_zh)}\n                                </div>',
    )
    html = html.replace(
        f'<div class="news">\n                                    {p2_en}\n                                </div>',
        f'<div class="news">\n                                    {wrap_block(p2_en, p2_zh)}\n                                </div>',
    )
    html = html.replace(
        "<strong>Donate $29.95 or more now</strong>",
        f"<strong>{wrap_pair('Donate $29.95 or more now', '立即捐助 29.95 美元或以上', True)}</strong>",
    )
    return html


def patch_sermon_titles(html: str) -> str:
    html = html.replace(
        "<h2 class=\"section-title text-center\">Sermons From Reverend Balfour</h2>",
        f"<h2 class=\"section-title text-center\">{wrap_pair('Sermons From Reverend Balfour', '鲍尔弗牧师讲道')}</h2>",
    )
    titles = [
        ("The Sun Darkens - 14 aug", "太阳变暗 - 8月14日"),
        ("Satan’s Control of U.S. Government - 24 mar", "撒旦对美国政府的控制 - 3月24日"),
        ("Angels of Vengeance - 01 jan", "复仇天使 - 1月1日"),
        ("New World Disorder - 25 jul", "新世界失序 - 7月25日"),
        ("The Judge is At the Door - 09 nov", "审判者已在门前 - 11月9日"),
        ("Annointed By God - 22 jan", "受上帝膏抹 - 1月22日"),
        ("The Time Has Come! - 26 jun", "时候已到！ - 6月26日"),
    ]
    for en, zh in titles:
        if wrap_pair(en, zh, True) in html:
            continue
        html = re.sub(
            rf">{re.escape(en)}\s*<span class=\"year",
            f">{wrap_pair(en, zh, True)} <span class=\"year",
            html,
        )
    return html


def main():
    zh_map = json.loads((ROOT / "scripts" / "sermon_plain_zh.json").read_text(encoding="utf-8"))

    for fname in ["index.html", "about.html", "book.html", "sermons.html"]:
        path = ROOT / fname
        html = path.read_text(encoding="utf-8")
        html = patch_title(html)
        html = patch_header(html)
        html = patch_footer(html)
        html = add_scripts(html)
        html = patch_form_script(html)
        if fname == "index.html":
            html = patch_index(html)
        elif fname == "about.html":
            html = patch_about(html)
        elif fname == "book.html":
            html = patch_book(html)
        elif fname == "sermons.html":
            html = patch_sermon_titles(html)
            html = patch_sermon_paragraphs(html, zh_map)
        path.write_text(html, encoding="utf-8")
        print("patched", fname)


if __name__ == "__main__":
    main()
