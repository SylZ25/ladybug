#!/usr/bin/env python3
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

FOOTER_BAD = re.compile(
    r'<div class="lang-en">(?:<div class="lang-en">)+<p>There is but one Church.*?</div>(?:<div class="lang-zh"><p>人只得在一个教会里得救.*?</p></div>)+',
    re.S,
)
FOOTER_GOOD = (
    '<div class="lang-en"><p>There is but one Church in which men find salvation, '
    'just as outside the ark of Noah it was not possible for anyone to be saved. (Thomas Aquinas)</p></div>'
    '<div class="lang-zh"><p>人只得在一个教会里得救，正如在挪亚方舟之外，无人能得救。（托马斯·阿奎那）</p></div>'
)

VERSE_BAD = re.compile(
    r'<div class="lang-en">(?:<div class="lang-en">)+<p class="news news-title text-center">.*?</div>(?:<div class="lang-zh"><p class="news news-title text-center">.*?</p></div>)+',
    re.S,
)
VERSE_GOOD = (
    '<div class="lang-en"><p class="news news-title text-center">\n'
    '                        For I will pass through the land of Egypt this night,<br>\n'
    '                        and will smite all the firstborn in the land of Egypt, both man and beast;<br>\n'
    '                        and against all the gods of Egypt I will execute judgment: <br>\n'
    '                        I <i>am</i> the LORD.\n'
    '                    </p></div>'
    '<div class="lang-zh"><p class="news news-title text-center">\n'
    '                        因我今夜要行经埃及全地，把埃及地一切头生的，无论是人是牲畜，都击杀了；<br>\n'
    '                        又要败坏埃及一切的神。<br>\n'
    '                        我乃是耶和华。\n'
    '                    </p></div>'
)

ABOUT_NEWS = """                                <div class="news">
                                    <div class="lang-en"><p>
                                        We are a small, non-denominational, fundamentalist Church devoted to total submission to the will of God and his herald, the Passover Angel.
                                    </p></div><div class="lang-zh"><p>
                                        我们是一座小型、非宗派、基要主义的教会，全然顺服上帝的旨意及其使者逾越节天使。
                                    </p></div>
                                    <div class="lang-en"><p>
                                        We believe that the End Times are near. Soon God will return to the world, through his messenger the Passover Angel, in order to cleanse the world of sin and restore righteousness through the Rapture.
                                    </p></div><div class="lang-zh"><p>
                                        我们相信末世已近。上帝不久将借其使者逾越节天使重返世界，洁净罪恶，并通过被提恢复公义。
                                    </p></div>
                                    <div class="lang-en"><p>
                                        Many churches will tell you that the Rapture was foretold by John in the Book of Revelations, but they are deceived. Only those who follow the true words of God's Angel will be redeemed, and so we must all repent if we hope to be saved.
                                    </p></div><div class="lang-zh"><p>
                                        许多教会告诉你被提已在《启示录》中由约翰预言，但他们受了迷惑。唯有听从上帝天使真实话语者才能得赎，因此我们若盼望得救，都必须悔改。
                                    </p></div>
                                    <div class="lang-en"><p>
                                        Donate to our Church now and receive <a href="book.html"><u>The Book of the Passover Angel</u></a> to learn more.  Redeem yourself now before our Lord, before it is too late!
                                    </p></div><div class="lang-zh"><p>
                                        请立即向本教会捐助，并领取<a href="book.html"><u>《逾越节天使之书》</u></a>以了解更多。趁还来得及，在主面前赎回自己！
                                    </p></div>
                                    <div class="lang-en"><p>
                                        "Boast not thyself of to morrow; for thou knowest not what a day may bring forth." (Proverbs 27:1)
                                    </p></div><div class="lang-zh"><p>
                                        「不要为明日自夸，因为一日要生何事，你尚且不能知道。」（箴言 27:1）
                                    </p></div>
                                </div>"""

BOOK_P1 = """                                <div class="news">
                                    <div class="lang-en">The Rapture is soon come. Only those who repent before Our Lord will be redeemed. But do not be fooled by the churches preaching the deception of John. The world will be redeemed without Revelation. Sin will be removed from the earth as it was in Egypt before the Exodus. When the stars are right, the Pharaoh will once again pay! Donate to our Church below and we will send you this beautiful book, outlining the truth in the Scripture as revealed to our Reverend Balfour by God's Own Angel.</div><div class="lang-zh">被提即将来临。唯有在主面前悔改者才能得赎。勿被那些传讲约翰迷惑的教会所欺。世界将在无需《启示录》的情况下得赎。罪恶将如出埃及前在埃及地那样从地上除去。当星辰归位，法老将再次付出代价！请向本教会捐助，我们将寄赠此书，其中载有上帝的天使向鲍尔弗牧师所启示的圣经真理。</div>
                                </div>"""


def fix_about(html):
    m = re.search(r'<div class="news">.*?</div>\s*</div>\s*</div>\s*</div> <!-- \.row -->', html, re.S)
    if not m:
        return html
    return html[: m.start()] + ABOUT_NEWS + "\n                            " + html[m.end() - len("                            </div>\n                        </div> <!-- .row -->") :]


def fix_book(html):
    html = re.sub(
        r'<div class="news">\s*The Rapture is soon come\..*?</div>\s*</div>\s*<div class="col-md-12 col-sm-6">\s*<image',
        BOOK_P1 + "\n                            </div>\n                            <div class=\"col-md-12 col-sm-6\">\n                                    <image",
        html,
        count=1,
        flags=re.S,
    )
    html = re.sub(r'(data-alt-en="Donate" data-alt-zh="捐助")\s*(?:\1\s*)+', r'\1 ', html)
    return html


def main():
    for fname in ["index.html", "about.html", "book.html", "sermons.html"]:
        path = ROOT / fname
        html = path.read_text(encoding="utf-8")
        html = FOOTER_BAD.sub(FOOTER_GOOD, html)
        if fname == "index.html":
            html = VERSE_BAD.sub(VERSE_GOOD, html)
        if fname == "about.html":
            html = fix_about(html)
        if fname == "book.html":
            html = fix_book(html)
        path.write_text(html, encoding="utf-8")
        print("fixed", fname)


if __name__ == "__main__":
    main()
