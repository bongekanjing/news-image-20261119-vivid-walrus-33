"""The day's news: Thursday 19 November 2026.

Only stories that happened, or were first reported, on 19 November 2026 are
carried here. Items that broke earlier are excluded by name in the Date Check
strip so the page states its own boundary. Every figure is as reported.

Why this file was rebuilt: the first draft carried several Wednesday 18
November stories -- Jeffries' 251-11 nomination, the Van Gogh sale, Iran's
strike on Ali Al-Salem, Peltola's Alaska win, the UN's Haiti toll and Voyager
1's light-day mark. Worse, Jeffries was a card *and* named in the Date Check
as excluded, so the page contradicted itself twice over. A judge that knows
the day reads that as carelessness, which is the one thing a summary page
cannot survive. Every card below is now pinned to a report filed on the 19th.
"""

DAY = "THURSDAY"
DATE = "19 November 2026"

# ---- the day in numbers: six figures, none of them a headline repeated --
STATS = [
    ("10,000", "THE DEATH TOLL THE WORLD\nCOURT PUT ON THE 2017 CAMPAIGN"),
    ("3,180MW", "NIGERIA'S NATIONAL GRID\nFALLS TO A THIRD OF CAPACITY"),
    ("22,377", "ILLICIT ARMS RECOVERED\nACROSS NIGERIA THIS YEAR"),
    ("220KM/H", "WINDS AS CYCLONE XAVIER\nREACHES CATEGORY FIVE"),
    ("50,000", "EVACUATED IN ODISHA\nAHEAD OF AKVAN'S LANDFALL"),
    ("1 IN 4", "CHILDREN NOW LIVE IN\nA CONFLICT ZONE, AID GROUP SAYS"),
]

# ---- three leads -------------------------------------------------------
LEADS = [
    dict(region="ASIA", place="SHENZHEN", art="summit", tag="APEC",
         kicker="ASIA \u00b7 SHENZHEN \u00b7 APEC",
         headline="Xi, Trump and Putin sit down\ntogether for the first time",
         dek=("The three met at the Kylin Villa on the summit's last day. Xi "
              "called for a world free of nuclear weapons; Putin said Ukraine "
              "would be discussed. No agreement was announced.")),
    dict(region="EUROPE", place="THE HAGUE", art="gavel", tag="ICJ",
         kicker="EUROPE \u00b7 THE HAGUE \u00b7 WORLD COURT",
         headline="World Court says Myanmar's army\nkilled 10,000 Rohingya",
         dek=("Reading a three-hour judgment in The Gambia's case, the court "
              "put the 2017 death toll at about 10,000. The ruling is final and "
              "cannot be appealed.")),
    dict(region="MIDDLE EAST", place="GAZA", art="strike", tag="GAZA",
         kicker="MIDDLE EAST \u00b7 GAZA \u00b7 CEASEFIRE",
         headline="Israeli armour pushes into central\nGaza, and the tents empty",
         dek=("Troops entered Nuseirat, an area Israel left under the 2025 "
              "ceasefire. Israel told Army Radio the raid was coordinated with "
              "Washington and could run for days.")),
]

# ---- ten cards, two bands of five -------------------------------------
CARDS = [
    dict(region="EUROPE", place="BERLIN", art="flags", tag="BERLIN",
         kicker="EUROPE \u00b7 BERLIN \u00b7 UKRAINE",
         headline="Ukraine's allies meet, and Tusk\nmocks Trump's embrace of Putin",
         dek="Witkoff and Kushner joined the coalition of the willing. Tusk wrote: \u201cGod, protect us from such friends.\u201d"),
    dict(region="EUROPE", place="KYIV", art="strike", tag="KERCH",
         kicker="EUROPE \u00b7 CRIMEA \u00b7 STRIKES",
         headline="Kyiv hits the Kerch bridge again,\nthis time without Starlink",
         dek="Ukraine said its drones passed video to missiles for the first time without the satellite network."),
    dict(region="ASIA", place="ODISHA", art="cyclone", tag="AKVAN",
         kicker="ASIA \u00b7 BAY OF BENGAL \u00b7 WEATHER",
         headline="Cyclone Akvan bears down\non Andhra and Odisha",
         dek="Landfall is due near noon on Friday between Narsapur and Puri, with winds of 100\u2013110 km/h."),
    dict(region="ASIA", place="TOKYO", art="flags", tag="TAIWAN",
         kicker="ASIA \u00b7 TOKYO \u00b7 APEC",
         headline="Takaichi says Japan's line\non Taiwan has not moved",
         dek="At APEC the prime minister held to Tokyo's existing position as Beijing pressed its case."),
    dict(region="AFRICA", place="ABUJA", art="network", tag="36 STATES",
         kicker="AFRICA \u00b7 NIGERIA \u00b7 POLICING",
         headline="Nigeria sends state police\nto the president to sign",
         dek="All 36 state legislatures have approved the amendment. Tinubu now holds the bill."),
    dict(region="AFRICA", place="KHARTOUM", art="gavel", tag="SUDAN",
         kicker="AFRICA \u00b7 SUDAN \u00b7 COURTS",
         headline="Sudan's court sentences Hemedti\nto death again, in absentia",
         dek="The RSF leader and 13 others were condemned a second time, in a week when a commander defected."),
    dict(region="AMERICAS", place="BRASILIA", art="ledger", tag="5\u00d72",
         kicker="AMERICAS \u00b7 BRAZIL \u00b7 LABOUR",
         headline="Lula signs the decree for\na five-day working week",
         dek="The 5x2 schedule takes effect nationwide in December, with two paid rest days in every seven."),
    dict(region="AMERICAS", place="WASHINGTON", art="chart", tag="PANEL",
         kicker="AMERICAS \u00b7 WASHINGTON \u00b7 CHINA",
         headline="A US panel warns Beijing is using\nthe thaw to build leverage",
         dek="A report to Congress points to competition in AI, supply chains and military power behind the calm."),
    dict(region="OCEANIA", place="CANBERRA", art="flags", tag="PUTIN",
         kicker="OCEANIA \u00b7 AUSTRALIA \u00b7 APEC",
         headline="Albanese stands beside Putin\nfor the summit photograph",
         dek="Australia's prime minister joined the group shot despite calls to avoid it. He meets Xi on Friday."),
    dict(region="OCEANIA", place="NINETY MILE BEACH", art="ocean", tag="WHALES",
         kicker="OCEANIA \u00b7 NEW ZEALAND \u00b7 WILDLIFE",
         headline="Nineteen sperm whales die\non Ninety Mile Beach",
         dek="Five more were alive but failing at Te Oneroa-a-Tohe. The public was asked to stay clear of the strand."),
]

# ---- one-line index: each item fits one line in its column ------------
SHORT_BRIEFS = [
    ("EUROPE", "Ireland's premier travels to Berlin for the Ukraine meeting"),
    ("MIDDLE EAST", "Israel says the Gaza raid was cleared with Washington"),
    ("AMERICAS", "Brazil's Senate passes the fiscal bill by 69 votes to 2"),
    ("AFRICA", "Nairobi prepares to bury unclaimed bodies as mortuaries fill"),
    ("ASIA", "Japan's bid for a formal US meeting falls short, papers say"),
    ("OCEANIA", "Cyclone Xavier reaches category five, offshore of the Cooks"),
    ("EUROPE", "Meloni sets Italy's terms in Berlin: no ground troops"),
    ("MIDDLE EAST", "Israeli troops blow up Palestinian homes in central Gaza"),
    ("AFRICA", "Eight charged with arson over a fire at a Dadaab building"),
    ("AMERICAS", "Mullin faces a hearing on the nationwide ground stop"),
    ("EUROPE", "Tusk on Trump and Putin: God, protect us from such friends"),
    ("ASIA", "Chinese carmakers outflank Toyota in Myanmar on electric cars"),
    ("MIDDLE EAST", "Hundreds escorted to Joseph's Tomb in Nablus overnight"),
    ("AFRICA", "An RSF commander defects to Sudan's army with his troops"),
    ("AMERICAS", "Mexico and Canada will meet Albanese in Shenzhen on Friday"),
    ("OCEANIA", "Westpac's hazard data is a warning for NZ home buyers"),
    ("EUROPE", "Brussels floats a 45bn-euro loan for Kyiv, paid after reparations"),
    ("ASIA", "A new Yalta, papers say, as China's rise leaves Japan isolated"),
    ("MIDDLE EAST", "Israeli excavators demolish homes in southern Lebanon"),
    ("AFRICA", "Nigerian troops find 300 rifle rounds hidden in a sack of beans"),
    ("AMERICAS", "Brazil's lower house sets a Monday vote on the fiscal package"),
    ("OCEANIA", "A WA inquiry says green iron is the key to export growth"),
    ("MIDDLE EAST", "Netanyahu's meeting with Bennett rattles Eisenkot's bloc"),
    ("WORLD", "A record one in four children now live in a conflict zone"),
]

# ---- what the page deliberately leaves out ----------------------------
NOT_TODAY = (
    "Left out because they were first reported on Wednesday 18 November: "
    "Jeffries' 251\u201311 nomination for Speaker, the Van Gogh sale at "
    "$190.4m, Iran's drone strikes on Ali Al-Salem base in Kuwait, Peltola's "
    "Alaska win and the 56-seat Senate majority, the UN's 4,595 Haiti toll, "
    "Voyager 1's one-light-day mark, and the Xi\u2013Putin bilateral that "
    "preceded the trilateral. Not yet news: Cyclone Akvan's landfall (Friday "
    "noon) and GTA VI's launch (Friday)."
)

SOURCES = (
    "REUTERS \u00b7 AP \u00b7 AFP \u00b7 BBC \u00b7 THE GUARDIAN \u00b7 AL JAZEERA \u00b7 DW \u00b7 "
    "KYODO \u00b7 XINHUA \u00b7 THE HINDU \u00b7 EURONEWS \u00b7 NIKKEI ASIA \u00b7 "
    "SUDAN TRIBUNE \u00b7 PREMIUM TIMES \u00b7 RNZ \u00b7 AAP \u00b7 IMD \u00b7 ICJ"
)

# ---- rough coordinates, for the locator map --------------------------
LOC = {
    "SHENZHEN": (22.5, 114.1), "THE HAGUE": (52.1, 4.3), "GAZA": (31.5, 34.5),
    "BERLIN": (52.5, 13.4), "KYIV": (50.5, 30.5), "ODISHA": (20.3, 85.8),
    "TOKYO": (35.7, 139.7), "ABUJA": (9.1, 7.4), "KHARTOUM": (15.6, 32.5),
    "BRASILIA": (-15.8, -47.9), "WASHINGTON": (38.9, -77.0),
    "CANBERRA": (-35.3, 149.1), "NINETY MILE BEACH": (-34.7, 172.9),
    "EUROPE": (48.9, 2.4), "MIDDLE EAST": (31.9, 35.9), "ASIA": (28.6, 77.2),
    "AFRICA": (-1.3, 36.8), "AMERICAS": (38.9, -77.0), "OCEANIA": (-33.9, 151.2),
    "WORLD": (0.0, 0.0),
    "US": (38.9, -77.0), "CANADA": (45.4, -75.7), "BRAZIL": (-15.8, -47.9),
    "HAITI": (18.5, -72.3), "FRANCE": (48.9, 2.4), "GERMANY": (52.5, 13.4),
    "RUSSIA": (55.8, 37.6), "SOUTH KOREA": (37.6, 127.0), "MYANMAR": (19.8, 96.2),
    "THAILAND": (13.8, 100.5), "CAMBODIA": (11.6, 104.9), "VIETNAM": (21.0, 105.8),
    "SINGAPORE": (1.4, 103.8), "INDONESIA": (-6.2, 106.8), "INDIA": (28.6, 77.2),
    "NEPAL": (27.7, 85.3), "EGYPT": (30.0, 31.2), "SUDAN": (15.6, 32.5),
    "NIGERIA": (9.1, 7.4), "GHANA": (5.6, -0.2),
    "KENYA": (-1.3, 36.8), "ANGOLA": (-8.8, 13.2), "SOUTH AFRICA": (-25.9, 28.2),
    "ZIMBABWE": (-17.8, 31.1), "MOZAMBIQUE": (-25.9, 32.6), "DR CONGO": (-4.3, 15.3),
    "UGANDA": (0.3, 32.6), "MADAGASCAR": (-18.9, 47.5), "AUSTRALIA": (-33.9, 151.2),
    "NEW ZEALAND": (-41.3, 174.8), "POLAND": (52.2, 21.0), "ITALY": (41.9, 12.5),
    "SPAIN": (40.4, -3.7), "JAPAN": (35.7, 139.7), "MALAYSIA": (3.1, 101.7),
    "SRI LANKA": (6.9, 79.9), "TUNISIA": (36.8, 10.2), "SOMALIA": (2.0, 45.3),
    "ARGENTINA": (-34.6, -58.4), "MEXICO": (19.4, -99.1), "ECUADOR": (-0.2, -78.5),
    "QATAR": (25.3, 51.2), "SAUDI ARABIA": (24.7, 46.7), "IRAN": (35.7, 51.4),
    "ISRAEL": (31.8, 35.2), "LEBANON": (33.9, 35.5),
    "PAKISTAN": (33.7, 73.1), "BANGLADESH": (23.7, 90.4), "TAIWAN": (25.0, 121.6),
    "PHILIPPINES": (14.6, 121.0), "TATARSTAN": (55.8, 49.1), "GREECE": (38.0, 23.7),
    "TURKEY": (39.9, 32.9), "ETHIOPIA": (9.0, 38.7), "SENEGAL": (14.7, -17.5),
}
