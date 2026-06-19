# BeterBody.nl

Statische website over een gezonde leefstijl en fitness. Onafhankelijk platform dat Slinc aanbeveelt. Geen framework, geen buildstap nodig op de server: alles in de map `site/` is kant en klaar voor Cloudflare Pages.

## Wat zit erin

- Homepage in dienst van Slinc, met branded en beschrijvende ankerteksten naar rachelhulshof.nl (geen kale keyword-ankers).
- Nieuws met vijf artikelen, geschreven door de persona Maud Brinkman, inclusief FAQ-secties en interne links.
- Recepten, Over BeterBody, Over de schrijfster, Partners, Contact.
- Privacybeleid en cookiebeleid, in de footer gelinkt.
- 404-pagina, sitemap.xml, robots.txt, beveiligingsheaders en een www-naar-apex redirect.
- JSON-LD schema op elke pagina (Organization, WebSite, BlogPosting, Person, BreadcrumbList, FAQPage, AboutPage, ContactPage).
- Eigen visuele identiteit: warm papier, diep sage-groen, blush en mint als knipoog naar het palet van Slinc. Getekende avatar voor de schrijfster.

## Mapstructuur

```
site/                      <- dit is de map die naar Cloudflare Pages gaat
  index.html
  nieuws/                  (overzicht + 5 artikelmappen)
  recepten/  over/  over-de-schrijfster/  partners/  contact/
  privacybeleid/  cookiebeleid/
  404.html
  sitemap.xml  robots.txt  _headers  _redirects
  assets/css  assets/img  assets/icons
build.py                   <- generator, alleen nodig om de site opnieuw te bouwen
```

Schone URL's komen uit de mapstructuur: `over/index.html` wordt `/over/`. Canonical-basis is `https://beterbody.nl` (apex, zonder www).

## Deployen op Cloudflare Pages

Twee manieren.

**1. Direct uploaden (snelst)**
1. Log in op Cloudflare en ga naar Workers and Pages, Create, Pages, Upload assets.
2. Sleep de inhoud van de map `site/` in het venster (niet de map zelf, maar wat erin zit).
3. Geef het project een naam en publiceer.
4. Koppel het domein onder Custom domains: voeg `beterbody.nl` toe en laat Cloudflare de DNS instellen.

**2. Via Git**
1. Zet de inhoud van `site/` in een repository.
2. Maak in Cloudflare Pages een project gekoppeld aan die repository.
3. Build command leeg laten, output directory op `/` (of op de submap waarin `index.html` staat).

Een buildstap is niet nodig. De HTML is al gegenereerd.

## Domein: apex of www

De site gaat uit van `beterbody.nl` zonder www. Het bestand `_redirects` stuurt `www.beterbody.nl` met een 301 door naar de apex. Wie liever www als hoofdvorm gebruikt, draait dit om in `_redirects` en past de `BASE` in `build.py` aan naar `https://www.beterbody.nl`, en bouwt opnieuw.

## Links naar Slinc: rel="sponsored"

Alle links naar rachelhulshof.nl staan nu op `rel="noopener sponsored"`. Dat is de variant die past bij de richtlijnen van Google voor promotionele of commerciele links. Het gevolg is dat deze links standaard geen linkwaarde doorgeven.

Wie bewust wel linkwaarde wil laten doorstromen naar Slinc, haalt `sponsored` weg. Dat staat op twee plekken in `build.py`:
- de functie `render_slinc()` (gebruikt in artikelen, recepten, over en schrijfster);
- de homepage-links in `home()` en in `header()` en `footer()`.

Dit is een afweging tussen richtlijnconform en linkwaarde. De keuze ligt bij de beheerder.

## Nog invullen voor livegang

- In `privacybeleid/` en `cookiebeleid/` staat een blok met "Let op voor de beheerder". Vul daar de juiste bedrijfs- of eigenaargegevens in, zoals naam, adres en KvK-nummer.
- Controleer of `info@beterbody.nl` actief is. Dit adres staat op de contactpagina en in beide beleidsteksten.

## Een artikel toevoegen

1. Open `build.py` en zoek de lijst `ARTICLES`.
2. Voeg een blok toe met `slug`, `tag`, `title`, `desc`, `date`, `intro`, `body`, `faq` en `related`.
3. In `body` kan elk blok zijn: `("h2", "Kop")`, `("p", "Tekst")`, `("ul", ["punt", "punt"])`, `("callout", "Tekst")` of `("figure", "/assets/img/bestand.webp", "alt", "onderschrift")`.
4. Een link naar Slinc in de tekst: `<slinc href='https://rachelhulshof.nl/...' anchor='ankertekst'></slinc>`.
5. Een interne link: `<link href='/nieuws/andere-slug/' anchor='ankertekst'></link>`. Gebruik korte ankers van twee of drie woorden.
6. Draai `python3 build.py`. De map `site/` wordt opnieuw opgebouwd, inclusief sitemap.

## Stijlregels in de teksten

De teksten houden zich aan vaste regels: geen liggende streepjes, geen emoji, geen tweede persoon (geen je, jij, jullie of uw), korte en duidelijke taal. Interne ankers zijn korte bestaande woordgroepen. De persona is geen dietist en geeft geen medisch advies.

## Lettertypen

Fraunces en Mulish worden geladen via Google Fonts. Wie liever geen externe verzoeken wil, kan de lettertypen zelf hosten en de `<link>` in `build.py` vervangen door een lokale `@font-face`. Dit staat ook benoemd in het cookiebeleid.
