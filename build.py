#!/usr/bin/env python3
# BeterBody.nl static site generator
# Output: schone URL-structuur met map/index.html, klaar voor Cloudflare Pages.
import os, json, html, shutil

BASE = "https://beterbody.nl"
SITE = "BeterBody"
OUT = os.path.join(os.path.dirname(__file__), "site")
SRC = os.path.dirname(__file__)

NAV = [
    ("Home", "/"),
    ("Nieuws", "/nieuws/"),
    ("Recepten", "/recepten/"),
    ("Over", "/over/"),
    ("Partners", "/partners/"),
    ("Contact", "/contact/"),
]

LEAF = ('<svg class="leaf" viewBox="0 0 32 32" fill="none" aria-hidden="true">'
        '<path d="M16 29C16 20 16 13 16 6" stroke="currentColor" stroke-width="2.4" stroke-linecap="round"/>'
        '<path d="M16 12C12 11 9 12.5 7 16C11 17 14 16 16 12Z" fill="currentColor"/>'
        '<path d="M16 9C20 8 23 9.5 25 13C21 14 18 13 16 9Z" fill="currentColor"/>'
        '<path d="M16 17C13 16.5 10.5 17.7 9 20.5C12.2 21.3 14.6 20.4 16 17Z" fill="currentColor"/></svg>')

ICON_LEAF_BIG = ('<svg viewBox="0 0 32 32" fill="none" aria-hidden="true">'
                 '<path d="M16 29C16 20 16 13 16 6" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/>'
                 '<path d="M16 12C12 11 9 12.5 7 16C11 17 14 16 16 12Z" fill="currentColor"/>'
                 '<path d="M16 9C20 8 23 9.5 25 13C21 14 18 13 16 9Z" fill="currentColor"/>'
                 '<path d="M16 17C13 16.5 10.5 17.7 9 20.5C12.2 21.3 14.6 20.4 16 17Z" fill="currentColor"/></svg>')

ARROW = '<svg viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>'

ORG_JSONLD = {
    "@type": "Organization",
    "@id": BASE + "/#organisatie",
    "name": SITE,
    "url": BASE + "/",
    "logo": {"@type": "ImageObject", "url": BASE + "/assets/icons/logo-mark.png", "width": 512, "height": 512},
    "description": "Nederlands blog over een gezonde leefstijl en fitness.",
    "email": "info@beterbody.nl",
}

PERSON_JSONLD = {
    "@type": "Person",
    "@id": BASE + "/over-de-schrijfster/#maud",
    "name": "Maud Brinkman",
    "url": BASE + "/over-de-schrijfster/",
    "jobTitle": "Leefstijl- en gezondheidsschrijver",
    "image": BASE + "/assets/img/maud-avatar.svg",
    "worksFor": {"@id": BASE + "/#organisatie"},
}


def esc(s):
    return html.escape(s, quote=True)


def head(title, desc, path, jsonld=None, og_image="/assets/img/og-default.png", article=False):
    canonical = BASE + path
    blocks = ""
    if jsonld:
        if isinstance(jsonld, dict):
            jsonld = [jsonld]
        for obj in jsonld:
            blocks += '<script type="application/ld+json">' + json.dumps(obj, ensure_ascii=False) + '</script>\n'
    return f"""<!doctype html>
<html lang="nl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="{canonical}">
<meta name="robots" content="index, follow, max-image-preview:large">
<meta property="og:type" content="{'article' if article else 'website'}">
<meta property="og:locale" content="nl_NL">
<meta property="og:site_name" content="{SITE}">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{BASE}{og_image}">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="/assets/icons/logo-mark.png" sizes="any">
<link rel="apple-touch-icon" href="/assets/icons/logo-mark.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,400..600;1,9..144,400..500&family=Mulish:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/css/style.css">
{blocks}</head>
<body>
"""


def header(current):
    links = ""
    for label, href in NAV:
        cur = ' aria-current="page"' if href == current else ""
        links += f'<li><a href="{href}"{cur}>{label}</a></li>'
    return f"""<header class="site-header">
  <nav class="nav" aria-label="Hoofdmenu">
    <a class="brand" href="/">{LEAF}<span>Beter<b>Body</b></span></a>
    <button class="nav-toggle" aria-expanded="false" aria-controls="menu" aria-label="Menu openen">
      <svg viewBox="0 0 24 24" fill="none"><path d="M4 7h16M4 12h16M4 17h16" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>
    </button>
    <ul class="nav-links" id="menu">{links}</ul>
  </nav>
</header>
<main>
"""


def footer():
    return f"""</main>
<footer class="site-footer">
  <div class="wrap">
    <div class="footer-grid">
      <div>
        <a class="brand" href="/">{LEAF}<span>Beter<b>Body</b></span></a>
        <p>Blog over een gezonde leefstijl en fitness. Praktische artikelen over voeding, beweging en gewoontes die vol te houden zijn.</p>
      </div>
      <div>
        <h4>Lezen</h4>
        <ul>
          <li><a href="/nieuws/">Nieuws</a></li>
          <li><a href="/recepten/">Recepten</a></li>
          <li><a href="/over/">Over BeterBody</a></li>
          <li><a href="/over-de-schrijfster/">Over de schrijfster</a></li>
        </ul>
      </div>
      <div>
        <h4>Info</h4>
        <ul>
          <li><a href="/partners/">Partners</a></li>
          <li><a href="/contact/">Contact</a></li>
          <li><a href="/privacybeleid/">Privacybeleid</a></li>
          <li><a href="/cookiebeleid/">Cookiebeleid</a></li>
        </ul>
      </div>
    </div>
    <div class="footer-bottom">
      <span>&copy; 2026 {SITE}. Alle rechten voorbehouden.</span>
      <span><a href="/over/">Over BeterBody</a> &middot; <a href="/contact/">Contact</a></span>
    </div>
  </div>
</footer>
<script>
(function(){{
  var t=document.querySelector('.nav-toggle'),m=document.getElementById('menu');
  if(t&&m){{t.addEventListener('click',function(){{var o=m.classList.toggle('open');t.setAttribute('aria-expanded',o);}});}}
}})();
</script>
</body>
</html>"""


def write(path, content):
    if path == "/":
        full = os.path.join(OUT, "index.html")
    else:
        full = os.path.join(OUT, path.strip("/"), "index.html")
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(content)


def breadcrumb(items):
    # items: list of (name, path)
    el = []
    for i, (name, p) in enumerate(items, 1):
        el.append({"@type": "ListItem", "position": i, "name": name, "item": BASE + p})
    return {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": el}


def crumbs_html(items):
    parts = []
    for i, (name, p) in enumerate(items):
        if i < len(items) - 1:
            parts.append(f'<a href="{p}">{name}</a>')
        else:
            parts.append(f'<span>{name}</span>')
    return '<nav class="crumbs wrap" aria-label="Kruimelpad">' + ' / '.join(parts) + '</nav>'


# ----------------------------------------------------------------------------
# ARTICLES
# ----------------------------------------------------------------------------
ARTICLES = [
    {
        "slug": "streng-dieet-werkt-zelden",
        "tag": "Voeding",
        "title": "Waarom een streng dieet zelden blijft werken",
        "desc": "Een streng dieet levert snel resultaat op, maar houdt zelden stand. Een aanpak die vol te houden is, werkt op lange termijn beter.",
        "date": "2026-02-04",
        "intro": "Ik heb de meeste crashdiëten zelf geprobeerd. Het patroon was elke keer hetzelfde: een paar weken streng volhouden, daarna terugvallen en de kilo's weer aankomen.",
        "body": [
            ("h2", "Snel resultaat is meestal tijdelijk"),
            ("p", "Een streng dieet belooft veel in korte tijd. De eerste kilo's gaan er ook vaak vlot af, deels door verlies van vocht. Het probleem zit in het vervolg. Een aanpak met weinig eten en veel verboden is moeilijk lang vol te houden, en zodra het oude eetpatroon terugkomt, komt het gewicht meestal mee terug."),
            ("h2", "Volhouden is belangrijker dan streng zijn"),
            ("p", "Blijvend resultaat hangt niet af van de strengste week, maar van wat na een jaar nog overeind staat. Een eetpatroon dat past bij het dagelijks leven, met genoeg variatie en zonder constant honger, is makkelijker vast te houden dan een kort en hard regime."),
            ("p", "Daar hoort ook bij dat af en toe iets lekkers mogelijk blijft. Een aanpak die niets toestaat, leidt eerder tot een terugval dan een aanpak met ruimte."),
            ("callout", "Wie zoekt naar een opbouw zonder streng dieet, vindt bij <slinc href='https://rachelhulshof.nl/afvallen-zonder-dieet' anchor='afvallen zonder dieet'></slinc> een uitgewerkt voorbeeld van die gedachte: gewoon eten, met regelmaat over de dag."),
            ("h2", "Drie dingen die wel houdbaar zijn"),
            ("ul", [
                "Regelmatig eten over de dag, zodat grote trek minder kans krijgt.",
                "Genoeg eiwit en vezels, voor een langer verzadigd gevoel.",
                "Dagelijks wat beweging, los van een sportschool.",
            ]),
            ("p", "Deze drie gewoontes vragen geen wilskracht voor twee weken, maar passen in een gewoon weekschema. Meer hierover staat in het artikel over <link href='/nieuws/vezels-en-verzadiging/' anchor='vezels en verzadiging'></link> en in dat over <link href='/nieuws/dagelijks-bewegen/' anchor='dagelijks bewegen'></link>."),
        ],
        "faq": [
            ("Hoe snel mag gewicht eraf?", "Een geleidelijk tempo is beter vol te houden dan een snelle daling. Wie langzaam afbouwt, behoudt meer spiermassa en loopt minder kans op een terugval."),
            ("Waarom kom ik na een dieet weer aan?", "Een streng dieet is moeilijk lang vol te houden. Zodra het oude patroon terugkeert, keert het gewicht meestal mee terug. Een vol te houden aanpak voorkomt dat."),
            ("Helpt minder eten altijd?", "Heel weinig eten is zelden lang vol te houden en leidt vaak tot eetbuien. Genoeg en gevarieerd eten werkt op lange termijn beter."),
        ],
        "related": ["jojo-effect-voorkomen", "eiwitten-en-spiermassa"],
    },
    {
        "slug": "vezels-en-verzadiging",
        "tag": "Voeding",
        "title": "Vezels en een langer verzadigd gevoel",
        "desc": "Vezels zorgen voor een langer verzadigd gevoel en een soepele spijsvertering. Een overzicht van vezelrijke producten en wat ze doen.",
        "date": "2026-02-18",
        "intro": "Vezels horen bij de minst spannende onderwerpen rond voeding, en tegelijk bij de meest praktische. Ze maken het makkelijker om met minder moeite verzadigd te blijven.",
        "body": [
            ("h2", "Wat vezels doen"),
            ("p", "Vezels zijn delen van plantaardig voedsel die het lichaam niet volledig verteert. Ze geven volume aan een maaltijd, vragen meer kauwwerk en zorgen voor een geleidelijke overgang van voedsel door het darmkanaal. Het gevolg is een verzadigd gevoel dat langer aanhoudt."),
            ("h2", "Waar vezels in zitten"),
            ("ul", [
                "Groente, van rauwkost tot gestoofde groenten bij het avondeten.",
                "Volkoren producten zoals volkorenbrood, volkoren pasta en zilvervliesrijst.",
                "Peulvruchten zoals linzen, kikkererwten en bonen.",
                "Fruit met schil, en noten in een kleine portie.",
            ]),
            ("p", "Een eenvoudige stap is om bij elke maaltijd iets met vezels toe te voegen. Een handvol groente bij de lunch of een portie peulvruchten bij het avondeten telt al snel op."),
            ("h2", "Vezels en de bloedsuikerspiegel"),
            ("p", "Vezelrijke producten worden langzamer opgenomen dan snelle suikers. Daardoor blijft de bloedsuikerspiegel stabieler, zonder grote pieken en dalen. Dat helpt om tussendoor minder snel trek te krijgen."),
            ("callout", "Een eetschema dat draait om regelmaat en vezelrijke keuzes is terug te zien in <slinc href='https://rachelhulshof.nl/gezond-afvallen/' anchor='de visie van Slinc op gezond afvallen'></slinc>."),
        ],
        "faq": [
            ("Hoeveel vezels per dag is genoeg?", "Voor volwassenen wordt ongeveer dertig tot veertig gram per dag aangeraden. Veel mensen halen dat niet en kunnen dus wat meer groente en volkoren producten toevoegen."),
            ("Maakt veel groente eten een verschil?", "Groente bevat veel vezels en weinig calorieën. Meer groente op het bord betekent meer volume en verzadiging zonder veel extra calorieën."),
            ("Zijn vezels uit fruit ook goed?", "Ja. Fruit met schil levert vezels en houdt langer verzadigd dan vruchtensap, dat de vezels mist."),
        ],
        "related": ["streng-dieet-werkt-zelden", "eiwitten-en-spiermassa"],
    },
    {
        "slug": "eiwitten-en-spiermassa",
        "tag": "Voeding",
        "title": "Eiwitten en behoud van spiermassa bij afvallen",
        "desc": "Genoeg eiwit helpt om spiermassa te behouden tijdens het afvallen en geeft een verzadigd gevoel. Een praktisch overzicht.",
        "date": "2026-03-05",
        "intro": "Wie afvalt wil vooral vet kwijt, geen spieren. Eiwit speelt daarin een grotere rol dan veel mensen denken.",
        "body": [
            ("h2", "Waarom eiwit telt"),
            ("p", "Eiwitten zijn de bouwstenen van spieren. Tijdens het afvallen krijgt het lichaam minder energie binnen dan het verbruikt. Met genoeg eiwit blijft de spiermassa beter behouden en haalt het lichaam de energie eerder uit vetreserves."),
            ("p", "Spiermassa verbruikt bovendien meer energie dan vet. Behoud van spieren helpt daarom om de stofwisseling op peil te houden."),
            ("h2", "Eiwit en verzadiging"),
            ("p", "Eiwitrijke maaltijden geven een sterker verzadigd gevoel dan maaltijden met vooral snelle koolhydraten. Dat maakt het makkelijker om met een kleinere portie tevreden te zijn."),
            ("h2", "Goede bronnen van eiwit"),
            ("ul", [
                "Magere zuivel zoals kwark en yoghurt.",
                "Eieren, kip, vis en mager vlees.",
                "Peulvruchten en tofu voor plantaardige maaltijden.",
                "Een kleine portie noten als tussendoortje.",
            ]),
            ("callout", "Een programma dat eiwit bewust inzet voor behoud van spiermassa is terug te lezen bij <slinc href='https://rachelhulshof.nl/supplementen-afvallen/' anchor='Slinc Shaper en Fit'></slinc>."),
        ],
        "faq": [
            ("Hoeveel eiwit is nodig bij afvallen?", "Tijdens het afvallen is wat meer eiwit nuttig om spiermassa te behouden. Een bron van eiwit bij elke maaltijd is een praktische richtlijn."),
            ("Behoud ik spieren zonder sporten?", "Genoeg eiwit helpt, maar enige beweging of krachtinspanning ondersteunt het behoud van spiermassa extra."),
            ("Zijn eiwitshakes nodig?", "Niet per se. De meeste mensen halen genoeg eiwit uit gewone voeding zoals zuivel, eieren, vis en peulvruchten."),
        ],
        "related": ["streng-dieet-werkt-zelden", "vezels-en-verzadiging"],
    },
    {
        "slug": "dagelijks-bewegen",
        "tag": "Fitness",
        "title": "Elke dag een halfuur bewegen, zonder sportschool",
        "desc": "Dagelijks bewegen hoeft geen sportschool te vereisen. Wandelen, fietsen en huishouden tellen allemaal mee.",
        "date": "2026-03-20",
        "intro": "Bewegen klinkt voor veel mensen als sporten, en sporten klinkt als iets waar tijd, geld en motivatie voor nodig zijn. Dat hoeft niet zo te zijn.",
        "body": [
            ("h2", "Alles telt mee"),
            ("p", "Een halfuur bewegen per dag draagt bij aan een betere gezondheid, en dat halfuur hoeft niet in een sportschool plaats te vinden. Wandelen, fietsen naar het werk, traplopen en stevig huishouden tellen allemaal mee."),
            ("h2", "Waarom dagelijks beter werkt"),
            ("p", "Een gewoonte die elke dag terugkomt, vraagt minder wilskracht dan een zware training die soms wel en soms niet doorgaat. Een vaste wandeling na het avondeten is makkelijker vol te houden dan een ambitieus sportschema."),
            ("ul", [
                "Een wandeling van twintig tot dertig minuten.",
                "De fiets in plaats van de auto voor korte ritten.",
                "De trap nemen waar dat kan.",
                "Een keer per week iets actievers, zoals zwemmen of fietsen.",
            ]),
            ("h2", "Bewegen en eten in balans"),
            ("p", "Meer bewegen vraagt om voldoende voeding. Wie actiever wordt, hoeft niet minder te eten, maar juist genoeg om het lichaam van energie te voorzien. Meer hierover staat in het artikel over <link href='/nieuws/streng-dieet-werkt-zelden/' anchor='een streng dieet'></link>."),
            ("callout", "Beweging in combinatie met een regelmatig eetritme is de basis van <slinc href='https://rachelhulshof.nl/afvallen-met-slinc/' anchor='afvallen met Slinc'></slinc>."),
        ],
        "faq": [
            ("Is wandelen genoeg om fit te blijven?", "Dagelijks stevig wandelen draagt veel bij aan de algehele gezondheid. Voor extra resultaat helpt het om af en toe iets actievers toe te voegen."),
            ("Hoeveel beweging per dag is aan te raden?", "Een richtlijn is minstens een halfuur matige beweging per dag. Dat mag opgeteld worden uit kortere stukken."),
            ("Moet ik naar de sportschool?", "Nee. Een sportschool kan prettig zijn, maar is niet nodig. Alledaagse beweging telt net zo goed mee."),
        ],
        "related": ["jojo-effect-voorkomen", "streng-dieet-werkt-zelden"],
    },
    {
        "slug": "jojo-effect-voorkomen",
        "tag": "Leefstijl",
        "title": "Het jojo-effect voorkomen na een dieet",
        "desc": "Na een dieet komen de kilo's vaak terug. Met een stapsgewijze opbouw en houdbare gewoontes blijft het gewicht beter stabiel.",
        "date": "2026-04-08",
        "intro": "Afvallen lukt veel mensen wel. Het lastige deel komt erna: het gewicht eraf houden. Dat heen en weer gaan heet het jojo-effect.",
        "body": [
            ("h2", "Hoe het jojo-effect ontstaat"),
            ("p", "Het jojo-effect komt meestal door een te streng dieet dat niet vol te houden is. Na afloop keert het oude eetpatroon terug, en daarmee het gewicht. Soms komt er zelfs meer bij dan eraf ging."),
            ("h2", "Een geleidelijke overgang"),
            ("p", "De stap van een dieet naar gewoon eten gaat het beste in fases. In plaats van direct terug naar het oude patroon, helpt een geleidelijke opbouw waarin meer volwaardige producten een plek krijgen, met behoud van regelmaat."),
            ("p", "Slinc werkt dit principe uit met een opbouw na de eerste fase, waarin het eetpatroon stap voor stap ruimer wordt. Meer daarover staat bij <slinc href='https://rachelhulshof.nl/afvallen-met-slinc/' anchor='de aanpak van Slinc'></slinc>."),
            ("figure", "/assets/img/slinc-fase2-fase3.webp", "Slinc fase 2 en fase 3 met Shaper, Fit en Balance", "De opbouw van Slinc verloopt in fases, van stabiliseren naar balans."),
            ("h2", "Gewoontes die het gewicht stabiel houden"),
            ("ul", [
                "Blijf regelmatig eten, ook na het afvallen.",
                "Houd genoeg eiwit en vezels in het eetpatroon.",
                "Blijf dagelijks bewegen.",
                "Sta af en toe iets lekkers toe, zonder het patroon los te laten.",
            ]),
            ("p", "Deze gewoontes sluiten aan bij wat er staat over <link href='/nieuws/eiwitten-en-spiermassa/' anchor='eiwitten en spiermassa'></link> en over <link href='/nieuws/dagelijks-bewegen/' anchor='dagelijks bewegen'></link>."),
        ],
        "faq": [
            ("Waarom kom ik na een dieet weer aan?", "Meestal omdat het dieet te streng was om vol te houden. Een zorgvuldige opbouw en houdbare gewoontes voorkomen dat het gewicht terugkomt."),
            ("Hoe houd ik mijn gewicht stabiel?", "Met regelmaat, genoeg eiwit en vezels, dagelijkse beweging en ruimte voor af en toe iets lekkers."),
            ("Is een onderhoudsfase nodig?", "Een geleidelijke overgang van afvallen naar onderhoud helpt om het jojo-effect te voorkomen."),
        ],
        "related": ["streng-dieet-werkt-zelden", "dagelijks-bewegen"],
    },
]

ART_BY_SLUG = {a["slug"]: a for a in ARTICLES}


def render_slinc(href, anchor):
    return f'<a href="{href}" target="_blank" rel="noopener sponsored">{anchor}</a>'


def render_link(href, anchor):
    return f'<a href="{href}">{anchor}</a>'


def render_block(b):
    kind = b[0]
    if kind == "h2":
        return f"<h2>{b[1]}</h2>"
    if kind == "h3":
        return f"<h3>{b[1]}</h3>"
    if kind == "p":
        return f"<p>{expand(b[1])}</p>"
    if kind == "ul":
        items = "".join(f"<li>{expand(i)}</li>" for i in b[1])
        return f"<ul>{items}</ul>"
    if kind == "callout":
        return f'<div class="callout"><p>{expand(b[1])}</p></div>'
    if kind == "figure":
        _, src, alt, cap = b
        return f'<figure><img src="{src}" alt="{esc(alt)}" loading="lazy"><figcaption>{esc(cap)}</figcaption></figure>'
    return ""


def expand(text):
    # replace <slinc href='..' anchor='..'></slinc> and <link .../>
    import re
    def slinc_sub(m):
        return render_slinc(m.group(1), m.group(2))
    def link_sub(m):
        return render_link(m.group(1), m.group(2))
    text = re.sub(r"<slinc href='([^']+)' anchor='([^']+)'></slinc>", slinc_sub, text)
    text = re.sub(r"<link href='([^']+)' anchor='([^']+)'></link>", link_sub, text)
    return text


def nl_date(iso):
    months = ["januari","februari","maart","april","mei","juni","juli","augustus","september","oktober","november","december"]
    y,m,d = iso.split("-")
    return f"{int(d)} {months[int(m)-1]} {y}"


def article_page(a):
    path = f"/nieuws/{a['slug']}/"
    crumbs = [("Home","/"),("Nieuws","/nieuws/"),(a["title"],path)]
    body_html = "".join(render_block(b) for b in a["body"])
    # faq
    faq_html = ""
    faq_ld = None
    if a.get("faq"):
        items = "".join(
            f'<details><summary>{q}</summary><p>{expand(ans)}</p></details>' for q,ans in a["faq"]
        )
        faq_html = f'<h2>Veelgestelde vragen</h2><div class="faq">{items}</div>'
        faq_ld = {
            "@context":"https://schema.org","@type":"FAQPage",
            "mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":strip_tags(expand(ans))}} for q,ans in a["faq"]]
        }
    # related
    rel_html = ""
    if a.get("related"):
        cards = ""
        for slug in a["related"]:
            r = ART_BY_SLUG[slug]
            cards += card_html(r)
        rel_html = f'<section class="section tight cream"><div class="wrap"><h2>Verder lezen</h2><div class="cards">{cards}</div></div></section>'

    article_ld = {
        "@context":"https://schema.org","@type":"BlogPosting",
        "mainEntityOfPage":{"@type":"WebPage","@id":BASE+path},
        "headline":a["title"],"description":a["desc"],
        "image":BASE+"/assets/img/og-default.png",
        "datePublished":a["date"]+"T08:00:00+01:00","dateModified":a["date"]+"T08:00:00+01:00",
        "author":{"@type":"Person","name":"Maud Brinkman","url":BASE+"/over-de-schrijfster/"},
        "publisher":ORG_JSONLD,
        "articleSection":a["tag"],"inLanguage":"nl-NL",
    }
    ld = [article_ld, breadcrumb(crumbs)]
    if faq_ld: ld.append(faq_ld)

    h = head(f"{a['title']} | {SITE}", a["desc"], path, ld, article=True)
    h += header("/nieuws/")
    h += crumbs_html(crumbs)
    h += f"""<article class="article">
  <div class="wrap narrow">
    <span class="eyebrow">{LEAF}{a['tag']}</span>
    <h1>{a['title']}</h1>
    <p class="lead">{esc(a['desc'])}</p>
    <div class="byline">
      <img src="/assets/img/maud-avatar.svg" alt="Maud Brinkman" width="52" height="52">
      <div><b>Maud Brinkman</b><span>{nl_date(a['date'])}</span></div>
    </div>
    <p>{expand(a['intro'])}</p>
    {body_html}
    {faq_html}
  </div>
</article>
{rel_html}"""
    h += footer()
    write(path, h)


def card_html(a):
    return f"""<a class="card" href="/nieuws/{a['slug']}/">
  <div class="thumb">{ICON_LEAF_BIG}</div>
  <div class="body">
    <span class="tag">{a['tag']}</span>
    <h3>{a['title']}</h3>
    <p>{esc(a['desc'])}</p>
    <span class="more">Lees verder &rsaquo;</span>
  </div>
</a>"""


def strip_tags(s):
    import re
    return re.sub(r"<[^>]+>", "", s)


# ----------------------------------------------------------------------------
# HOMEPAGE
# ----------------------------------------------------------------------------
def home():
    path = "/"
    website_ld = {
        "@context":"https://schema.org","@type":"WebSite","@id":BASE+"/#website",
        "url":BASE+"/","name":SITE,"inLanguage":"nl-NL","publisher":{"@id":BASE+"/#organisatie"},
        "description":"Nederlands blog over een gezonde leefstijl en fitness.",
    }
    org_ld = dict(ORG_JSONLD); org_ld["@context"]="https://schema.org"

    latest = "".join(card_html(a) for a in ARTICLES[:3])

    h = head(
        f"{SITE} | Blog over een gezonde leefstijl en fitness",
        "Praktische artikelen over voeding, beweging en een leefstijl die vol te houden is. Met recepten en tips voor een betere body.",
        path, [website_ld, org_ld]
    )
    h += header("/")
    h += f"""<section class="hero">
  <div class="wrap hero-grid">
    <div>
      <span class="eyebrow">{LEAF}Gezonde leefstijl en fitness</span>
      <h1>Een <em>betere body</em> begint bij gewoon eten</h1>
      <p class="lead">BeterBody verzamelt praktische, vol te houden manieren om fitter te worden. Geen crashdieet, geen honger, wel resultaat dat blijft.</p>
      <div class="hero-actions">
        <a class="btn btn-primary" href="/nieuws/">Lees de artikelen</a>
        <a class="btn btn-ghost" href="/recepten/">Bekijk de recepten</a>
      </div>
    </div>
    <div class="hero-media">
      <div class="frame"><img src="/assets/img/leefstijl-hormonen.webp" alt="Slinc supplementen op een aanrecht in een lichte keuken" width="600" height="600"></div>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="section-head">
      <span class="eyebrow">{LEAF}Van het blog</span>
      <h2>Nieuwste artikelen</h2>
      <p>Praktische stukken over voeding, beweging en een leefstijl die vol te houden is.</p>
    </div>
    <div class="cards">{latest}</div>
    <p style="margin-top:28px"><a class="btn btn-ghost" href="/nieuws/">Alle artikelen</a></p>
  </div>
</section>

<section class="section mint">
  <div class="wrap">
    <div class="slinc">
      <div>
        <span class="eyebrow">{LEAF}Aanbevolen</span>
        <h2>De aanpak die wij aanraden</h2>
        <p>Voor wie liever met een uitgewerkt programma werkt, is Slinc een goede optie. Het draait om afvallen met gewoon eten, met regelmaat over de dag en zonder streng dieet.</p>
        <ul>
          <li>{LEAF}<span>Gewoon eten uit de supermarkt, ook samen met het gezin.</span></li>
          <li>{LEAF}<span>Een duidelijk eetschema met vaste momenten.</span></li>
          <li>{LEAF}<span>Een opbouw die het jojo-effect helpt voorkomen.</span></li>
        </ul>
        <a class="btn btn-primary" href="https://rachelhulshof.nl/afvallen-met-slinc/" target="_blank" rel="noopener sponsored">Lees meer over Slinc {ARROW}</a>
      </div>
      <div class="slinc-media">
        <img src="/assets/img/slinc-shaper-fit.jpg" alt="Verpakkingen van Slinc Shaper en Slinc Fit" width="1080" height="1080">
      </div>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="author-card">
      <img src="/assets/img/maud-avatar.svg" alt="Maud Brinkman, schrijfster van BeterBody" width="160" height="160">
      <div>
        <div class="role">De schrijfster</div>
        <h3>Maud Brinkman</h3>
        <p>Maud schrijft de artikelen op BeterBody. Na jaren van streng diëten koos ze voor een aanpak die wel vol te houden is, en daar gaat het op dit blog over.</p>
        <a href="/over-de-schrijfster/">Meer over Maud</a>
      </div>
    </div>
  </div>
</section>"""
    h += footer()
    write(path, h)


# ----------------------------------------------------------------------------
# NIEUWS (index)
# ----------------------------------------------------------------------------
def nieuws_index():
    path = "/nieuws/"
    crumbs = [("Home","/"),("Nieuws",path)]
    cards = "".join(card_html(a) for a in ARTICLES)
    ld = [breadcrumb(crumbs), {
        "@context":"https://schema.org","@type":"Blog","@id":BASE+path,
        "name":"Nieuws van BeterBody","url":BASE+path,"inLanguage":"nl-NL",
        "publisher":{"@id":BASE+"/#organisatie"},
        "blogPost":[{"@type":"BlogPosting","headline":a["title"],"url":BASE+f"/nieuws/{a['slug']}/","datePublished":a["date"]} for a in ARTICLES]
    }]
    h = head("Nieuws | "+SITE, "Artikelen over een gezonde leefstijl, voeding en fitness. Praktisch en vol te houden.", path, ld)
    h += header("/nieuws/")
    h += crumbs_html(crumbs)
    h += f"""<section class="section">
  <div class="wrap">
    <div class="section-head">
      <span class="eyebrow">{LEAF}Het blog</span>
      <h1>Nieuws en artikelen</h1>
      <p>Stukken over voeding, beweging en een leefstijl die vol te houden is. Geschreven door Maud Brinkman.</p>
    </div>
    <div class="cards">{cards}</div>
  </div>
</section>"""
    h += footer()
    write(path, h)


# ----------------------------------------------------------------------------
# RECEPTEN
# ----------------------------------------------------------------------------
def recepten():
    path = "/recepten/"
    crumbs = [("Home","/"),("Recepten",path)]
    recipes = [
        ("Ontbijt", "Havermout met fruit en kwark", "Havermout met een schep magere kwark en vers fruit. Vezels en eiwit zorgen samen voor een langer verzadigd gevoel tot de ochtendsnack."),
        ("Lunch", "Volkoren wrap met kip en groente", "Een volkoren wrap met kipfilet, sla, tomaat en komkommer. Snel klaar en goed mee te nemen."),
        ("Avond", "Poké bowl met kip teriyaki", "Zilvervliesrijst met kip, edamame en frisse groente. Voedzaam en gevarieerd, met genoeg eiwit."),
        ("Avond", "Griekse salade met feta", "Tomaat, komkommer, rode ui, olijven en een blokje feta. Licht en vezelrijk als bijgerecht of lichte maaltijd."),
        ("Salade", "Orzo salade met sinaasappel", "Orzo met feta, frisse kruiden en partjes sinaasappel. Lekker als lunch of bijgerecht."),
        ("Toetje", "Magere yoghurt met noten", "Magere yoghurt met een kleine portie noten en kaneel. Een licht toetje met wat extra eiwit."),
    ]
    cards = "".join(
        f'<div class="recipe"><span class="kcal">{k}</span><h3>{esc(t)}</h3><p>{esc(d)}</p></div>'
        for k,t,d in recipes
    )
    ld = [breadcrumb(crumbs)]
    h = head("Recepten | "+SITE, "Gezonde recepten en inspiratie voor het hele gezin. Voedzaam, gevarieerd en makkelijk vol te houden.", path, ld)
    h += header("/recepten/")
    h += crumbs_html(crumbs)
    h += f"""<section class="section">
  <div class="wrap">
    <div class="section-head">
      <span class="eyebrow">{LEAF}Inspiratie</span>
      <h1>Gezonde recepten</h1>
      <p>Voedzame gerechten waar het hele gezin van mee kan eten. De gedachte erachter: gewoon en gevarieerd eten, met genoeg groente, eiwit en vezels.</p>
    </div>
    <div class="recipes">{cards}</div>
    <div class="callout" style="margin-top:36px">
      <p>Op zoek naar meer recepten die passen bij afvallen met gezond eten? Bekijk de gerechten bij {render_slinc('https://rachelhulshof.nl/recepten/','de recepten van Slinc')}.</p>
    </div>
  </div>
</section>"""
    h += footer()
    write(path, h)


# ----------------------------------------------------------------------------
# OVER
# ----------------------------------------------------------------------------
def over():
    path = "/over/"
    crumbs = [("Home","/"),("Over",path)]
    ld = [breadcrumb(crumbs), {
        "@context":"https://schema.org","@type":"AboutPage","@id":BASE+path,
        "url":BASE+path,"name":"Over BeterBody","inLanguage":"nl-NL","about":{"@id":BASE+"/#organisatie"}
    }]
    h = head("Over BeterBody | "+SITE, "BeterBody is een blog over een gezonde leefstijl en fitness, met een voorkeur voor een aanpak die vol te houden is.", path, ld)
    h += header("/over/")
    h += crumbs_html(crumbs)
    h += f"""<section class="article">
  <div class="wrap narrow prose">
    <span class="eyebrow">{LEAF}Over het blog</span>
    <h1>Over BeterBody</h1>
    <p class="lead">BeterBody is een blog over een gezonde leefstijl en fitness.</p>
    <p>Rond afvallen en gezond leven is veel ruis. Crashdiëten, wondermiddelen en steeds wisselende adviezen wisselen elkaar af. BeterBody kiest bewust voor het nuchtere deel van dat verhaal: gewoon eten, regelmaat, genoeg beweging en gewoontes die ook over een jaar nog overeind staan.</p>
    <h2>Waar dit blog voor staat</h2>
    <p>De artikelen op BeterBody gaan over voeding, beweging en leefstijl. Het uitgangspunt is steeds hetzelfde. Een aanpak werkt pas als die vol te houden is. Streng zijn voor een paar weken levert zelden blijvend resultaat op.</p>
    <h2>Wie schrijft de artikelen</h2>
    <p>De stukken op BeterBody zijn van de hand van Maud Brinkman. Meer over haar achtergrond en aanpak staat op de pagina <a href="/over-de-schrijfster/">over de schrijfster</a>.</p>
    <div class="callout"><p>Vragen of een idee voor samenwerking? Bekijk de <a href="/contact/">contactpagina</a> of de <a href="/partners/">partnerpagina</a>.</p></div>
  </div>
</section>"""
    h += footer()
    write(path, h)


# ----------------------------------------------------------------------------
# OVER DE SCHRIJFSTER
# ----------------------------------------------------------------------------
def schrijfster():
    path = "/over-de-schrijfster/"
    crumbs = [("Home","/"),("Over de schrijfster",path)]
    person = dict(PERSON_JSONLD); person["@context"]="https://schema.org"
    person["description"]="Leefstijl- en gezondheidsschrijver bij BeterBody. Schrijft over een vol te houden aanpak van gezond leven."
    ld = [person, breadcrumb(crumbs)]
    h = head("Over de schrijfster | "+SITE, "Maud Brinkman schrijft de artikelen op BeterBody over een gezonde leefstijl en fitness.", path, ld)
    h += header("/over/")
    h += crumbs_html(crumbs)
    h += f"""<section class="article">
  <div class="wrap narrow prose">
    <span class="eyebrow">{LEAF}De schrijfster</span>
    <div class="author-card" style="margin-bottom:36px">
      <img src="/assets/img/maud-avatar.svg" alt="Getekend portret van Maud Brinkman" width="160" height="160">
      <div>
        <div class="role">Leefstijl- en gezondheidsschrijver</div>
        <h1 style="margin:0">Maud Brinkman</h1>
      </div>
    </div>
    <p class="lead">Ik ben Maud, schrijver van de artikelen op BeterBody.</p>
    <p>Mijn hele tienertijd en de jaren daarna was ik bezig met afvallen. Ik kende elk dieet, elke shake en elke app, en toch bleef het gewicht heen en weer gaan. Pas toen ik stopte met streng zijn en koos voor een aanpak die vol te houden was, bleef het resultaat eindelijk hangen.</p>
    <p>Op BeterBody schrijf ik over wat me daarbij geholpen heeft. Genoeg en gevarieerd eten, regelmaat over de dag, en dagelijks wat bewegen zonder dat het een verplichting wordt. Geen wondermiddelen, geen overdreven beloftes.</p>
    <p>Ik ben geen diëtist en geef geen medisch advies. Ik deel wat ik lees, wat ik zelf merk en wat in de praktijk vol te houden blijkt. Wie met een gezondheidsklacht zit, raad ik altijd aan om een huisarts of diëtist te raadplegen.</p>
    <p>Voor wie graag met een uitgewerkt programma werkt, beveel ik {render_slinc('https://rachelhulshof.nl/afvallen-met-slinc/','Slinc')} aan. Het sluit goed aan bij de aanpak waar ik zelf baat bij had.</p>
    <p><a href="/nieuws/">Lees de artikelen van Maud</a></p>
  </div>
</section>"""
    h += footer()
    write(path, h)


# ----------------------------------------------------------------------------
# PARTNERS
# ----------------------------------------------------------------------------
def partners():
    path = "/partners/"
    crumbs = [("Home","/"),("Partners",path)]
    ld = [breadcrumb(crumbs)]
    h = head("Partners | "+SITE, "Betrouwbare Nederlandse bronnen over voeding en gezondheid die BeterBody aanraadt, plus ruimte voor toekomstige linkpartners.", path, ld)
    h += header("/partners/")
    h += crumbs_html(crumbs)
    h += f"""<section class="section">
  <div class="wrap">
    <div class="section-head">
      <span class="eyebrow">{LEAF}Aanbevolen bronnen</span>
      <h1>Partners en bronnen</h1>
      <p>BeterBody verwijst graag naar betrouwbare Nederlandse bronnen over voeding en gezondheid. Hieronder twee toonaangevende autoriteiten.</p>
    </div>
    <div class="grid-2">
      <div class="partner">
        <div class="mark">V</div>
        <div>
          <h3>Voedingscentrum</h3>
          <p>Het Voedingscentrum geeft onafhankelijke en wetenschappelijk onderbouwde informatie over gezonde en duurzame voeding in Nederland.</p>
          <a href="https://www.voedingscentrum.nl/" target="_blank" rel="noopener">Naar voedingscentrum.nl</a>
        </div>
      </div>
      <div class="partner">
        <div class="mark">T</div>
        <div>
          <h3>Thuisarts</h3>
          <p>Thuisarts.nl biedt betrouwbare medische informatie van Nederlandse huisartsen over gezondheid, leefstijl en veelvoorkomende klachten.</p>
          <a href="https://www.thuisarts.nl/" target="_blank" rel="noopener">Naar thuisarts.nl</a>
        </div>
      </div>
    </div>
    <div class="callout" style="margin-top:36px">
      <p><strong>Linkpartner worden?</strong> Voor een samenwerking is BeterBody bereikbaar via <a href="mailto:info@beterbody.nl">info@beterbody.nl</a>.</p>
    </div>
  </div>
</section>"""
    h += footer()
    write(path, h)


# ----------------------------------------------------------------------------
# CONTACT
# ----------------------------------------------------------------------------
def contact():
    path = "/contact/"
    crumbs = [("Home","/"),("Contact",path)]
    ld = [breadcrumb(crumbs), {
        "@context":"https://schema.org","@type":"ContactPage","@id":BASE+path,
        "url":BASE+path,"name":"Contact","inLanguage":"nl-NL"
    }]
    h = head("Contact | "+SITE, "Neem contact op met BeterBody via info@beterbody.nl.", path, ld)
    h += header("/contact/")
    h += crumbs_html(crumbs)
    h += f"""<section class="section">
  <div class="wrap">
    <div class="contact-card">
      <span class="eyebrow" style="justify-content:center">{LEAF}Contact</span>
      <h1>Even mailen</h1>
      <p>Een vraag, een tip of een idee voor samenwerking? Een bericht is welkom. BeterBody werkt zonder contactformulier en is bereikbaar per e-mail.</p>
      <a class="mail" href="mailto:info@beterbody.nl">info@beterbody.nl</a>
      <div><a class="btn btn-primary" href="mailto:info@beterbody.nl">Stuur een e-mail {ARROW}</a></div>
    </div>
  </div>
</section>"""
    h += footer()
    write(path, h)


# ----------------------------------------------------------------------------
# LEGAL
# ----------------------------------------------------------------------------
def privacy():
    path = "/privacybeleid/"
    crumbs = [("Home","/"),("Privacybeleid",path)]
    ld = [breadcrumb(crumbs)]
    h = head("Privacybeleid | "+SITE, "Hoe BeterBody omgaat met persoonsgegevens.", path, ld)
    h += header("/")
    h += crumbs_html(crumbs)
    h += f"""<section class="article">
  <div class="wrap narrow prose">
    <span class="eyebrow">{LEAF}Privacy</span>
    <h1>Privacybeleid</h1>
    <p class="updated">Laatst bijgewerkt: 1 juni 2026</p>
    <p>BeterBody hecht waarde aan de privacy van bezoekers. Dit beleid legt uit welke gegevens worden verwerkt en met welk doel. Het beleid sluit aan bij de Algemene verordening gegevensbescherming (AVG).</p>
    <h2>Welke gegevens</h2>
    <p>BeterBody verzamelt zelf geen persoonsgegevens via de website. Er staat geen contactformulier op de site. Wie per e-mail contact opneemt, deelt daarbij een e-mailadres en de inhoud van het bericht.</p>
    <h2>Doel van de verwerking</h2>
    <p>Een e-mailadres en bericht worden alleen gebruikt om de betreffende vraag te beantwoorden of op een verzoek te reageren. Deze gegevens worden niet voor andere doeleinden gebruikt en niet aan derden verkocht.</p>
    <h2>Bewaartermijn</h2>
    <p>E-mailcorrespondentie wordt niet langer bewaard dan nodig is voor de afhandeling van de vraag of zolang dat wettelijk verplicht is.</p>
    <h2>Externe links</h2>
    <p>BeterBody verwijst naar externe websites, waaronder Slinc en de genoemde bronnen op de partnerpagina. Op die websites geldt het privacybeleid van de betreffende partij. BeterBody is niet verantwoordelijk voor de gegevensverwerking op externe sites.</p>
    <h2>Rechten</h2>
    <p>Iedereen heeft het recht op inzage, correctie of verwijdering van eigen persoonsgegevens. Een verzoek daartoe kan per e-mail worden ingediend via <a href="mailto:info@beterbody.nl">info@beterbody.nl</a>.</p>
    <h2>Cookies</h2>
    <p>Informatie over het gebruik van cookies staat in het <a href="/cookiebeleid/">cookiebeleid</a>.</p>
    <h2>Contact</h2>
    <p>Vragen over dit privacybeleid kunnen per e-mail worden gesteld via <a href="mailto:info@beterbody.nl">info@beterbody.nl</a>.</p>
  </div>
</section>"""
    h += footer()
    write(path, h)


def cookies():
    path = "/cookiebeleid/"
    crumbs = [("Home","/"),("Cookiebeleid",path)]
    ld = [breadcrumb(crumbs)]
    h = head("Cookiebeleid | "+SITE, "Hoe BeterBody omgaat met cookies.", path, ld)
    h += header("/")
    h += crumbs_html(crumbs)
    h += f"""<section class="article">
  <div class="wrap narrow prose">
    <span class="eyebrow">{LEAF}Cookies</span>
    <h1>Cookiebeleid</h1>
    <p class="updated">Laatst bijgewerkt: 1 juni 2026</p>
    <p>Dit cookiebeleid legt uit hoe BeterBody omgaat met cookies en vergelijkbare technieken.</p>
    <h2>Wat zijn cookies</h2>
    <p>Cookies zijn kleine bestanden die een website op een apparaat kan plaatsen. Ze worden onder meer gebruikt om voorkeuren te onthouden of om bezoek te meten.</p>
    <h2>Welke cookies gebruikt BeterBody</h2>
    <p>BeterBody is opgezet als eenvoudige website zonder trackingcookies en zonder advertentienetwerken. Er worden geen cookies geplaatst die bezoekers volgen voor advertentiedoeleinden.</p>
    <p>Wel kan het hostingplatform technische gegevens verwerken die nodig zijn om de website veilig en betrouwbaar te tonen. Dit gebeurt op basis van een gerechtvaardigd belang en zonder het volgen van individuele bezoekers.</p>
    <h2>Externe content</h2>
    <p>Voor de weergave van lettertypen maakt de site gebruik van een externe bron. Daarbij kan een verzoek naar die dienst gaan om de lettertypen te laden. Bij het aanklikken van een link naar een externe website, zoals Slinc, gelden de cookieregels van die website.</p>
    <h2>Cookies beheren</h2>
    <p>Cookies kunnen via de browserinstellingen worden bekeken en verwijderd. In de meeste browsers is het mogelijk om cookies te blokkeren of een melding te krijgen voordat een cookie wordt geplaatst.</p>
    <h2>Vragen</h2>
    <p>Vragen over dit cookiebeleid kunnen per e-mail worden gesteld via <a href="mailto:info@beterbody.nl">info@beterbody.nl</a>.</p>
  </div>
</section>"""
    h += footer()
    write(path, h)


def not_found():
    h = head("Pagina niet gevonden | "+SITE, "Deze pagina bestaat niet of is verplaatst.", "/404", None)
    h += header("/")
    h += f"""<section class="section">
  <div class="wrap narrow" style="text-align:center;padding:40px 0">
    <span class="eyebrow" style="justify-content:center">{LEAF}404</span>
    <h1>Deze pagina is er niet</h1>
    <p>De opgevraagde pagina bestaat niet of is verplaatst. Een van onderstaande links helpt verder.</p>
    <p style="margin-top:24px"><a class="btn btn-primary" href="/">Naar de homepage</a> <a class="btn btn-ghost" href="/nieuws/">Naar het nieuws</a></p>
  </div>
</section>"""
    h += footer()
    full = os.path.join(OUT, "404.html")
    with open(full, "w", encoding="utf-8") as f:
        f.write(h)


# ----------------------------------------------------------------------------
# sitemap + robots + headers
# ----------------------------------------------------------------------------
def extras():
    urls = ["/","/nieuws/","/recepten/","/over/","/over-de-schrijfster/","/partners/","/contact/","/privacybeleid/","/cookiebeleid/"]
    urls += [f"/nieuws/{a['slug']}/" for a in ARTICLES]
    lastmod = "2026-06-01"
    body = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemap.org/schemas/sitemap/0.9">\n'
    body = body.replace("sitemap.org/schemas/sitemap/0.9","sitemaps.org/schemas/sitemap/0.9")
    for u in urls:
        pr = "1.0" if u == "/" else ("0.8" if u.startswith("/nieuws/") and u!="/nieuws/" else "0.7")
        body += f"  <url><loc>{BASE}{u}</loc><lastmod>{lastmod}</lastmod><priority>{pr}</priority></url>\n"
    body += "</urlset>\n"
    with open(os.path.join(OUT,"sitemap.xml"),"w",encoding="utf-8") as f:
        f.write(body)

    robots = f"""User-agent: *
Allow: /

Sitemap: {BASE}/sitemap.xml
"""
    with open(os.path.join(OUT,"robots.txt"),"w",encoding="utf-8") as f:
        f.write(robots)

    headers = """/*
  X-Content-Type-Options: nosniff
  Referrer-Policy: strict-origin-when-cross-origin
  X-Frame-Options: SAMEORIGIN
  Permissions-Policy: geolocation=(), microphone=(), camera=()

/assets/*
  Cache-Control: public, max-age=31536000, immutable
"""
    with open(os.path.join(OUT,"_headers"),"w",encoding="utf-8") as f:
        f.write(headers)

    redirects = "https://www.beterbody.nl/* https://beterbody.nl/:splat 301!\n"
    with open(os.path.join(OUT,"_redirects"),"w",encoding="utf-8") as f:
        f.write(redirects)


def copy_assets():
    src = os.path.join(SRC, "assets")
    dst = os.path.join(OUT, "assets")
    if os.path.exists(dst):
        shutil.rmtree(dst)
    shutil.copytree(src, dst)


def main():
    if os.path.exists(OUT):
        shutil.rmtree(OUT)
    os.makedirs(OUT, exist_ok=True)
    copy_assets()
    home()
    nieuws_index()
    for a in ARTICLES:
        article_page(a)
    recepten()
    over()
    schrijfster()
    partners()
    contact()
    privacy()
    cookies()
    not_found()
    extras()
    print("Build klaar in", OUT)


if __name__ == "__main__":
    main()
