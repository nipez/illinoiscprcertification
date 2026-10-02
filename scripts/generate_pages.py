#!/usr/bin/env python3
"""Generate static multi-page HTML for Illinois CPR Certification."""
from pathlib import Path

ROOT = Path("/workspace/public")
TODAY = "2026-10-02"
SITE = "https://illinoiscprcertification.com"
OG = f"{SITE}/images/og-default.jpg"
AHA_DISCLAIMER = (
    "The American Heart Association strongly promotes knowledge and proficiency in all AHA courses "
    "and has developed instructional materials for this purpose. Use of these materials in an educational "
    "course does not represent course sponsorship by the AHA. Any fees charged for such a course, except "
    "for a portion of fees needed for AHA course materials, do not represent income to the AHA."
)
TRADEMARK = (
    "American Heart Association® and AHA® are registered trademarks of the American Heart Association. "
    "Illinois CPR Certification is an independent training provider and is not owned, operated, or "
    "sponsored by the American Heart Association."
)

ORG_JSONLD = """{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": ["Organization", "LocalBusiness", "ProfessionalService"],
      "@id": "https://illinoiscprcertification.com/#business",
      "name": "Illinois CPR Certification",
      "legalName": "Illinois CPR Certification LLC",
      "url": "https://illinoiscprcertification.com/",
      "telephone": "+1-847-321-7610",
      "email": "contact@illinoiscprcertification.com",
      "logo": "https://illinoiscprcertification.com/images/logo.png",
      "image": "https://illinoiscprcertification.com/images/og-default.jpg",
      "address": {
        "@type": "PostalAddress",
        "streetAddress": "605 N Michigan Ave, Suite 454",
        "addressLocality": "Chicago",
        "addressRegion": "IL",
        "postalCode": "60611",
        "addressCountry": "US"
      },
      "founder": {
        "@type": "Person",
        "name": "Jason Pierce"
      },
      "areaServed": [
        {"@type": "City", "name": "Chicago"},
        {"@type": "AdministrativeArea", "name": "Chicagoland"},
        {"@type": "State", "name": "Illinois"}
      ]
    },
    {
      "@type": "WebSite",
      "@id": "https://illinoiscprcertification.com/#website",
      "url": "https://illinoiscprcertification.com/",
      "name": "Illinois CPR Certification",
      "publisher": {"@id": "https://illinoiscprcertification.com/#business"}
    }
  ]
}"""
# TODO comments for geo/openingHours/priceRange/sameAs left in HTML comments near JSON-LD


def nav(current: str) -> str:
    items = [
        ("/", "Home", "home"),
        ("/bls-certification/", "BLS Course", "bls"),
        ("/onsite-group-training/", "Onsite Training", "onsite"),
        ("/service-areas/", "Service Areas", "areas"),
        ("/about/", "About", "about"),
        ("/faq/", "FAQ", "faq"),
        ("/contact/", "Contact", "contact"),
    ]
    links = []
    for href, label, key in items:
        cur = ' aria-current="page"' if key == current else ""
        links.append(f'        <a href="{href}"{cur}>{label}</a>')
    cta_cur = ' aria-current="page"' if current == "contact" else ""
    links.append(f'        <a class="nav-cta" href="/contact/#quote"{cta_cur}>Request a quote</a>')
    return "\n".join(links)


def header(current: str) -> str:
    return f"""    <a class="skip-link" href="#main">Skip to content</a>
    <header class="site-header">
      <div class="site-header-inner">
        <a href="/" aria-label="Illinois CPR Certification home">
          <img
            class="site-logo"
            src="/images/logo.png"
            width="860"
            height="282"
            alt="Illinois CPR Certification"
          />
        </a>
        <button class="nav-toggle" type="button" aria-expanded="false" aria-controls="site-nav">
          Menu
        </button>
        <nav class="site-nav" id="site-nav" aria-label="Primary">
{nav(current)}
        </nav>
      </div>
    </header>"""


def footer() -> str:
    return f"""    <footer class="site-footer">
      <div class="container">
        <div class="footer-grid">
          <div class="footer-brand">
            <img
              class="footer-seal"
              src="/images/logo-seal.png"
              width="400"
              height="218"
              alt="Illinois CPR Certification seal"
              loading="lazy"
            />
            <div class="footer-logo-text">Illinois CPR Certification</div>
            <div class="footer-nap">
              <p>605 N Michigan Ave, Suite 454<br />Chicago, IL 60611</p>
              <p><a href="tel:+18473217610">(847) 321-7610</a></p>
              <p><a href="mailto:contact@illinoiscprcertification.com">contact@illinoiscprcertification.com</a></p>
              <p>Mobile AHA BLS training across Chicagoland &amp; Illinois</p>
              <p>Owned and taught by Jason Pierce</p>
            </div>
          </div>
          <div class="footer-nav" aria-label="Footer courses">
            <strong>Training</strong>
            <a href="/bls-certification/">AHA BLS Provider course</a>
            <a href="/onsite-group-training/">Onsite group training</a>
            <a href="/service-areas/">Chicagoland &amp; Illinois</a>
            <a href="/faq/">FAQ</a>
            <a href="/about/">About Jason Pierce</a>
            <a href="/contact/">Request a quote</a>
          </div>
          <div class="footer-nav" aria-label="Footer legal">
            <strong>Policies</strong>
            <a href="/privacy-policy/">Privacy Policy</a>
            <a href="/terms/">Terms of Service</a>
            <a href="/cancellation-refund-policy/">Cancellation &amp; Refund</a>
            <a href="/accessibility/">Accessibility</a>
            <a href="/aha-disclaimer/">AHA Disclaimer</a>
          </div>
        </div>
        <div class="aha-box">
          <p>{AHA_DISCLAIMER}</p>
          <p>{TRADEMARK}</p>
        </div>
        <div class="legal-row">
          <a href="/privacy-policy/">Privacy</a>
          <a href="/terms/">Terms</a>
          <a href="/cancellation-refund-policy/">Cancellation</a>
          <a href="/accessibility/">Accessibility</a>
          <a href="/aha-disclaimer/">AHA Disclaimer</a>
          <a href="/contact/">Contact</a>
        </div>
        <p class="copyright">© 2026 Illinois CPR Certification LLC. All rights reserved.</p>
      </div>
    </footer>
    <script src="/contact.js" defer></script>"""


def head(
    title: str,
    description: str,
    canonical: str,
    *,
    extra: str = "",
    noindex: bool = False,
    jsonld: str | None = None,
) -> str:
    robots = '    <meta name="robots" content="noindex" />\n' if noindex else ""
    ld = jsonld if jsonld is not None else ORG_JSONLD
    return f"""<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>{title}</title>
    <meta name="description" content="{description}" />
{robots}    <link rel="canonical" href="{canonical}" />
    <meta property="og:type" content="website" />
    <meta property="og:title" content="{title}" />
    <meta property="og:description" content="{description}" />
    <meta property="og:url" content="{canonical}" />
    <meta property="og:image" content="{OG}" />
    <meta property="og:site_name" content="Illinois CPR Certification" />
    <meta name="twitter:card" content="summary_large_image" />
    <meta name="twitter:title" content="{title}" />
    <meta name="twitter:description" content="{description}" />
    <meta name="twitter:image" content="{OG}" />
    <link rel="icon" href="/favicon.png" type="image/png" />
    <link rel="icon" href="/favicon.svg" type="image/svg+xml" />
    <link rel="preconnect" href="https://fonts.googleapis.com" />
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
    <link
      href="https://fonts.googleapis.com/css2?family=Figtree:wght@400;600&family=Instrument+Serif&display=swap"
      rel="stylesheet"
    />
    <link rel="stylesheet" href="/styles.css" />
    <!-- TODO-JASON: add geo, openingHours, priceRange, and sameAs (social profiles) to LocalBusiness JSON-LD when confirmed -->
    <script type="application/ld+json">
{ld}
    </script>
{extra}  </head>"""


QUOTE_FORM = """          <form id="quote" class="quote">
            <h2>Request a class quote</h2>
            <p class="form-intro">
              Tell us about your team and we will follow up with a class quote for onsite
              AHA BLS training.
            </p>
            <fieldset>
              <legend>Contact</legend>
              <label>
                Full name
                <input name="name" type="text" autocomplete="name" required />
              </label>
              <label>
                Email address
                <input name="email" type="email" autocomplete="email" required />
              </label>
              <label>
                Direct phone
                <input name="phone" type="tel" autocomplete="tel" />
              </label>
            </fieldset>
            <fieldset>
              <legend>Practice</legend>
              <label>
                Practice / company name
                <input name="practice" type="text" />
              </label>
              <label>
                Practice type
                <select name="practice_type">
                  <option value="">Select one</option>
                  <option>Dental Office</option>
                  <option>Medical Clinic</option>
                  <option>Physical Therapy</option>
                  <option>Urgent Care</option>
                  <option>Hospital or Network</option>
                  <option>Other Corporate Office</option>
                </select>
              </label>
              <div class="split">
                <label>
                  Estimated students
                  <input name="students" type="number" min="1" />
                </label>
                <label>
                  Zip code
                  <input name="zip" type="text" inputmode="numeric" autocomplete="postal-code" />
                </label>
              </div>
              <label>
                Ideal timeframe
                <select name="timeframe">
                  <option value="">Select one</option>
                  <option>ASAP (Within 30 days)</option>
                  <option>Next Month</option>
                  <option>2–3 Months Out</option>
                  <option>Just looking for information</option>
                </select>
              </label>
            </fieldset>
            <label>
              Notes
              <textarea name="notes" rows="3" placeholder="Split shifts, schedule notes, or accessibility needs"></textarea>
            </label>
            <button type="submit">Send quote request</button>
            <p id="quote-status" class="form-status" hidden></p>
          </form>"""


def crumbs(items: list[tuple[str, str]]) -> str:
    parts = ['      <nav class="breadcrumbs" aria-label="Breadcrumb">']
    for i, (href, label) in enumerate(items):
        if i == len(items) - 1:
            parts.append(f"        <span>{label}</span>")
        else:
            parts.append(f'        <a href="{href}">{label}</a> /')
    parts.append("      </nav>")
    # BreadcrumbList JSON-LD
    elements = []
    for i, (href, label) in enumerate(items, start=1):
        url = SITE + (href if href != "/" else "/")
        if not url.endswith("/") and href != "/":
            url += "/"
        if href == "/":
            url = SITE + "/"
        else:
            url = SITE + href
        elements.append(
            f'{{"@type":"ListItem","position":{i},"name":"{label}","item":"{url}"}}'
        )
    return "\n".join(parts), (
        '{\n  "@context": "https://schema.org",\n  "@type": "BreadcrumbList",\n  "itemListElement": ['
        + ",".join(elements)
        + "]\n}"
    )


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    print("wrote", path.relative_to(ROOT))


# ========== HOME ==========
home = f"""{head(
    "Illinois CPR Certification | Mobile AHA BLS",
    "Mobile AHA BLS training for busy healthcare teams across Chicagoland and Illinois. Taught by AHA Instructors at your office or clinic.",
    f"{SITE}/",
)}
  <body>
{header("home")}
    <main id="main" class="site-main">
      <section class="home-hero" aria-label="Illinois CPR Certification">
        <div class="home-hero-copy">
          <div class="brand-mark">
            <img
              src="/images/logo.png"
              width="860"
              height="282"
              alt="Illinois CPR Certification"
            />
          </div>
          <h1>Mobile AHA BLS Training Built for Busy Healthcare Teams</h1>
          <div class="highlights">
            <ul class="promises">
              <li>No lost production.</li>
              <li>No weekend travel.</li>
              <li>
                Just American Heart Association BLS Provider training delivered
                right to your office or clinic.
              </li>
            </ul>
            <ul class="features">
              <li>Follows current AHA guidelines</li>
              <li>Flexible Hours</li>
              <li>Taught by AHA Instructors</li>
            </ul>
          </div>
          <h2>Keep Your Practice Ready with Instructor-Led AHA BLS</h2>
          <p>
            State dental boards and medical networks look for the gold standard.
            Illinois CPR Certification brings
            <strong>instructor-led American Heart Association BLS Provider courses</strong>
            to your team—using mandatory real-time feedback manikins—so your staff
            can renew CPR certification without leaving the clinic.
          </p>
          <p>
            Don’t risk licensing requirements on unapproved “online-only” courses.
            Our AHA Instructors bring the classroom to you, so your team can meet
            employer and board expectations with less scheduling hassle.
          </p>
          <div class="btn-row">
            <a class="btn" href="#quote">Get your quote today</a>
            <a class="btn btn-secondary" href="/bls-certification/">AHA BLS course details</a>
          </div>
          <p class="call-line">
            Call us today <a href="tel:+18473217610">(847) 321-7610</a>
          </p>
          <p class="call-line">
            Email
            <a href="mailto:contact@illinoiscprcertification.com">contact@illinoiscprcertification.com</a>
          </p>
        </div>
        <figure class="home-hero-visual">
          <img
            src="/images/hero.jpg"
            width="1600"
            height="900"
            alt="Instructor performing chest compressions on a CPR training manikin"
          />
        </figure>
      </section>

      <section class="section">
        <div class="container">
          <div class="section-head">
            <h2>CPR certification services for Chicagoland teams</h2>
            <p class="lede">
              Mobile CPR training and onsite BLS certification designed around
              healthcare schedules—not the other way around.
            </p>
          </div>
          <div class="service-grid">
            <a class="service-link" href="/bls-certification/">
              <h3>AHA BLS Provider course</h3>
              <p>
                Hands-on Basic Life Support for healthcare providers, with an AHA
                BLS Provider course completion eCard after successful completion.
              </p>
              <span class="more">Course details →</span>
            </a>
            <a class="service-link" href="/onsite-group-training/">
              <h3>Onsite group training</h3>
              <p>
                We come to your dental office, clinic, or hospital network with
                manikins, AED trainers, and materials.
              </p>
              <span class="more">How onsite works →</span>
            </a>
            <a class="service-link" href="/service-areas/">
              <h3>Chicagoland &amp; Illinois</h3>
              <p>
                Mobile AHA BLS training across Chicagoland and Illinois—scheduled
                around your shifts.
              </p>
              <span class="more">Service areas →</span>
            </a>
          </div>
        </div>
      </section>

      <section class="section section-muted">
        <div class="container">
          <div class="section-head">
            <h2>Why healthcare teams choose mobile BLS</h2>
          </div>
          <ul class="why-list">
            <li><strong>We come to you.</strong> No weekend travel to a classroom across town.</li>
            <li><strong>Flexible hours.</strong> Before clinic, after hours, or split groups—work around production.</li>
            <li><strong>Real skills practice.</strong> Adult, child, and infant CPR with feedback manikins—not online-only shortcuts.</li>
            <li><strong>eCards you can verify.</strong> AHA BLS Provider course completion eCards, checkable at heart.org.</li>
          </ul>
          <p style="margin-top:1.25rem">
            Learn more about <a href="/about/">Illinois CPR Certification &amp; Jason Pierce</a>,
            or browse the <a href="/faq/">CPR certification FAQ</a>.
          </p>
        </div>
      </section>

      <section class="section">
        <div class="container">
          <div class="section-head">
            <h2>Quick answers</h2>
            <p class="lede">Common questions about AHA BLS and onsite training.</p>
          </div>
          <div class="faq-list">
            <details>
              <summary>Is an online-only BLS course enough?</summary>
              <p>
                No. AHA courses that teach CPR skills require a hands-on skills session.
                Online-only BLS does not produce an AHA BLS Provider course completion card.
              </p>
            </details>
            <details>
              <summary>How long is BLS certification valid?</summary>
              <p>
                An AHA BLS Provider eCard is valid for two years, through the end of the
                month it was issued.
              </p>
            </details>
            <details>
              <summary>Do you train at our office?</summary>
              <p>
                Yes. Illinois CPR Certification specializes in mobile CPR training and
                onsite BLS for dental offices, clinics, and healthcare teams across Chicagoland.
              </p>
            </details>
          </div>
          <p><a href="/faq/">See all FAQ answers →</a></p>
        </div>
      </section>

      <section class="section section-muted" id="quote">
        <div class="container contact-layout">
          <div>
            <h2>Request a quote for onsite BLS</h2>
            <p class="lede">
              Tell us your practice type, student count, and timeframe. We’ll follow up
              with options for mobile AHA BLS training at your location.
            </p>
            <p class="call-line">Phone <a href="tel:+18473217610">(847) 321-7610</a></p>
            <p class="call-line">
              Email
              <a href="mailto:contact@illinoiscprcertification.com">contact@illinoiscprcertification.com</a>
            </p>
          </div>
{QUOTE_FORM}
        </div>
      </section>
    </main>
{footer()}
  </body>
</html>
"""
write(ROOT / "index.html", home)

print("home done")

def page_shell(title, desc, path, current, body, *, extra_jsonld=None, noindex=False, crumb_items=None):
    extras = ""
    ld_blocks = [ORG_JSONLD]
    if crumb_items:
        crumb_html, crumb_ld = crumbs(crumb_items)
        ld_blocks.append(crumb_ld)
    else:
        crumb_html = ""
    if extra_jsonld:
        ld_blocks.append(extra_jsonld)
    # Combine into graph or multiple script tags - multiple script tags is cleaner
    extra_scripts = ""
    for block in ld_blocks[1:]:
        extra_scripts += f'    <script type="application/ld+json">\n{block}\n    </script>\n'
    html = f"""{head(title, desc, SITE + path, noindex=noindex, extra=extra_scripts)}
  <body>
{header(current)}
    <main id="main" class="site-main">
{crumb_html}
{body}
    </main>
{footer()}
  </body>
</html>
"""
    # Fix empty crumb leading newline issues
    out = ROOT / path.lstrip("/").rstrip("/")
    if path == "/":
        write(ROOT / "index.html", html)
    else:
        write(out / "index.html", html)


# ========== BLS ==========
bls_course_ld = """{
  "@context": "https://schema.org",
  "@type": "Course",
  "name": "American Heart Association BLS Provider",
  "description": "Instructor-led AHA Basic Life Support Provider course for healthcare providers, including hands-on CPR skills with feedback manikins and AHA BLS Provider course completion eCard upon successful completion.",
  "provider": {
    "@type": "Organization",
    "name": "Illinois CPR Certification",
    "url": "https://illinoiscprcertification.com/"
  },
  "offers": {
    "@type": "Offer",
    "availability": "https://schema.org/InStock",
    "url": "https://illinoiscprcertification.com/contact/"
  }
}"""

bls_body = r'''
      <section class="page-hero">
        <div class="container narrow">
          <p class="meta-line">AHA BLS Provider</p>
          <h1>AHA BLS Certification for Healthcare Providers</h1>
          <p class="lede">
            Instructor-led American Heart Association BLS Provider training for dental offices,
            clinics, and healthcare teams—delivered as mobile CPR training at your workplace
            across Chicagoland and Illinois.
          </p>
          <div class="btn-row">
            <a class="btn" href="/contact/#quote">Request a quote</a>
            <a class="btn btn-secondary" href="/onsite-group-training/">Onsite group training</a>
          </div>
        </div>
      </section>

      <section class="section">
        <div class="container prose">
          <h2>Who the AHA BLS Provider course is for</h2>
          <p>
            The American Heart Association BLS Provider course is designed for healthcare
            professionals who need BLS certification for work: dentists and dental hygienists,
            nurses, physicians, medical assistants, physical therapists, urgent care staff,
            hospital and network teams, and other clinicians who may need to respond to
            cardiac arrest in or out of hospital.
          </p>
          <p>
            If your employer or licensing board requires an AHA BLS Provider course completion
            card, this is the course built for that requirement. Always confirm with your
            employer or board which card they accept—AHA cards are accepted in all U.S. states,
            but each workplace sets its own rules.
          </p>

          <h2>What BLS covers</h2>
          <p>
            BLS focuses on high-quality CPR and team dynamics for single-rescuer and team
            Basic Life Support in in-hospital and out-of-hospital settings. Course skills include:
          </p>
          <ul>
            <li>Adult, child, and infant CPR</li>
            <li>AED use</li>
            <li>Bag-mask ventilation</li>
            <li>Relief of choking</li>
            <li>Team dynamics for multi-rescuer resuscitation</li>
          </ul>
          <p>
            Illinois CPR Certification teaches the current AHA BLS Provider curriculum with
            hands-on practice—not a lecture-only or online-only shortcut.
          </p>

          <h2>Hands-on skills with feedback manikins</h2>
          <p>
            Since January 31, 2019, the AHA has required instrumented directive feedback
            devices or manikins that give real-time rate and depth feedback in all courses
            that teach adult CPR. Your team practices compressions with that live feedback
            so skills match current AHA guidelines and course requirements.
          </p>
          <p>
            Online-only BLS does not meet AHA hands-on requirements and does not produce an
            AHA BLS Provider course completion card. If you need a card employers recognize,
            plan on a skills session with an AHA Instructor.
          </p>

          <dl class="course-facts">
            <div>
              <dt>Format</dt>
              <dd>Instructor-led classroom at your site (mobile / onsite)</dd>
            </div>
            <div>
              <dt>Initial course length</dt>
              <dd>About 4.5 hours with breaks (AHA estimate at a 1:6:2 instructor:student:manikin ratio)</dd>
            </div>
            <div>
              <dt>Renewal course length</dt>
              <dd>About 4 hours (AHA estimate at the same ratio)</dd>
            </div>
            <div>
              <dt>Card type</dt>
              <dd>AHA BLS Provider course completion eCard</dd>
            </div>
            <div>
              <dt>Validity</dt>
              <dd>Two years, through the end of the month issued</dd>
            </div>
            <div>
              <dt>Ages covered in skills</dt>
              <dd>Adult, child, and infant</dd>
            </div>
          </dl>

          <h2>Classroom and blended options</h2>
          <p>
            Most groups book a full instructor-led BLS Provider course on site. Some Training
            Centers also support HeartCode BLS (online cognitive portion) plus an in-person
            skills session.
          </p>
          <p class="todo-note">
            [TODO: confirm Jason offers HeartCode BLS skills sessions]
            <!-- TODO-JASON: confirm whether HeartCode BLS blended skills sessions are offered -->
          </p>

          <h2>eCard delivery and verification</h2>
          <p>
            After you successfully complete the skills and written requirements, course
            completion cards are issued through the AHA Training Center your instructor is
            aligned with. Training Centers must issue cards within 20 business days of
            successful completion; in practice, eCards often arrive sooner.
          </p>
          <p class="todo-note">
            Course completion cards are issued through [TODO: AHA Training Center name, City, IL].
            <!-- TODO-JASON: Training Center name, city, and state for BLS card issuance disclosure -->
          </p>
          <p>
            You can verify AHA eCards at
            <a href="https://www.heart.org/cpr/mycards" rel="noopener noreferrer">heart.org/cpr/mycards</a>.
          </p>

          <h2>Renewal every two years</h2>
          <p>
            Plan to renew BLS certification before your eCard expires. We schedule renewals
            for full teams so dental office BLS and clinic staff stay current together—often
            before or after clinic hours so you protect production time.
          </p>

          <h2>What to bring</h2>
          <ul>
            <li>A government-issued photo ID</li>
            <li>Comfortable clothes you can kneel and practice compressions in</li>
            <li>Any employer paperwork your credentialing team needs signed</li>
            <li>Your previous AHA BLS card if you are renewing (helpful, not always required)</li>
          </ul>

          <h2>Group size and pricing</h2>
          <p class="todo-note">
            [TODO: minimum and maximum group size per class]
            <!-- TODO-JASON: confirm min/max students per BLS class -->
          </p>
          <p>
            Pricing depends on group size, location, and whether you need initial or renewal
            courses. We do not publish rates here—<a href="/contact/#quote">request a quote</a>
            for onsite BLS training and we will follow up with options for your team.
          </p>

          <h2>Why teams book Illinois CPR Certification</h2>
          <ul class="why-list">
            <li><strong>Mobile first.</strong> AHA BLS at your office—no weekend classroom travel.</li>
            <li><strong>Healthcare-focused.</strong> Built around dental, clinic, PT, urgent care, and hospital schedules.</li>
            <li><strong>Current AHA requirements.</strong> Feedback manikins and instructor-led skills, not online-only claims.</li>
            <li><strong>Clear next steps.</strong> Quote, schedule, train, then eCards through the aligned Training Center.</li>
          </ul>
          <p>
            Ready to schedule? <a href="/contact/#quote">Request a quote for AHA BLS</a> or
            call <a href="tel:+18473217610">(847) 321-7610</a>. See also
            <a href="/onsite-group-training/">how onsite group training works</a> and
            <a href="/faq/">frequently asked questions</a>.
          </p>
        </div>
      </section>
'''

page_shell(
    "AHA BLS Certification | Illinois CPR",
    "American Heart Association BLS Provider course for healthcare teams. Onsite BLS certification with feedback manikins across Chicagoland.",
    "/bls-certification/",
    "bls",
    bls_body,
    extra_jsonld=bls_course_ld,
    crumb_items=[("/", "Home"), ("/bls-certification/", "BLS Certification")],
)

# ========== ONSITE ==========
onsite_body = r'''
      <section class="page-hero">
        <div class="container narrow">
          <p class="meta-line">Mobile / onsite</p>
          <h1>Onsite Group CPR Training Across Chicagoland</h1>
          <p class="lede">
            Illinois CPR Certification brings AHA BLS and mobile CPR training to your office—
            manikins, AED trainers, and materials included—so your team certifies without
            shutting down the day for travel.
          </p>
          <div class="btn-row">
            <a class="btn" href="/contact/#quote">Request a quote</a>
            <a class="btn btn-secondary" href="/bls-certification/">BLS course details</a>
          </div>
        </div>
      </section>

      <section class="section section-muted">
        <div class="container">
          <div class="section-head">
            <h2>How onsite BLS training works</h2>
            <p class="lede">Four clear steps from quote to eCards.</p>
          </div>
          <ol class="steps">
            <li>
              <h3>Book your date</h3>
              <p>Share your practice type, headcount, zip code, and timeframe. We confirm a written schedule once details are set.</p>
            </li>
            <li>
              <h3>We bring the equipment</h3>
              <p>Feedback manikins, AED trainers, and AHA course materials come with us—so you are not renting gear.</p>
            </li>
            <li>
              <h3>Train at your office</h3>
              <p>Your team practices high-quality CPR on site, taught by AHA Instructors, on a schedule that fits clinic flow.</p>
            </li>
            <li>
              <h3>eCards issued</h3>
              <p>After successful completion, AHA BLS Provider course completion eCards are issued through the aligned Training Center.</p>
            </li>
          </ol>
        </div>
      </section>

      <section class="section">
        <div class="container prose">
          <h2>What your site needs to provide</h2>
          <p>
            Training happens at the client’s location—not at a public classroom. Please plan for:
          </p>
          <ul>
            <li>A private room or open area large enough for kneeling practice</li>
            <li>Chairs for the cognitive portion and skills rotations</li>
            <li>Clear floor space for manikins (carpet or mats are fine)</li>
            <li>Access for the instructor to load in equipment</li>
            <li>A point of contact on site for check-in and schedule changes</li>
          </ul>
          <p>
            If your space is tight, tell us in the quote notes—we will help you plan group
            size and rotations.
          </p>

          <h2>Minimum group size and scheduling</h2>
          <p class="todo-note">
            [TODO: minimum group size for onsite training]
            <!-- TODO-JASON: confirm minimum students for onsite group BLS -->
          </p>
          <p class="todo-note">
            [TODO: confirm before/after hours and lunch-hour scheduling options]
            <!-- TODO-JASON: confirm scheduling windows (before clinic, after hours, lunch) -->
          </p>
          <p>
            Most healthcare teams prefer early morning, evening, or split sessions so
            production continues. Mention your ideal windows when you
            <a href="/contact/#quote">request a quote</a>.
          </p>
        </div>
      </section>

      <section class="section section-muted">
        <div class="container">
          <div class="section-head">
            <h2>Designed for organizations that need onsite CPR training</h2>
            <p class="lede">
              The same mobile model supports clinical teams and other groups that need
              the right American Heart Association course on site.
            </p>
          </div>
          <div class="audience-grid">
            <div class="audience-item">
              <h3>Healthcare &amp; medical offices</h3>
              <p>Primary care, specialty clinics, urgent care, and surgery centers that need AHA BLS for clinical staff.</p>
            </div>
            <div class="audience-item">
              <h3>Dental practices</h3>
              <p>General, pediatric, and oral surgery teams scheduling dental office BLS without weekend travel.</p>
            </div>
            <div class="audience-item">
              <h3>Schools &amp; training programs</h3>
              <p>Nursing, MA, CNA, allied health, and EMS students—contact us about the right AHA course for your team.</p>
            </div>
            <div class="audience-item">
              <h3>Public safety &amp; emergency response</h3>
              <p>Fire, EMS, and law enforcement teams that need healthcare-provider BLS or related AHA training.</p>
            </div>
            <div class="audience-item">
              <h3>Healthcare employers</h3>
              <p>Hospitals, skilled nursing, home health, and rehab networks coordinating group renewals.</p>
            </div>
            <div class="audience-item">
              <h3>Corporate &amp; community organizations</h3>
              <p>Occupational health, fitness, industrial, and community groups—contact us about the right AHA course for your team.</p>
            </div>
          </div>
        </div>
      </section>

      <section class="section">
        <div class="container prose">
          <h2>Practice types we quote every week</h2>
          <p>
            Use the quote form to select dental office, medical clinic, physical therapy,
            urgent care, hospital or network, or other corporate office. Each setting gets
            the same instructor-led BLS standards—with logistics tuned to your floor plan
            and shift pattern.
          </p>
          <h3>Dental offices</h3>
          <p>
            Hygienists, assistants, and dentists often renew together. Onsite BLS keeps
            the operatory schedule intact while meeting board and credentialing expectations.
          </p>
          <h3>Medical clinics &amp; physical therapy</h3>
          <p>
            Multi-provider clinics and PT offices use mobile CPR training to certify clinical
            and support staff in one visit.
          </p>
          <h3>Urgent care, hospitals &amp; networks</h3>
          <p>
            Larger groups can split into sessions. We help you plan headcount, rooms, and
            renewal timing so eCards stay current across locations.
          </p>
          <h3>Corporate offices</h3>
          <p>
            Some corporate teams need BLS; others need a different AHA course.
            Tell us who is training and we will point you to the right option—including
            contacting us about the right AHA course when BLS is not the fit.
          </p>
          <p>
            Explore the <a href="/bls-certification/">AHA BLS Provider course</a>,
            check <a href="/service-areas/">Chicagoland &amp; Illinois service areas</a>,
            or <a href="/contact/#quote">request a quote</a> now.
          </p>
        </div>
      </section>
'''

page_shell(
    "Onsite Group CPR Training | Illinois CPR",
    "Mobile onsite AHA BLS training for dental offices, clinics, and healthcare teams across Chicagoland and Illinois.",
    "/onsite-group-training/",
    "onsite",
    onsite_body,
    crumb_items=[("/", "Home"), ("/onsite-group-training/", "Onsite Training")],
)

print("bls+onsite done")

# Fix: wrap breadcrumbs in container for layout
def page_shell(title, desc, path, current, body, *, extra_jsonld=None, noindex=False, crumb_items=None):
    extra_scripts = ""
    if crumb_items:
        crumb_html_raw, crumb_ld = crumbs(crumb_items)
        crumb_html = f'      <div class="container" style="padding-top:1rem">{crumb_html_raw}\n      </div>'
        extra_scripts += f'    <script type="application/ld+json">\n{crumb_ld}\n    </script>\n'
    else:
        crumb_html = ""
    if extra_jsonld:
        extra_scripts += f'    <script type="application/ld+json">\n{extra_jsonld}\n    </script>\n'
    html = f"""{head(title, desc, SITE + path, noindex=noindex, extra=extra_scripts)}
  <body>
{header(current)}
    <main id="main" class="site-main">
{crumb_html}
{body}
    </main>
{footer()}
  </body>
</html>
"""
    if path.endswith("/") and path != "/":
        write(ROOT / path.strip("/") / "index.html", html)
    else:
        write(ROOT / "index.html", html)


# Re-generate BLS and onsite with fixed page_shell
page_shell(
    "AHA BLS Certification | Illinois CPR",
    "American Heart Association BLS Provider course for healthcare teams. Onsite BLS certification with feedback manikins across Chicagoland.",
    "/bls-certification/",
    "bls",
    bls_body,
    extra_jsonld=bls_course_ld,
    crumb_items=[("/", "Home"), ("/bls-certification/", "BLS Certification")],
)
page_shell(
    "Onsite Group CPR Training | Illinois CPR",
    "Mobile onsite AHA BLS training for dental offices, clinics, and healthcare teams across Chicagoland and Illinois.",
    "/onsite-group-training/",
    "onsite",
    onsite_body,
    crumb_items=[("/", "Home"), ("/onsite-group-training/", "Onsite Training")],
)

# ========== HEARTSAVER (draft, noindex, not in nav/sitemap) ==========
heartsaver_body = r'''
      <!-- TODO-JASON: confirm he teaches Heartsaver before indexing or linking this page -->
      <div class="draft-banner">DRAFT — TODO-JASON: confirm Heartsaver courses are offered before publishing</div>
      <section class="page-hero">
        <div class="container narrow">
          <p class="meta-line">Draft page</p>
          <h1>Heartsaver CPR AED &amp; First Aid</h1>
          <p class="lede">
            This draft describes American Heart Association Heartsaver training for non-clinical
            teams. It is not linked from the site navigation until Jason confirms these courses
            are offered.
          </p>
          <p class="todo-note">
            [TODO: confirm Jason teaches Heartsaver CPR AED / First Aid]
            <!-- TODO-JASON: confirm Heartsaver CPR AED and First Aid offerings, formats, and audiences -->
          </p>
        </div>
      </section>
      <section class="section">
        <div class="container prose">
          <h2>Who Heartsaver is typically for</h2>
          <p>
            Heartsaver courses are generally aimed at anyone with a duty to respond who is not
            a healthcare provider needing BLS—such as teachers, coaches, workplace responders,
            and community groups. Healthcare providers who need BLS certification should see the
            <a href="/bls-certification/">AHA BLS Provider course</a> instead.
          </p>
          <h2>What we would confirm before offering</h2>
          <ul>
            <li>Which Heartsaver modules are taught (CPR AED, First Aid, or combined)</li>
            <li>Whether training is onsite only or also open-enrollment</li>
            <li>Group minimums and card issuance through the aligned Training Center</li>
          </ul>
          <p>
            Until this page is confirmed, please <a href="/contact/">contact Illinois CPR Certification</a>
            about the right AHA course for your team, or request onsite
            <a href="/onsite-group-training/">group BLS training</a> if your staff needs BLS.
          </p>
        </div>
      </section>
'''

page_shell(
    "Heartsaver CPR AED First Aid | Draft",
    "Draft page for AHA Heartsaver CPR AED and First Aid. Confirm offerings with Illinois CPR Certification before booking.",
    "/heartsaver-cpr-aed-first-aid/",
    "home",
    heartsaver_body,
    noindex=True,
    crumb_items=[("/", "Home"), ("/heartsaver-cpr-aed-first-aid/", "Heartsaver (Draft)")],
)

# ========== SERVICE AREAS ==========
areas_body = r'''
      <section class="page-hero">
        <div class="container narrow">
          <p class="meta-line">Chicagoland &amp; Illinois</p>
          <h1>Mobile AHA BLS Across Chicagoland &amp; Illinois</h1>
          <p class="lede">
            Illinois CPR Certification provides mobile CPR training and onsite BLS certification
            at your workplace. We travel to client sites—we do not operate a public drop-in classroom
            at our Chicago mailing address.
          </p>
          <div class="btn-row">
            <a class="btn" href="/contact/#quote">Request a quote</a>
          </div>
        </div>
      </section>
      <section class="section">
        <div class="container prose">
          <h2>How service areas work</h2>
          <p>
            Our phone area code (847) is associated with the north and northwest Chicago suburbs,
            and our mailing office is in Chicago. Training itself is mobile: we bring AHA BLS
            courses to dental offices, clinics, hospitals, and other workplaces across Chicagoland
            and Illinois when travel is workable for your date and group size.
          </p>
          <p>
            We do not publish a fixed city-by-city list until Jason confirms each market. If you
            are unsure whether we reach your zip code, send it through the
            <a href="/contact/#quote">quote form</a> or call
            <a href="tel:+18473217610">(847) 321-7610</a>.
          </p>

          <h2>Cities &amp; counties to confirm</h2>
          <div class="todo-note">
            <p><strong>[TODO: Jason — confirm cities, counties, and travel radius]</strong></p>
            <!-- TODO-JASON: confirm served cities/counties and maximum travel radius for onsite BLS -->
            <ul>
              <li>Confirm Chicagoland counties regularly served</li>
              <li>Confirm any downstate Illinois travel or overnight rules</li>
              <li>Confirm zip-code radius or drive-time limit from Chicago / north suburbs</li>
              <li>List any cities that should appear publicly once verified</li>
            </ul>
          </div>

          <h2>What to expect when we travel to you</h2>
          <ul>
            <li>Instructor-led AHA BLS at your address</li>
            <li>Equipment brought on site (manikins, AED trainers, materials)</li>
            <li>Scheduling that can work around clinic hours when possible</li>
            <li>eCards issued through the aligned AHA Training Center after successful completion</li>
          </ul>
          <p>
            Learn more about <a href="/onsite-group-training/">onsite group training</a> or the
            <a href="/bls-certification/">AHA BLS Provider course</a>.
          </p>
        </div>
      </section>
'''

page_shell(
    "Service Areas | Chicagoland & Illinois CPR",
    "Mobile AHA BLS and CPR certification across Chicagoland and Illinois. Onsite training at your office—request a quote by zip code.",
    "/service-areas/",
    "areas",
    areas_body,
    crumb_items=[("/", "Home"), ("/service-areas/", "Service Areas")],
)

# ========== ABOUT ==========
about_person_ld = """{
  "@context": "https://schema.org",
  "@type": "Person",
  "name": "Jason Pierce",
  "jobTitle": "Owner & Lead Instructor",
  "worksFor": {
    "@type": "Organization",
    "name": "Illinois CPR Certification",
    "url": "https://illinoiscprcertification.com/"
  },
  "url": "https://illinoiscprcertification.com/about/"
}"""

about_body = r'''
      <section class="page-hero">
        <div class="container narrow">
          <p class="meta-line">Our story</p>
          <h1>About Illinois CPR Certification &amp; Jason Pierce</h1>
          <p class="lede">
            Illinois CPR Certification is a mobile training company focused on American Heart
            Association BLS for busy healthcare teams. Owned and taught by Jason Pierce, we
            bring instructor-led CPR certification to your clinic—not the other way around.
          </p>
        </div>
      </section>
      <section class="section">
        <div class="container prose">
          <h2>Mission</h2>
          <p>
            Healthcare schedules are tight. Weekend classroom travel and lost production make
            it harder to keep BLS cards current. Our mission is simple: deliver AHA BLS Provider
            training on site, on hours that work for dental offices, medical clinics, therapy
            practices, urgent care, and hospital teams across Chicagoland and Illinois.
          </p>
          <p>
            We follow current AHA guidelines and course requirements, use feedback manikins for
            adult CPR skills, and help teams leave with a clear path to their AHA BLS Provider
            course completion eCard after successful completion.
          </p>

          <h2>Why mobile training works for healthcare teams</h2>
          <ul>
            <li>Your staff stays in the building—no caravan to an off-site classroom</li>
            <li>Sessions can be timed around patients and shifts</li>
            <li>Whole teams renew together, which simplifies credentialing</li>
            <li>Equipment comes with the instructor, so you are not storing manikins year-round</li>
          </ul>

          <h2>Jason Pierce, Owner &amp; Lead Instructor</h2>
          <!-- TODO-JASON: confirm job title "Owner & Lead Instructor" -->
          <p>
            Jason Pierce has taught CPR and BLS classes in the Chicago area for years, working
            with healthcare and professional teams who need reliable, instructor-led training.
            He founded Illinois CPR Certification LLC to make onsite AHA BLS easier to schedule
            for practices that cannot spare a full day of travel.
          </p>
          <p class="todo-note">
            [TODO: credentials, exact years, background, AHA Training Center alignment, headshot]
            <!-- TODO-JASON: add Jason credentials, exact years teaching, background, TC alignment, and headshot image -->
          </p>
          <p class="todo-note">
            Course completion cards are issued through [TODO: AHA Training Center name, City, IL].
            <!-- TODO-JASON: Training Center name/city for About page disclosure -->
          </p>

          <h2>Business details</h2>
          <ul>
            <li><strong>Legal name:</strong> Illinois CPR Certification LLC</li>
            <li><strong>Office / mailing:</strong> 605 N Michigan Ave, Suite 454, Chicago, IL 60611</li>
            <li><strong>Phone:</strong> <a href="tel:+18473217610">(847) 321-7610</a></li>
            <li><strong>Email:</strong> <a href="mailto:contact@illinoiscprcertification.com">contact@illinoiscprcertification.com</a></li>
          </ul>
          <p>
            Ready to talk through a class?
            <a href="/contact/#quote">Request a quote</a> or read the
            <a href="/faq/">FAQ</a>.
          </p>
        </div>
      </section>
'''

page_shell(
    "About Jason Pierce | Illinois CPR",
    "Meet Illinois CPR Certification and owner Jason Pierce. Mobile AHA BLS training for healthcare teams across Chicagoland.",
    "/about/",
    "about",
    about_body,
    extra_jsonld=about_person_ld,
    crumb_items=[("/", "Home"), ("/about/", "About")],
)

print("heartsaver+areas+about done")

# ========== FAQ ==========
faq_qas = [
    (
        "Is online-only BLS valid for an AHA card?",
        "No. American Heart Association courses that teach CPR skills require a hands-on skills session. Online-only BLS does not produce an AHA BLS Provider course completion card. Illinois CPR Certification provides instructor-led skills training so your team can complete the requirements employers typically expect.",
    ),
    (
        "How long is the AHA BLS Provider class?",
        "The full BLS Provider course is about 4.5 hours with breaks. The renewal course is about 4 hours. Those are AHA timing estimates based on a 1:6:2 instructor:student:manikin ratio; your group size and remediation needs can change the clock time.",
    ),
    (
        "When do I get my eCard?",
        "After successful completion of the skills and written requirements, cards are issued through the AHA Training Center your instructor is aligned with. Training Centers must issue cards within 20 business days; eCards often arrive sooner. You can verify cards at heart.org/cpr/mycards.",
    ),
    (
        "How long is BLS certification good for?",
        "An AHA BLS Provider eCard is valid for two years, through the end of the month it was issued. Plan renewals before the expiration month so your dental office or clinic stays covered.",
    ),
    (
        "Do you come to our office?",
        "Yes. Mobile and onsite group training is the core of Illinois CPR Certification. We bring manikins, AED trainers, and materials to your workplace across Chicagoland and Illinois when travel works for your date and group.",
    ),
    (
        "How many people can be in a class?",
        "[TODO: minimum and maximum students per class]. AHA course quality depends on instructor-to-student and manikin ratios, so we size groups carefully. Tell us your headcount on the quote form.",
    ),
    (
        "What do we need to provide on site?",
        "A suitable room with chairs and enough clear floor space for kneeling compressions, plus access for equipment load-in and a site contact. Details are listed on the onsite group training page.",
    ),
    (
        "Do you offer BLS renewals?",
        "Yes. Most healthcare teams book renewals for the full staff so everyone stays on the same two-year cycle. Mention renewal vs initial training in your quote notes.",
    ),
    (
        "What if someone does not pass a skills test?",
        "AHA courses allow remediation within the course framework when a participant needs more practice. Participants must still meet AHA skills and written requirements to receive a course completion card. Instructors may pause or stop participation when safety is a concern.",
    ),
    (
        "Is the AHA BLS card accepted by the Illinois dental board and employers?",
        "AHA course completion cards are accepted in all U.S. states, but each employer, hospital credentialing office, and licensing board sets its own rules. Always confirm with your board or employer which card and renewal window they require.",
    ),
    (
        "How do I verify an AHA eCard?",
        "Use the American Heart Association eCard verification tools at https://www.heart.org/cpr/mycards. Employers often ask staff to share a verification link or screenshot from that portal.",
    ),
    (
        "How much does onsite BLS training cost?",
        "Pricing depends on group size, location, and initial vs renewal format. We do not list public prices—request a quote and we will follow up with options for your team.",
    ),
    (
        "What is your cancellation policy?",
        "See the Cancellation & Refund Policy for notice periods, rescheduling, and no-show terms. Several values are still marked for Jason to confirm.",
    ),
    (
        "Can you provide accessibility accommodations?",
        "Yes—we review reasonable accommodation requests in good faith. AHA allows reasonable accommodations, but students must still meet core skill requirements to receive a course completion card. Contact us before class day whenever possible; details are on the Accessibility page.",
    ),
]

import json as _json

faq_items_html = []
faq_ld_entities = []
for q, a in faq_qas:
    a_html = a
    replacements = [
        ("onsite group training page", '<a href="/onsite-group-training/">onsite group training page</a>'),
        ("Cancellation & Refund Policy", '<a href="/cancellation-refund-policy/">Cancellation &amp; Refund Policy</a>'),
        ("Accessibility page", '<a href="/accessibility/">Accessibility page</a>'),
        ("https://www.heart.org/cpr/mycards", '<a href="https://www.heart.org/cpr/mycards" rel="noopener noreferrer">heart.org/cpr/mycards</a>'),
    ]
    for old, new in replacements:
        a_html = a_html.replace(old, new)
    if "request a quote" in a_html and "<a href=\"/contact/#quote\">" not in a_html:
        a_html = a_html.replace("request a quote", '<a href="/contact/#quote">request a quote</a>', 1)
    if a.startswith("[TODO:"):
        a_html = f'{a} <!-- TODO-JASON: confirm class size limits for FAQ -->'

    faq_items_html.append(
        f"""            <details>
              <summary>{q}</summary>
              <p>{a_html}</p>
            </details>"""
    )
    faq_ld_entities.append(
        {
            "@type": "Question",
            "name": q,
            "acceptedAnswer": {"@type": "Answer", "text": a},
        }
    )

faq_ld = _json.dumps(
    {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": faq_ld_entities},
    ensure_ascii=False,
    indent=2,
)

faq_body = f'''
      <section class="page-hero">
        <div class="container narrow">
          <p class="meta-line">FAQ</p>
          <h1>CPR Certification &amp; AHA BLS FAQ</h1>
          <p class="lede">
            Straight answers about BLS certification, eCards, onsite logistics, and what
            Illinois CPR Certification provides for healthcare teams.
          </p>
        </div>
      </section>
      <section class="section">
        <div class="container">
          <div class="faq-list">
{chr(10).join(faq_items_html)}
          </div>
          <p style="margin-top:1.75rem">
            Still need details? <a href="/contact/#quote">Request a quote</a> or call
            <a href="tel:+18473217610">(847) 321-7610</a>.
          </p>
        </div>
      </section>
'''

page_shell(
    "CPR Certification FAQ | Illinois CPR",
    "FAQ for AHA BLS certification, eCards, renewals, onsite training logistics, and Illinois CPR Certification policies.",
    "/faq/",
    "faq",
    faq_body,
    extra_jsonld=faq_ld,
    crumb_items=[("/", "Home"), ("/faq/", "FAQ")],
)

# ========== CONTACT ==========
contact_body = f'''
      <section class="page-hero">
        <div class="container narrow">
          <p class="meta-line">Contact</p>
          <h1>Contact / Request a Quote</h1>
          <p class="lede">
            Ask about onsite AHA BLS for your dental office, clinic, or healthcare team.
            We serve Chicagoland and Illinois with mobile CPR training.
          </p>
        </div>
      </section>
      <section class="section">
        <div class="container contact-layout">
          <div>
            <div class="nap-block">
              <h2>Illinois CPR Certification</h2>
              <p>605 N Michigan Ave, Suite 454<br />Chicago, IL 60611</p>
              <p class="call-line">Phone <a href="tel:+18473217610">(847) 321-7610</a></p>
              <p class="call-line">
                Email
                <a href="mailto:contact@illinoiscprcertification.com">contact@illinoiscprcertification.com</a>
              </p>
              <p>Mobile AHA BLS training across Chicagoland &amp; Illinois</p>
              <p>Owned and taught by Jason Pierce</p>
              <p class="todo-note">
                [TODO: business hours]
                <!-- TODO-JASON: confirm public business hours for contact page -->
              </p>
            </div>
            <p>
              Prefer to review course details first? See the
              <a href="/bls-certification/">AHA BLS course for healthcare providers</a>
              or <a href="/onsite-group-training/">onsite group training</a>.
            </p>
          </div>
{QUOTE_FORM}
        </div>
      </section>
'''

page_shell(
    "Contact & Quote | Illinois CPR Certification",
    "Request a quote for onsite AHA BLS training. Call (847) 321-7610 or email contact@illinoiscprcertification.com.",
    "/contact/",
    "contact",
    contact_body,
    crumb_items=[("/", "Home"), ("/contact/", "Contact")],
)

print("faq+contact done")

# ========== PRIVACY ==========
privacy_body = r'''
      <section class="page-hero">
        <div class="container narrow">
          <p class="meta-line">Legal</p>
          <h1>Privacy Policy</h1>
          <p class="lede">Effective date: October 2, 2026</p>
        </div>
      </section>
      <section class="section">
        <div class="container prose">
          <!-- TODO-JASON: have Jason review; not legal advice -->
          <p>
            This Privacy Policy describes how Illinois CPR Certification LLC
            (“Illinois CPR Certification,” “we,” “us”) collects and uses information
            when you visit illinoiscprcertification.com or submit a quote request.
          </p>
          <p>
            <strong>Operator:</strong> Illinois CPR Certification LLC,
            605 N Michigan Ave, Suite 454, Chicago, IL 60611.
            Contact: <a href="mailto:contact@illinoiscprcertification.com">contact@illinoiscprcertification.com</a>,
            <a href="tel:+18473217610">(847) 321-7610</a>.
          </p>

          <h2>Information we collect</h2>
          <p>When you use the quote form, we collect:</p>
          <ul>
            <li>Name</li>
            <li>Email address</li>
            <li>Phone number</li>
            <li>Practice / company name</li>
            <li>Practice type</li>
            <li>Estimated student count</li>
            <li>Zip code</li>
            <li>Ideal timeframe</li>
            <li>Notes you choose to provide</li>
          </ul>
          <p>
            If you email or call us, we also receive the information you include in that message.
          </p>

          <h2>How we use information</h2>
          <ul>
            <li>To respond to quote requests and schedule training</li>
            <li>To operate and secure the website and admin tools</li>
            <li>To issue course completion credentials through the aligned AHA Training Center / AHA (student names and emails needed for eCards)</li>
            <li>To comply with law and enforce our terms</li>
          </ul>

          <h2>Where data is stored and who processes it</h2>
          <ul>
            <li><strong>Cloudflare D1:</strong> quote submissions are stored in a Cloudflare D1 database bound to this site.</li>
            <li><strong>Email:</strong> quote notifications are emailed to the business Google Workspace inboxes at contact@ and jason@illinoiscprcertification.com.</li>
            <li><strong>Cloudflare:</strong> Cloudflare processes HTTP requests and logs (observability is enabled on the Worker).</li>
            <li><strong>Google Fonts:</strong> fonts load from Google’s servers when you view the site.</li>
          </ul>

          <h2>Cookies</h2>
          <p>
            We do not use advertising or analytics cookies. The only first-party cookie we set is
            <code>icc_admin</code>, an HttpOnly session cookie used so the site owner can sign in
            to the private quote inbox at /admin. That cookie is set only after a successful admin login.
          </p>

          <h2>Analytics and sale of data</h2>
          <p>
            We do not run a third-party analytics pixel on this site, and we do not sell personal information.
          </p>

          <h2>Student data for eCards</h2>
          <p>
            To issue AHA course completion eCards, student names and email addresses are shared with
            the AHA Training Center the instructor is aligned with and with the American Heart Association
            as required for card issuance and verification.
          </p>

          <h2>Retention</h2>
          <p class="todo-note">
            [TODO: data retention period for quote records and emails]
            <!-- TODO-JASON: confirm how long quote records and related emails are retained -->
          </p>

          <h2>Your requests</h2>
          <p>
            To ask questions about your information, or to request access or deletion where applicable,
            email <a href="mailto:contact@illinoiscprcertification.com">contact@illinoiscprcertification.com</a>.
          </p>

          <h2>Changes</h2>
          <p>
            We may update this Privacy Policy. The effective date above will change when we post a revision.
          </p>
        </div>
      </section>
'''

page_shell(
    "Privacy Policy | Illinois CPR Certification",
    "Privacy Policy for Illinois CPR Certification LLC: quote form data, Cloudflare D1 storage, email notices, and cookies.",
    "/privacy-policy/",
    "home",
    privacy_body,
    crumb_items=[("/", "Home"), ("/privacy-policy/", "Privacy Policy")],
)

# ========== TERMS ==========
terms_body = r'''
      <section class="page-hero">
        <div class="container narrow">
          <p class="meta-line">Legal</p>
          <h1>Terms of Service</h1>
          <p class="lede">Effective date: October 2, 2026</p>
        </div>
      </section>
      <section class="section">
        <div class="container prose">
          <!-- TODO-JASON: have attorney review Terms; Illinois/Cook County venue marked for confirmation -->
          <p>
            These Terms of Service (“Terms”) govern your use of illinoiscprcertification.com
            and related communications with Illinois CPR Certification LLC (“we,” “us,” “our”),
            605 N Michigan Ave, Suite 454, Chicago, IL 60611.
          </p>

          <h2>Who we are</h2>
          <p>
            Illinois CPR Certification LLC provides in-person, instructor-led American Heart
            Association training—primarily mobile AHA BLS Provider courses for healthcare teams.
            We are an independent training provider and are not owned, operated, or sponsored by
            the American Heart Association.
          </p>

          <h2>Site use</h2>
          <p>
            You may use this website for lawful purposes: learning about our services, requesting
            a quote, and contacting us. You may not misuse the site, attempt unauthorized access
            to /admin or /api routes, scrape in a way that degrades service, or submit malicious
            or fraudulent content.
          </p>

          <h2>Quotes and booking</h2>
          <p>
            Quote requests submitted through the website are inquiries, not binding contracts.
            A class is not booked until we confirm date, location, headcount, course type, and
            price in writing (email is fine). Either party may decline to proceed before that
            written confirmation.
          </p>

          <h2>Course completion and cards</h2>
          <p>
            Course completion depends on meeting American Heart Association skills and written
            test requirements. Attendance alone does not guarantee a course completion card.
            Cards are issued through the AHA Training Center the instructor is aligned with,
            not as a certificate created by this website. Timelines follow AHA Training Center rules.
          </p>

          <h2>Safety and instructor authority</h2>
          <p>
            CPR training involves physical activity, including kneeling and chest compressions.
            Participants should monitor their own condition and follow instructor safety directions.
            Instructors may pause or stop a participant’s skills practice when safety requires it.
            The client provides a suitable training space (room, chairs, and clear floor area).
          </p>

          <h2>Assumption of risk</h2>
          <p>
            By participating, you acknowledge that hands-on resuscitation practice includes
            physical exertion and ordinary risks of kneeling, lifting practice equipment, and
            repeated compressions. Tell the instructor about relevant physical limitations
            before skills practice begins.
          </p>

          <h2>No medical advice</h2>
          <p>
            Training content is educational. Nothing on this site or in a course is medical advice,
            diagnosis, or treatment. In an emergency, call 911 (or your local emergency number).
          </p>

          <h2>American Heart Association</h2>
          <p>
            The AHA is not a party to these Terms. Use of AHA materials does not mean AHA sponsorship.
            See our <a href="/aha-disclaimer/">AHA Disclaimer</a> for required notices.
          </p>

          <h2>Disclaimer of warranties</h2>
          <p>
            The website is provided “as is.” To the fullest extent permitted by law, we disclaim
            warranties of merchantability, fitness for a particular purpose, and non-infringement
            regarding the site and informational content.
          </p>

          <h2>Limitation of liability</h2>
          <p>
            To the fullest extent permitted by law, Illinois CPR Certification LLC and its
            instructors are not liable for indirect, incidental, special, consequential, or
            punitive damages arising from site use or training logistics discussions. Our total
            liability for claims arising from the site or a quote inquiry is limited to the
            greater of fees you paid us for the specific confirmed class giving rise to the claim,
            or one hundred U.S. dollars if no class fee was paid. Some limits may not apply where
            prohibited by law.
          </p>

          <h2>Indemnification</h2>
          <p>
            You agree to indemnify and hold harmless Illinois CPR Certification LLC from claims
            arising out of your misuse of the site, your inaccurate form submissions, or your
            failure to provide a safe training space when you are the booking client—except to
            the extent caused by our willful misconduct.
          </p>

          <h2>Intellectual property</h2>
          <p>
            Site text, layout, and our logos are owned by Illinois CPR Certification LLC or used
            under license. AHA materials remain the property of the American Heart Association
            and are used under AHA program rules. You may not copy course materials for resale
            or redistribution.
          </p>

          <h2>DMCA contact</h2>
          <p>
            Copyright concerns: email
            <a href="mailto:contact@illinoiscprcertification.com">contact@illinoiscprcertification.com</a>
            with “DMCA” in the subject line.
          </p>

          <h2>Privacy</h2>
          <p>
            Personal information is handled as described in our
            <a href="/privacy-policy/">Privacy Policy</a>.
          </p>

          <h2>Severability and entire agreement</h2>
          <p>
            If a provision of these Terms is unenforceable, the rest remains in effect.
            These Terms, plus any written class confirmation we send, are the entire agreement
            for website use and quote inquiries. Confirmed classes may also include additional
            written terms specific to that booking.
          </p>

          <h2>Governing law and venue</h2>
          <p>
            These Terms are governed by the laws of the State of Illinois, without regard to
            conflict-of-law rules. Exclusive venue for disputes relating to the site or these
            Terms lies in the state or federal courts located in Cook County, Illinois
            <span class="todo-note">[TODO: Jason/attorney confirm venue]</span>.
            <!-- TODO-JASON: attorney confirm Illinois governing law and Cook County venue -->
          </p>

          <h2>Changes</h2>
          <p>
            We may update these Terms by posting a new version with a revised effective date.
          </p>

          <h2>Contact</h2>
          <p>
            Illinois CPR Certification LLC<br />
            605 N Michigan Ave, Suite 454, Chicago, IL 60611<br />
            <a href="tel:+18473217610">(847) 321-7610</a> ·
            <a href="mailto:contact@illinoiscprcertification.com">contact@illinoiscprcertification.com</a>
          </p>
        </div>
      </section>
'''

page_shell(
    "Terms of Service | Illinois CPR Certification",
    "Terms of Service for Illinois CPR Certification LLC: site use, quotes, AHA course completion, liability, and Illinois law.",
    "/terms/",
    "home",
    terms_body,
    crumb_items=[("/", "Home"), ("/terms/", "Terms of Service")],
)

# ========== CANCELLATION ==========
cancel_body = r'''
      <section class="page-hero">
        <div class="container narrow">
          <p class="meta-line">Legal</p>
          <h1>Cancellation &amp; Refund Policy</h1>
          <p class="lede">Effective date: October 2, 2026</p>
        </div>
      </section>
      <section class="section">
        <div class="container prose">
          <!-- TODO-JASON: fill in notice periods, fees, and refund percentages before relying on this policy -->
          <p>
            This policy applies to onsite classes booked with Illinois CPR Certification LLC
            after a written confirmation. Website quote requests are not bookings until confirmed
            in writing.
          </p>

          <h2>Client cancellation</h2>
          <p class="todo-note">
            [TODO: notice period required to cancel without fee]
            <!-- TODO-JASON: cancellation notice period -->
          </p>
          <p class="todo-note">
            [TODO: fee or percent if canceled inside the notice window]
            <!-- TODO-JASON: late cancellation fee -->
          </p>

          <h2>Rescheduling</h2>
          <p class="todo-note">
            [TODO: how many days’ notice to reschedule; any reschedule fee]
            <!-- TODO-JASON: rescheduling rules -->
          </p>

          <h2>No-shows</h2>
          <p class="todo-note">
            [TODO: no-show policy for the group or individual participants]
            <!-- TODO-JASON: no-show policy -->
          </p>

          <h2>Refunds</h2>
          <p class="todo-note">
            [TODO: when deposits or payments are refundable; method and timing]
            <!-- TODO-JASON: refund rules -->
          </p>

          <h2>Instructor or company cancellation</h2>
          <p>
            If Illinois CPR Certification must cancel a confirmed class (weather, instructor
            illness, safety, or similar), you will receive a full refund of fees paid for that
            session <strong>or</strong> the option to reschedule at no additional instructor
            cancellation fee—your choice.
          </p>

          <h2>Course completion</h2>
          <p>
            Fees cover instruction for the scheduled session. Course completion cards are issued
            only after AHA skills and written requirements are met; not completing those
            requirements is not, by itself, grounds for a refund.
          </p>

          <h2>Questions</h2>
          <p>
            Email <a href="mailto:contact@illinoiscprcertification.com">contact@illinoiscprcertification.com</a>
            or call <a href="tel:+18473217610">(847) 321-7610</a>.
          </p>
        </div>
      </section>
'''

page_shell(
    "Cancellation & Refund Policy | Illinois CPR",
    "Cancellation and refund policy for Illinois CPR Certification onsite classes, including instructor-cancellation remedies.",
    "/cancellation-refund-policy/",
    "home",
    cancel_body,
    crumb_items=[("/", "Home"), ("/cancellation-refund-policy/", "Cancellation & Refund")],
)

print("privacy+terms+cancel done")

# ========== ACCESSIBILITY ==========
# Based on Jason's policy nearly verbatim; support@ → contact@; address without 70052; WCAG paragraph added
access_body = r'''
      <section class="page-hero">
        <div class="container narrow">
          <p class="meta-line">Policy</p>
          <h1>Accessibility &amp; Non-Discrimination</h1>
          <p class="lede">Illinois CPR Certification LLC commitment to equal access.</p>
        </div>
      </section>
      <section class="section">
        <div class="container prose">
          <p>
            Illinois CPR Certification LLC is committed to providing its services in a manner
            that affords individuals full and equal access consistent with applicable law. We do
            not exclude, deny services to, or otherwise discriminate against any person on the
            basis of disability, medical condition, race, color, religion, sex, gender, gender
            identity, gender expression, sexual orientation, marital status, national origin,
            ancestry, citizenship, immigration status, primary language, age, veteran status, or
            any other status protected by applicable law.
          </p>
          <p>
            If you need a reasonable accommodation, reasonable modification, auxiliary aid or
            service, alternative format, or other accessibility-related assistance in order to
            access our website, register for a course, communicate with us, enter a training
            location, or participate in our services, please contact us at
            <a href="mailto:contact@illinoiscprcertification.com">contact@illinoiscprcertification.com</a>
            or <a href="tel:+18473217610">(847) 321-7610</a>.
            <!-- TODO-JASON: original policy listed support@; only contact@ and jason@ inboxes exist—confirm if support@ should be created -->
            We request advance notice whenever possible so that we can evaluate the request and
            make arrangements, but we will consider requests made at any time.
          </p>
          <p>
            Some course content, audiovisual materials, and digital resources used in our services
            are licensed from third-party providers. Because we may not own or control those
            materials, we may not always be able to alter the underlying source content itself.
            However, we will consider requests for reasonable accommodations, auxiliary aids or
            services, alternative formats, supplemental materials, alternative methods of
            communication, or other effective means of access in connection with such materials,
            consistent with applicable law.
          </p>
          <p>
            Illinois CPR Certification LLC reviews requests for accommodations, modifications,
            and accessibility assistance on an individualized basis and in good faith. When
            appropriate, we may ask for information reasonably necessary to understand the request
            and identify an effective solution, to the extent permitted by law. If a requested
            accommodation cannot be provided as requested, we may offer an alternative
            accommodation, communication method, format, scheduling option, or other measure that
            we determine is reasonable and effective under the circumstances.
          </p>
          <p>
            We may decline a particular request only to the extent permitted by law, including
            where the requested measure would fundamentally alter the nature of the service,
            impose an undue burden, create a direct threat to the health or safety of any person
            that cannot be mitigated by reasonable measures, or require us to waive legitimate
            safety requirements based on actual risks rather than speculation, stereotypes, or
            generalizations.
          </p>
          <p>
            The American Heart Association allows reasonable accommodations in courses, but a
            student must still meet core skill requirements to receive a course completion card.
            Participants remain responsible for monitoring their own physical condition and
            complying with stated safety instructions. If you have questions about whether a
            course format or training setup can be modified or adjusted, please contact us before
            participation so we can discuss available options.
          </p>

          <h2>Website accessibility</h2>
          <p>
            We aim for this website to conform to the Web Content Accessibility Guidelines (WCAG)
            2.1 Level AA. That includes semantic structure, keyboard-accessible navigation,
            readable contrast, and text alternatives for images. If you encounter a barrier on
            the site, tell us what page and assistive technology you were using so we can fix it.
          </p>

          <h2>Contact for accessibility feedback</h2>
          <p>
            If you encounter an accessibility barrier on our website or in our services, or if
            you have feedback regarding accessibility, please contact us at
            <a href="mailto:contact@illinoiscprcertification.com">contact@illinoiscprcertification.com</a>,
            <a href="tel:+18473217610">(847) 321-7610</a>, or
            605 N Michigan Ave, Suite 454, Chicago, IL 60611.
          </p>
        </div>
      </section>
'''

page_shell(
    "Accessibility Policy | Illinois CPR",
    "Accessibility and non-discrimination policy for Illinois CPR Certification LLC, including WCAG 2.1 AA website goals.",
    "/accessibility/",
    "home",
    access_body,
    crumb_items=[("/", "Home"), ("/accessibility/", "Accessibility")],
)

# ========== AHA DISCLAIMER ==========
aha_body = f'''
      <section class="page-hero">
        <div class="container narrow">
          <p class="meta-line">Compliance</p>
          <h1>AHA Disclaimer &amp; Trademark Notice</h1>
          <p class="lede">
            Required notices about American Heart Association courses, trademarks, and fees.
          </p>
        </div>
      </section>
      <section class="section">
        <div class="container prose">
          <h2>Course fees disclaimer</h2>
          <p>{AHA_DISCLAIMER}</p>

          <h2>Trademark notice</h2>
          <p>{TRADEMARK}</p>

          <h2>No AHA sponsorship</h2>
          <p>
            Illinois CPR Certification is an independent training provider. Use of AHA
            instructional materials in an educational course does not represent course sponsorship
            by the AHA. The American Heart Association does not set our course fees and does not
            receive our course income, except for the portion of fees needed for AHA course materials
            as described above.
          </p>

          <h2>Training Center disclosure</h2>
          <p class="todo-note">
            Course completion cards are issued through [TODO: AHA Training Center name, City, IL].
            <!-- TODO-JASON: Training Center name and city for AHA Disclaimer page -->
          </p>

          <h2>eCard verification</h2>
          <p>
            AHA course completion eCards can be verified at
            <a href="https://www.heart.org/cpr/mycards" rel="noopener noreferrer">https://www.heart.org/cpr/mycards</a>.
          </p>

          <h2>Hands-on skills requirement</h2>
          <p>
            Online-only courses do not meet AHA hands-on skills requirements for CPR. AHA courses
            that teach CPR skills require a hands-on skills session. Online-only BLS does not
            produce an AHA BLS Provider course completion card.
          </p>

          <h2>Wording we avoid</h2>
          <p>
            Consistent with AHA guidance, we do not claim that professionals are “AHA-certified”
            or that courses are “AHA-compliant” as a marketing label. We describe training as
            American Heart Association BLS Provider courses, taught by AHA Instructors, that follow
            current AHA guidelines and course requirements, with AHA BLS Provider course completion
            eCards issued after successful completion.
          </p>
          <p>
            Related pages:
            <a href="/bls-certification/">AHA BLS Provider course</a>,
            <a href="/terms/">Terms of Service</a>,
            <a href="/contact/">Contact</a>.
          </p>
        </div>
      </section>
'''

page_shell(
    "AHA Disclaimer | Illinois CPR Certification",
    "American Heart Association course-fee disclaimer, trademark notice, Training Center disclosure, and eCard verification for Illinois CPR Certification.",
    "/aha-disclaimer/",
    "home",
    aha_body,
    crumb_items=[("/", "Home"), ("/aha-disclaimer/", "AHA Disclaimer")],
)

# ========== 404 ==========
not_found = f"""{head(
    "Page not found | Illinois CPR Certification",
    "The page you requested is not available. Return home or request a quote for onsite AHA BLS training.",
    f"{SITE}/404.html",
    noindex=True,
)}
  <body>
{header("home")}
    <main id="main" class="site-main">
      <section class="page-hero">
        <div class="container narrow">
          <h1>Page not found</h1>
          <p class="lede">
            That URL is not on this site. Try one of these pages, or request a quote for
            mobile AHA BLS training.
          </p>
          <div class="btn-row">
            <a class="btn" href="/">Home</a>
            <a class="btn btn-secondary" href="/bls-certification/">AHA BLS course</a>
            <a class="btn btn-secondary" href="/contact/">Request a quote</a>
          </div>
          <ul>
            <li><a href="/onsite-group-training/">Onsite group training</a></li>
            <li><a href="/faq/">FAQ</a></li>
            <li><a href="/about/">About Jason Pierce</a></li>
            <li><a href="/service-areas/">Service areas</a></li>
          </ul>
        </div>
      </section>
    </main>
{footer()}
  </body>
</html>
"""
write(ROOT / "404.html", not_found)

# ========== robots + sitemap ==========
robots = """User-agent: *
Allow: /
Disallow: /admin
Disallow: /api/
Sitemap: https://illinoiscprcertification.com/sitemap.xml
"""
write(ROOT / "robots.txt", robots)

pages = [
    "/",
    "/bls-certification/",
    "/onsite-group-training/",
    "/service-areas/",
    "/about/",
    "/faq/",
    "/contact/",
    "/privacy-policy/",
    "/terms/",
    "/cancellation-refund-policy/",
    "/accessibility/",
    "/aha-disclaimer/",
]
# Heartsaver intentionally excluded (noindex draft)
sitemap_urls = "\n".join(
    f"""  <url>
    <loc>{SITE}{p if p != "/" else "/"}</loc>
    <lastmod>{TODAY}</lastmod>
  </url>"""
    for p in pages
)
# Fix home loc
sitemap_urls = sitemap_urls.replace(f"{SITE}/", f"{SITE}/", 1)

sitemap = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{sitemap_urls}
</urlset>
"""
write(ROOT / "sitemap.xml", sitemap)

print("ALL PAGES GENERATED")
