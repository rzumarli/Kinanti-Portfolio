# -*- coding: utf-8 -*-
"""Build 6 case study pages for the Kinanti portfolio from the site shell."""
import os

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SHELL = os.path.join(REPO, 'scripts', 'shell') + os.sep

prefix = open(SHELL + 'prefix.html', encoding='utf-8').read()
header = open(SHELL + 'header.html', encoding='utf-8').read()
footer = open(SHELL + 'footer.html', encoding='utf-8').read()
suffix = open(SHELL + 'suffix.html', encoding='utf-8').read()

CSS = """
<style>
.cs{max-width:880px;margin:0 auto;width:100%;font-family:"DM Sans",system-ui,sans-serif;color:#363636}
.cs-back{font-family:Silkscreen,monospace;font-size:14px;color:#363636;text-decoration:none;display:inline-block;margin-bottom:20px}
.cs-back:hover{text-decoration:underline}
.cs-kicker{display:inline-block;font-family:Silkscreen,monospace;font-size:13px;font-weight:700;padding:7px 16px;border:2px solid #363636;border-radius:999px}
.cs h1{font-family:Silkscreen,monospace;font-size:40px;line-height:1.18;margin:20px 0 12px;font-weight:700}
.cs-sub{font-size:19px;line-height:1.55;color:#4e4e4e;margin:0}
.cs-meta{display:grid;grid-template-columns:repeat(auto-fit,minmax(170px,1fr));gap:18px 28px;border-top:2px solid #363636;border-bottom:2px solid #363636;padding:22px 0;margin:30px 0 34px}
.cs-meta dt{font-family:Silkscreen,monospace;font-size:12px;letter-spacing:.06em;text-transform:uppercase;color:#8a8178;margin:0 0 6px}
.cs-meta dd{margin:0;font-size:16px;font-weight:600;line-height:1.45}
.cs-cover{width:100%;height:auto;border:2px solid #363636;border-radius:20px;display:block;margin:0 0 8px}
.cs h2{font-family:Silkscreen,monospace;font-size:23px;line-height:1.3;margin:46px 0 14px;font-weight:700}
.cs h3{font-family:Silkscreen,monospace;font-size:16px;line-height:1.4;margin:26px 0 10px;font-weight:700}
.cs p{font-size:17px;line-height:1.7;color:#4e4e4e;margin:0 0 14px}
.cs p strong,.cs li strong{color:#363636}
.cs ul,.cs ol{font-size:17px;line-height:1.65;color:#4e4e4e;margin:0 0 16px;padding-left:24px}
.cs li{margin-bottom:8px}
.cs-stats{display:grid;grid-template-columns:repeat(auto-fit,minmax(160px,1fr));gap:14px;margin:24px 0 8px}
.cs-stat{background:#fff;border:2px solid #363636;border-radius:16px;padding:16px 18px}
.cs-stat b{font-family:Silkscreen,monospace;font-size:25px;display:block;margin-bottom:5px;line-height:1.15}
.cs-stat span{font-size:14px;color:#4e4e4e;line-height:1.45;display:block}
.cs-cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));gap:14px;margin:20px 0 8px}
.cs-card{background:#fff;border:2px solid #363636;border-radius:16px;padding:18px 20px}
.cs-card h3{margin-top:0}
.cs-card p,.cs-card li{font-size:15.5px}
.cs-card ul{font-size:15.5px;margin-bottom:4px}
.cs-callout{background:#fff;border:2px solid #363636;border-left:10px solid #e8ee58;border-radius:16px;padding:18px 22px;margin:22px 0}
.cs-callout p{margin:0;font-size:17px}
.cs-pkgs{display:grid;grid-template-columns:repeat(auto-fit,minmax(185px,1fr));gap:14px;margin:20px 0 8px}
.cs-pkg{background:#fff;border:2px solid #363636;border-radius:16px;padding:16px 18px}
.cs-pkg h3{margin:0 0 4px;font-size:18px}
.cs-pkg .tag{display:inline-block;font-family:Silkscreen,monospace;font-size:11px;font-weight:700;background:#f85c36;color:#fff;border-radius:999px;padding:3px 10px;margin:2px 0 8px}
.cs-pkg ul{font-size:14px;padding-left:18px;margin:6px 0 0}
.cs-pkg li{margin-bottom:5px;line-height:1.5}
.cs-swatches{display:flex;flex-wrap:wrap;gap:12px;margin:18px 0 6px}
.cs-sw{width:92px}
.cs-sw i{display:block;height:46px;border:2px solid #363636;border-radius:10px;margin-bottom:6px}
.cs-sw span{font-size:12px;line-height:1.4;display:block;color:#4e4e4e}
.cs-sw b{color:#363636;display:block;font-size:12.5px}
.cs-src{margin-top:56px;padding-top:18px;border-top:2px solid #363636;font-size:14px;color:#8a8178}
.cs-src a{color:#363636}
@media (max-width:640px){.cs h1{font-size:29px}.cs h2{font-size:20px}.cs-sub{font-size:17px}.cs p,.cs ul,.cs ol{font-size:16px}}
</style>
"""


CASE_DESC = {
 'mobile-pos.html': 'UX research case study evaluating Mobile POS usage by store cashiers for an outdoor retail company: field observation, think-aloud testing, and interviews.',
 'dbank-pro.html': 'Studi kasus redesign fitur Top Up dan Info Kartu Kredit DBank Pro dari Bank Danamon, dengan skor usability testing rata-rata 8,6 dari 10.',
 'upcademy.html': 'Studi kasus UX UpCademy, platform edukasi online: desain flow pendaftaran, transaksi kelas, dan pembelajaran dengan metode Design Thinking.',
 'waste4change.html': 'Studi kasus redesign layanan Send Your Waste dari Waste4Change: form pengiriman, pembayaran, dan redeem points untuk desktop dan mobile.',
 'niagahoster.html': 'Redesign halaman checkout Niagahoster agar pengguna lebih cepat dan percaya diri memilih paket hosting, teruji dengan nilai rata-rata 8,5 dari 10.',
 'warunk-upnormal.html': 'Case study on bringing customers back to Warunk Upnormal: desk research, interviews, and three solution tracks, from feedback rewards to self-service Indomie.',
}
PROJECT_DESC = 'Selected UI/UX projects by Kinanti Ayudya Putri Rahardiani: Mobile POS research, DBank Pro redesign, Waste4Change, Niagahoster checkout, UpCademy, and more.'


def build(slug, title, body):
    head = prefix.replace('<title>Projects — Kinanti</title>', f'<title>{title}</title>')
    if slug in CASE_DESC:
        head = head.replace(PROJECT_DESC, CASE_DESC[slug])
        if slug in ('dbank-pro.html', 'upcademy.html', 'waste4change.html', 'niagahoster.html'):
            head = head.replace('<html lang="en">', '<html lang="id">', 1)
    head = head.replace('</head>', CSS + '\n</head>')
    close1 = suffix[:suffix.index('</main>') + len('</main>')]
    assert suffix.startswith(close1)
    html = head + header + body + close1 + footer + suffix[len(close1):]
    path = os.path.join(REPO, slug)
    open(path, 'w', encoding='utf-8').write(html)
    print(slug, len(html))


def hero(kicker_bg, kicker_fg, kicker, title, sub, meta, cover, cover_alt):
    items = ''.join(f'<div><dt>{k}</dt><dd>{v}</dd></div>' for k, v in meta)
    return f"""
<article class="cs">
<a class="cs-back" href="project.html">&larr; All projects</a>
<div><span class="cs-kicker" style="background:{kicker_bg};color:{kicker_fg}">{kicker}</span></div>
<h1>{title}</h1>
<p class="cs-sub">{sub}</p>
<dl class="cs-meta">{items}</dl>
<img class="cs-cover" src="assets/{cover}" alt="{cover_alt}" />
"""

# ---------------------------------------------------------------- Mobile POS
body = hero(
    '#e8ee58', '#363636', 'UX Research · Case Study',
    'Mobile POS Usage Evaluation',
    'Evaluating how store cashiers actually use Mobile POS, why adoption differed so much between stores, and what would help it spread. A UX research case study for an outdoor retail company.',
    [('Role', 'UI/UX Designer &amp; Researcher'), ('Users', 'Store cashiers'),
     ('Methods', 'Field observation · Think-aloud usability testing · In-depth interviews'),
     ('Note', 'Under NDA, the brand name is omitted')],
    'project-mpos.png', 'Mobile POS Usage Evaluation cover')
body += """
<h2>Overview</h2>
<p>This project focused on evaluating Mobile POS usage and adoption across physical stores, with the goal of understanding cashier behavior, identifying usability challenges, and uncovering opportunities to improve the overall experience. The findings were translated into recommendations to improve the experience and support wider adoption across stores. My contribution covered research support, interview moderation, research synthesis, usability testing, UX analysis, and the UX recommendations, working together with a Senior UX Researcher.</p>

<h2>Background</h2>
<p>Mobile POS was built to help reduce queues at checkouts, especially during peak seasons such as weekends and special events, when longer checkout times put pressure on cashiers and hurt the shopping experience. But months after rollout, adoption looked uneven. Some stores used it daily, others barely touched it. That led to one question: <strong>was the existing Mobile POS actually helping cashiers do their jobs more efficiently?</strong></p>

<h2>Objectives</h2>
<ol>
<li><strong>Usage evaluation.</strong> Evaluate cashiers' understanding of the Mobile POS workflow, and assess how effectively the system supports their daily tasks.</li>
<li><strong>Problem identification.</strong> Identify what prevents cashiers from using Mobile POS effectively, including technical, procedural, or work-habit factors that hinder adoption.</li>
<li><strong>Needs assessment.</strong> Understand which features support cashiers' performance, along with their expectations, preferences, and motivations to use Mobile POS more actively.</li>
</ol>

<h2>Research methods</h2>
<div class="cs-cards">
<div class="cs-card"><h3>1 · Field observation</h3><p>Direct observation of cashiers' behavior during in-store transactions, with and without Mobile POS, to understand their interaction with the device, the obstacles, and their actual workflow. Due to low customer traffic in some stores, only one store could be observed during peak hours.</p></div>
<div class="cs-card"><h3>2 · Think-aloud usability testing</h3><p>Cashiers demonstrated the payment process, the core scenario, using Mobile POS while verbalizing their thoughts. This showed what they found intuitive, where they hit obstacles, and what they looked for to complete the task.</p></div>
<div class="cs-card"><h3>3 · In-depth interviews</h3><p>One-on-one interviews with cashiers from two stores, one with high adoption and one with low adoption at similar revenue, to dig into personal experience, motivation, preference, perception, challenges, and needs.</p></div>
</div>

<h2>Findings</h2>
<p>After the research, one thing stood out: <strong>one store was using Mobile POS daily, while the other did not use it at all.</strong> Mapping the general user journey, the number of users dropped at the transition between considering Mobile POS and actually choosing to use it. Combining the insights from all three methods, three crucial points affected that decision:</p>
<h3>1 · Store area &amp; till capacity</h3>
<p>The two stores differed a lot in size, one was nearly 3 times larger than the other, with two tills versus one, while their average sales were close. The larger store felt its existing tills could handle the traffic, so staff felt Mobile POS was unnecessary. The smaller store, with one till, limited space, and long queues, relied on Mobile POS to keep customers moving.</p>
<h3>2 · Team availability</h3>
<p>When the store got busy, retail assistants were needed on the floor across different sections, so most prioritized serving customers over operating Mobile POS. Only a subset of staff was authorized to handle transactions, which limited who could run Mobile POS during peak hours.</p>
<h3>3 · The Mobile POS till area</h3>
<p>Mobile POS still needs a physical station. Payment confirmation happens on a secondary device, bill printing uses the same printer as the main cashier, and the station has to sit near the packaging area because purchases still need to be bagged. Setting up a separate till felt like more work than it saved.</p>

<h2>Recommendations</h2>
<p>Was Mobile POS actually helping cashiers? In the store where it was needed, yes. In the other, the problem sat in the surrounding factors: low adoption came from store size, staffing, and physical setup rather than the quality of the tool itself. The recommendations therefore cover two areas.</p>
<h3>Process &amp; people</h3>
<ol>
<li><strong>Store prioritizing with data.</strong> Categorize stores using tills, sales area, and sales data: <em>Priority</em> (limited tills, long queues, small area), <em>Potential</em> (could benefit, needs encouragement and practice), and <em>Non-priority</em> (not in need). Effort goes where Mobile POS really solves the problem.</li>
<li><strong>Plan staff availability for peak hours.</strong> Match the number of authorized staff on peak shifts to the number of tills, plus one more if the store opens a Mobile POS till. Review shift composition ahead of peak seasons and brief the team on task splitting.</li>
<li><strong>Design the Mobile POS till area.</strong> Provide a detailed technical setup guide covering packing space, the bill printer, and the secondary device, with a flexible cashier space that fits one more person. For potential stores, simulate the layout and queue flow first.</li>
<li><strong>Practice, simulation, and checklists.</strong> Area managers run simulations per area and provide checklists for setup and ongoing use. Priority stores receive direct support; potential stores are nurtured gradually.</li>
</ol>
<h3>System &amp; UI/UX</h3>
<ol start="5">
<li><strong>Make the payment flow seamless.</strong> Ideally Mobile POS keeps customer data integrated, confirms payment automatically, and sends the bill digitally by default, with a printed copy on request. Removing the dependency on additional devices lets Mobile POS actually be mobile.</li>
</ol>

<h2>Where this stands</h2>
<div class="cs-callout"><p>These recommendations have not been put into practice yet, so no outcome can be claimed. What the study changed is how the problem is framed: <strong>a product can be well designed and still go unused when the environment does not support it.</strong> If the recommendations move forward, adoption should be tracked by store category (priority, potential, non-priority) rather than one overall number, because a low number in a non-priority store is not a failure.</p></div>
<p class="cs-src">Case study by Kinanti Ayudya Putri Rahardiani. This project is under NDA; the brand name and other sensitive information have been omitted.</p>
</article>
"""
build('mobile-pos.html', 'Mobile POS Usage Evaluation — Kinanti', body)

# ---------------------------------------------------------------- DBank Pro
body = hero(
    '#f85c36', '#ffffff', 'Redesign · UX Case Study',
    'Redesign Top Up &amp; Info Kartu Kredit DBank Pro',
    'Merancang ulang fitur Top Up dan Info Kartu Kredit pada aplikasi mobile banking DBank Pro dari Bank Danamon, agar pengalaman pengguna lebih mudah, jelas, dan praktis.',
    [('Role', 'UI/UX Designer'), ('Platform', 'Aplikasi mobile banking'),
     ('Tahun', '2022'), ('Metode', 'Design Thinking')],
    'project-dbank-pro.webp', 'Redesign DBank Pro cover')
body += """
<h2>Ringkasan</h2>
<p>DBank Pro merupakan aplikasi mobile banking dari Bank Danamon yang menawarkan kemudahan dan ragam transaksi yang dapat diakses di mana pun dan kapan pun. Permasalahan yang dirasakan pengguna terkait fitur Top Up dan Info Kartu Kredit di-redesign untuk membuat pengalaman menggunakan aplikasi DBank Pro menjadi lebih baik.</p>
<div class="cs-stats">
<div class="cs-stat"><b>8,6/10</b><span>Rata-rata nilai dari partisipan usability testing</span></div>
<div class="cs-stat"><b>3 → 1 langkah</b><span>Alur cek info kartu kredit, dari semula 3 langkah menjadi 1 langkah dari Beranda</span></div>
<div class="cs-stat"><b>5 partisipan</b><span>4 pengguna DBank Pro dan 1 bukan pengguna, semua menyelesaikan semua task</span></div>
</div>

<h2>Proses desain</h2>
<p>Redesign ini mengikuti tahapan Design Thinking: Empathize, Define, Ideate, Prototype, dan Testing.</p>
<h3>Empathize</h3>
<p>User interview dilakukan terhadap 4 pengguna DBank Pro dengan rentang usia 25–50 tahun. Pertanyaan yang diajukan meliputi kesulitan yang dirasakan pada aplikasi DBank Pro, kekurangan pada Home Page, kesulitan menggunakan fitur Top Up, kesulitan mengakses info Kartu Kredit, dan hal yang disukai dari aplikasi DBank Pro. Permasalahan yang ditemukan dirangkum sebagai pain points pengguna.</p>
<h3>Define</h3>
<p>Permasalahan dari tahap Empathize dikelompokkan ke dalam Affinity Diagram berdasarkan permasalahan fitur, kemudian dirumuskan menjadi How Might We untuk menstimulasi ideasi solusi.</p>
<h3>Ideate</h3>
<p>Dari How Might We, dibuat ide-ide solusi untuk memecahkan permasalahan pengguna sebagai dasar perancangan ulang kedua fitur.</p>
<h3>Prototype</h3>
<p>Dibuat 3 user flow: cek saldo rekening, top up, dan cek informasi kartu kredit. Pada flow Top Up yang baru, pengguna memilih rekening sumber dana, memilih jenis top up, memasukkan nomor tujuan dan nominal, lalu meninjau halaman overview sebelum memasukkan PIN. Pada flow kartu kredit yang baru, pengguna langsung memilih kartu kredit dari home page dan informasinya langsung muncul. Setelah user flow, dibuat wireframe, UI Style Guide &amp; komponen agar desain konsisten, lalu High-Fidelity design yang dijadikan prototype interaktif untuk diujikan.</p>
<h3>Testing</h3>
<p>Usability Testing dilakukan terhadap 4 partisipan pengguna DBank Pro dan 1 partisipan bukan pengguna. Enam task diberikan, mulai dari login, melakukan Top Up OVO dengan nomor baru dan menyimpannya ke favorit, melakukan top up lagi dari layar transaksi berhasil, kembali ke Beranda, hingga masuk ke halaman info kartu kredit. Hasilnya, semua partisipan dapat menyelesaikan semua task, dengan rata-rata nilai 8,6 dari 10 dan feedback yang positif.</p>

<h2>Perbandingan desain</h2>
<h3>User flow Top Up</h3>
<p>Alur top up diubah agar pengguna lebih fokus mengisi 1 sampai 2 data dalam satu langkah, sehingga risiko pengguna terlewat mengisi data menjadi lebih kecil.</p>
<h3>User flow Info Kartu Kredit</h3>
<p>Alur cek kartu kredit diubah agar pengguna lebih mudah mengakses informasinya, dari semula 3 langkah menjadi 1 langkah saja dari Beranda.</p>
<h3>Warna</h3>
<p>Warna primary aplikasi DBank Pro asli adalah kuning <strong>#FFB11B</strong>. Pada redesign, warna yang digunakan adalah orange <strong>#E94E15</strong>, diambil dari warna logo Bank Danamon yang memiliki 3 shade orange. Dari ketiganya dipilih yang memiliki contrast score lebih tinggi, karena contrast score berpengaruh pada kejelasan tulisan terhadap background.</p>
<h3>Login</h3>
<p>Halaman login aplikasi asli terkesan berantakan. Pada redesign, halaman login dirapikan agar lebih enak dilihat dan informasi yang ingin ditampilkan menjadi lebih jelas.</p>

<h2>Kesimpulan</h2>
<p>Bagi pengguna, kemudahan, kejelasan, dan kepraktisan sebuah aplikasi merupakan nilai yang banyak dicari. Karena itu desain yang dibuat sebaiknya dapat memberikan kemudahan, kejelasan, dan kepraktisan kepada pengguna, seperti yang tercermin dari nilai rata-rata 8,6 dari 10 dengan feedback positif pada redesign ini.</p>
<p class="cs-src">Case study oleh Kinanti Ayudya Putri Rahardiani · 2022</p>
</article>
"""
build('dbank-pro.html', 'Redesign DBank Pro — Kinanti', body)

# ---------------------------------------------------------------- UpCademy
body = hero(
    '#fe7fc4', '#363636', 'UX Case Study',
    'UpCademy Online Education Platform',
    'Mendesain platform edukasi online yang mudah dipahami, dari flow pendaftaran &amp; login, transaksi kelas, sampai proses pembelajaran.',
    [('Role', 'UI/UX Designer'), ('Tim', 'Bersama Febrianasp &amp; Firratus Saadah'),
     ('Tahun', '2021'), ('Metode', 'Design Thinking')],
    'project-upcademy.webp', 'UpCademy cover')
body += """
<h2>Latar belakang &amp; objektif</h2>
<p>UpCademy adalah online education platform yang dapat digunakan sebagai sarana untuk belajar dengan mudah dari mana saja. Sebagai aplikasi belajar online, fitur yang sering digunakan user adalah pendaftaran &amp; login, transaksi kelas atau proses pembelian, dan proses pembelajaran. Objektif proyek ini:</p>
<ol>
<li>Mendesain platform edukasi online yang mudah dipahami oleh user.</li>
<li>Mendesain flow dan tampilan pendaftaran &amp; login.</li>
<li>Mendesain flow dan tampilan transaksi kelas.</li>
<li>Mendesain flow dan tampilan proses pembelajaran.</li>
</ol>
<p>Tantangannya adalah membuat aplikasi yang user friendly, membuat user merasa nyaman menggunakannya, dan memberikan informasi yang cukup agar user tidak bingung.</p>

<h2>1 · Empathize</h2>
<p>Target user adalah pengguna berusia 18–50 tahun, mahasiswa atau karyawan, berdomisili di seluruh Indonesia, dengan Bahasa Indonesia sebagai native language. Permasalahan yang muncul antara lain user tidak senang dengan tampilan, platform rumit digunakan, loading yang sangat lama, dan susah mencari motivasi untuk belajar. Dari sini, tim ingin membuat platform yang user friendly dengan tampilan menarik dan dapat meningkatkan motivasi belajar.</p>

<h2>2 · Define</h2>
<p>Dari permasalahan yang ditemukan, dipilih 5 pain points paling krusial:</p>
<ol>
<li>Harga kelas kurang terjangkau.</li>
<li>Bahasa yang digunakan dalam pembelajaran sulit dimengerti.</li>
<li>Kurangnya informasi tentang kelas.</li>
<li>Membutuhkan kuota lebih dalam transaksi.</li>
<li>Tidak semua orang bisa membayar transaksi secara online.</li>
</ol>
<p>Kemudian dibuat 3 How Might We: membuat kelas yang lebih terjangkau, membuat user mengerti bahasa yang sulit digunakan, dan memberikan user informasi yang jelas tentang kelas.</p>

<h2>3 · Ideate</h2>
<p>Dari How Might We dibuat ide solusi, lalu dilakukan voting hingga didapat top 3 solutions:</p>
<ol>
<li>Memberikan promo lisensi 1 kali bayar untuk akses semua kelas.</li>
<li>Memberikan deskripsi mengenai materi yang akan dibahas.</li>
<li>Membuat glosarium/kamus bahasa yang tidak umum digunakan.</li>
</ol>
<p>Berdasarkan Prioritization Idea (dampak terhadap user dibanding usaha pembuatannya), yang dikerjakan sekarang adalah deskripsi materi dan glosarium, sedangkan promo 1 kali bayar dilakukan nanti. Setelah itu tim melakukan Crazy 8 untuk masing-masing fitur, membuat 3 user flow (login &amp; pendaftaran, transaksi, proses pembelajaran), wireframe, dan UI Design.</p>

<h2>4 · Prototype</h2>
<p>UI Design yang selesai dibuat menjadi prototype interaktif yang terdiri dari 3 alur: pendaftaran &amp; login, transaksi, dan proses pembelajaran. Prototype inilah yang diujikan ke user pada tahap Testing.</p>

<h2>5 · Testing</h2>
<p>Testing dilakukan dengan In-Depth Interview dan Usability Testing. User mencoba prototype, lalu memberikan penilaian untuk setiap flow dengan skala Likert dan penilaian flow keseluruhan dengan Single Ease Question (SEQ).</p>
<div class="cs-stats">
<div class="cs-stat"><b>6,5/7</b><span>Single Ease Question untuk flow keseluruhan</span></div>
<div class="cs-stat"><b>6,5/7</b><span>Skala Likert flow pendaftaran &amp; login</span></div>
<div class="cs-stat"><b>6,3/7</b><span>Skala Likert flow transaksi</span></div>
<div class="cs-stat"><b>6,5/7</b><span>Skala Likert flow proses pembelajaran</span></div>
</div>
<p>Dengan nilai SEQ 6,5, desain yang dibuat sudah cukup memenuhi kebutuhan user, karena nilai minimal yang dibutuhkan adalah 5,5.</p>

<h2>Kesimpulan</h2>
<p>Walaupun sudah cukup memenuhi kebutuhan user, prototype ini masih memiliki banyak kekurangan. Testing yang dilakukan juga masih kurang objektif karena hanya melibatkan 1 orang responden, sehingga baru melihat dari satu sudut pandang user saja. Langkah selanjutnya adalah melakukan interview dengan beberapa responden lain untuk melihat sudut pandang yang berbeda dan mendapatkan feedback untuk iterasi desain berikutnya. Case study ini adalah UX Case Study pertama penulis.</p>
<p class="cs-src">Case study oleh Kinanti Ayudya Putri Rahardiani · 2021</p>
</article>
"""
build('upcademy.html', 'UpCademy — Kinanti', body)

# ---------------------------------------------------------------- Waste4Change
body = hero(
    '#e8ee58', '#363636', 'UX Case Study · Redesign',
    'Send Your Waste — Waste4Change',
    'Merancang ulang layanan Send Your Waste di website Waste4Change, agar alur mengirim sampah anorganik menjadi jelas, dari form, pembayaran, sampai redeem points.',
    [('Role', 'UI/UX Designer'), ('Tim', 'Tim 3 orang, bersama Firratus Saadah &amp; Febrianasp'),
     ('Platform', 'Website, desktop &amp; mobile'), ('Konteks', 'Program Skilvul × Kampus Merdeka, Waste4Change sebagai Challenge Partner')],
    'project-waste4change.webp', 'Waste4Change Send Your Waste cover')
body += """
<h2>Latar belakang</h2>
<p>Waste4Change adalah perusahaan yang menyediakan solusi untuk mengelola sampah anorganik di Indonesia, dengan layanan untuk perusahaan maupun individu. Case study ini fokus pada layanan untuk individu, yaitu Send Your Waste. Proyek ini adalah bagian dari program pelatihan UI/UX Skilvul untuk Kampus Merdeka; penulis tidak bekerja untuk atau terikat kontrak profesional dengan Waste4Change.</p>
<h3>Masalah</h3>
<ol>
<li>Alur aplikasi yang membingungkan pengguna.</li>
<li>Tampilan website yang sulit dipahami.</li>
<li>Kurangnya penjelasan terkait layanan yang tersedia.</li>
</ol>
<h3>Goals</h3>
<ol>
<li>Membuat sasaran utama pengguna, yaitu ibu rumah tangga dan pengguna umum, dapat dengan mudah mengoperasikan website Waste4Change.</li>
<li>Memperluas cakupan pengguna layanan Waste4Change.</li>
</ol>

<h2>1 · Empathize</h2>
<p>Target user berusia 20–35 tahun, merupakan mahasiswa, karyawan, dan/atau ibu rumah tangga, dengan ekonomi menengah ke atas, dan kebanyakan perempuan. Research dilakukan dari permasalahan yang disampaikan pihak Waste4Change, feedback user dari rating aplikasi serupa, dan diskusi kelompok berdasarkan percobaan menggunakan fitur Send Your Waste.</p>

<h2>2 · Define</h2>
<p>Dari research ditentukan 4 permasalahan paling krusial:</p>
<ol>
<li>Fitur yang disediakan tidak jelas.</li>
<li>Halaman points dan redeem points tidak jelas.</li>
<li>Alur transaksi yang membingungkan.</li>
<li>Pembayaran tidak dapat dilakukan di dalam website.</li>
</ol>
<p>Keempatnya dirumuskan menjadi How Might We: membuat fitur lebih jelas dan mudah dicari di Landing Page, membuat halaman point reward dan redeem point lebih jelas, membuat alur form transaksi mudah dipahami dan informatif, dan membuat pembayaran dapat dilakukan di dalam website agar lebih efisien.</p>

<h2>3 · Ideate</h2>
<p>Ide solusi dibuat dari setiap How Might We, dikelompokkan dengan Affinity Diagram, lalu diprioritaskan:</p>
<div class="cs-cards">
<div class="cs-card"><h3>Do Now</h3><p>Form, Payments, dan Point Reward.</p></div>
<div class="cs-card"><h3>Do Next</h3><p>Landing Page.</p></div>
</div>
<p>Tim kemudian melakukan Crazy 8s untuk masing-masing fitur dalam 2 versi, desktop dan mobile, dan membuat 4 user flow:</p>
<ol>
<li><strong>Login</strong>, bagaimana user masuk sebelum mengirim sampah.</li>
<li><strong>Send Trash &amp; Payment</strong>, pengisian data pengiriman dan pembayaran, dibuat untuk program reguler dan program points (pada program points, user memilih program terlebih dahulu sebelum mengisi form).</li>
<li><strong>Tracking Paket / Driver</strong>, melihat progress paket, dengan pop up jumlah points pada program points.</li>
<li><strong>Redeem Points</strong>, menukar points yang didapatkan.</li>
</ol>

<h2>4 · Prototype</h2>
<p>Wireframe dibuat terlebih dahulu menggunakan Figma untuk tampilan desktop dan mobile, dengan mengadopsi desain Waste4Change agar tema perusahaan tetap terjaga, ditambah referensi dari website sejenis. Setelah wireframe, dibuat UI Design dengan beberapa perubahan berdasarkan kegunaan dan kemudahan pengguna. Halaman yang dirancang ulang meliputi Halaman Login, Landing Page, Form Send Your Waste, Halaman Redeem Points, dan Halaman Points, lalu dibuat menjadi interactive prototype untuk desktop dan mobile.</p>

<h2>5 · Testing</h2>
<p>Testing dilakukan dengan In-Depth Interview dan Usability Testing terhadap 3 user yang memenuhi kriteria target user. User mencoba prototype dan memberikan penilaian untuk setiap flow dengan skala Likert, serta penilaian keseluruhan dengan Single Ease Question. Berdasarkan penilaian user, desain yang dibuat sudah cukup memenuhi kebutuhan user dan cukup mudah dimengerti dan digunakan. Tim juga sudah melakukan perbaikan desain berdasarkan hasil interview.</p>

<h2>Kesimpulan</h2>
<p>Dari seluruh proses, tim belajar banyak mengenai UI Design maupun teamwork. Prototype redesign Send Your Waste ini masih memiliki kekurangan dan banyak hal yang harus ditingkatkan, dan akan menjadi pelajaran untuk membuat case study dan desain yang lebih baik ke depannya, termasuk melakukan iterasi desain berikutnya.</p>
<p class="cs-src">Case study oleh Kinanti Ayudya Putri Rahardiani · 2021</p>
</article>
"""
build('waste4change.html', 'Waste4Change — Kinanti', body)

# ---------------------------------------------------------------- Niagahoster
body = hero(
    '#2185e3', '#ffffff', 'Redesign · UI Design',
    'Redesign Niagahoster Checkout Page',
    'Merancang ulang halaman checkout Niagahoster agar user tidak lagi bingung memilih paket hosting, dan dapat memutuskan pilihan dengan lebih cepat.',
    [('Role', 'UI/UX Designer'), ('Deliverable', 'Halaman checkout: paket, durasi, domain, estimasi harga'),
     ('Testing', 'Unmoderated usability testing, 2 partisipan'), ('Hasil', 'Nilai rata-rata 8,5 dari 10')],
    'project-niagahoster.webp', 'Redesign Niagahoster Checkout cover')
body += """
<h2>Latar belakang</h2>
<p>Niagahoster memiliki target yang belum tercapai untuk jumlah pembeli layanan hosting. Hasil riset menyatakan bahwa ada beberapa pengguna yang kebingungan saat memilih opsi layanan di halaman checkout, dan membutuhkan waktu yang lama untuk memutuskan pilihan mereka. Akar permasalahannya adalah pengguna dihadapkan dengan terlalu banyak pilihan dan tidak memahami definisi dari setiap pilihan yang ditawarkan. Tugas pada proyek ini adalah membantu meningkatkan persentase pengguna yang menyelesaikan pembelian layanan hosting di halaman checkout.</p>
<h3>Problem</h3>
<ul>
<li>Pengguna kebingungan saat memilih opsi layanan di halaman checkout.</li>
<li>Pengguna membutuhkan waktu yang lama untuk memutuskan pilihan.</li>
<li>Pengguna dihadapkan dengan terlalu banyak pilihan dan tidak memahami definisi tiap pilihan.</li>
</ul>
<h3>How Might We</h3>
<ul>
<li>How might we membuat user tidak bingung saat memilih opsi layanan?</li>
<li>How might we mempercepat user memutuskan pilihan?</li>
<li>How might we membuat user mengerti tentang pilihan yang ditawarkan?</li>
</ul>

<h2>Ideate</h2>
<p>Sebelum ideasi, dilakukan pengamatan terhadap produk web hosting kompetitor. Temuannya: kebanyakan kompetitor menampilkan jenis paket hosting dalam satu baris tanpa scroller atau penanda halaman, agar user langsung melihat semua paket tanpa terlewat. Kompetitor juga memberi tanda pada paket yang lebih menguntungkan user, sehingga user lebih cepat memilih karena sudah ada rekomendasi. Untuk detail paket, kompetitor menuliskan poin-poin kelebihan tiap paket, termasuk menginformasikan fasilitas yang tidak didapatkan pada paket yang lebih murah.</p>
<p>Solusi yang dirancang untuk menjawab How Might We:</p>
<ol>
<li>Menampilkan semua paket dalam satu baris.</li>
<li>Memberikan tanda rekomendasi untuk paket dan durasi yang paling menguntungkan.</li>
<li>Menginformasikan fasilitas yang akan didapat user pada tiap paket.</li>
</ol>
<p>Wireframe halaman checkout disusun dari elemen: Logo, Jenis-jenis paket, Durasi paket, Input domain, Estimasi harga, dan Button Lanjut.</p>

<h2>UI Design</h2>
<h3>Pilih Paket Hosting</h3>
<div class="cs-pkgs">
<div class="cs-pkg"><h3>Bayi</h3><ul><li>Tanpa gratis domain</li><li>15.000 pengunjung/bulan</li><li>500 MB SSD disk space</li><li>Unlimited bandwidth &amp; database</li><li>1 email account</li><li>1 domain</li><li>Gratis sertifikat SSL</li><li>SpamExperts mail protection</li></ul></div>
<div class="cs-pkg"><h3>Pelajar</h3><ul><li>Free domain 1 tahun</li><li>60.000 pengunjung/bulan</li><li>Unlimited SSD disk space</li><li>Unlimited bandwidth &amp; database</li><li>Unlimited email account</li><li>10 addon domain</li><li>Gratis sertifikat SSL</li><li>SpamExperts mail protection</li></ul></div>
<div class="cs-pkg"><h3>Personal</h3><span class="tag">Paling Laris!</span><ul><li>Free domain 1 tahun</li><li>135.000 pengunjung/bulan</li><li>Unlimited SSD disk space</li><li>Unlimited bandwidth &amp; database</li><li>Unlimited email account</li><li>Unlimited addon domain</li><li>Gratis sertifikat SSL</li><li>SpamExperts mail protection</li></ul></div>
<div class="cs-pkg"><h3>Bisnis</h3><ul><li>Free domain 1 tahun</li><li>180.000 pengunjung/bulan</li><li>Unlimited SSD disk space</li><li>Unlimited bandwidth &amp; database</li><li>Unlimited email account</li><li>Unlimited addon domain</li><li>Gratis sertifikat SSL</li><li>SpamExperts mail protection</li></ul></div>
</div>
<h3>Pilih Durasi Paket</h3>
<div class="cs-cards">
<div class="cs-card"><h3>1 Bulan</h3><p>Rp 129.900,00/bln. Total Rp 129.900,00.</p></div>
<div class="cs-card"><h3>1 Tahun · −68%</h3><p>Rp 34.900,00/bln. Total dari Rp 1.318.800,00 menjadi <strong>Rp 418.800,00</strong>.</p></div>
<div class="cs-card"><h3>3 Tahun · −75%</h3><p><strong>Paling Hemat!</strong> Rp 24.900,00/bln. Total dari Rp 3.596.400,00 menjadi <strong>Rp 896.400,00</strong>.</p></div>
</div>
<h3>Domain</h3>
<p>Tersedia tab "Domain Baru" dengan label "Gratis!" dan tab "Saya Sudah Punya Domain", kolom input nama domain, dan tombol "Cek Domain". Domain gratis yang tersedia antara lain .com, .net, .org, .info, .sch.id, .or.id, .ac.id, .web.id, .xyz, .website, .space, .site, .online, dan .ponpes.id.</p>
<h3>Estimasi Harga</h3>
<p>Ringkasan total harga ditampilkan di bagian estimasi, pada contoh sebesar <strong>Rp 896.400,00</strong>, dengan tombol "Lanjutkan" untuk menyelesaikan pembelian.</p>

<h2>Usability Testing</h2>
<p>Testing dilakukan dengan metode unmoderated: partisipan diberikan desain untuk dieksplorasi sendiri, lalu menjawab 8 pertanyaan, mulai dari apakah perbedaan tiap paket dapat dimengerti, kejelasan informasi paket dan durasi, kemudahan memutuskan, hal yang disukai dan tidak disukai, feedback, hingga nilai skala 1–10. Kriteria partisipan adalah mengerti tentang web hosting dan pernah menggunakan layanan web hosting.</p>
<div class="cs-stats">
<div class="cs-stat"><b>8</b><span>Nilai Partisipan 1, usia 23 tahun</span></div>
<div class="cs-stat"><b>9</b><span>Nilai Partisipan 2, usia 21 tahun</span></div>
<div class="cs-stat"><b>8,5</b><span>Rata-rata nilai dari kedua partisipan</span></div>
</div>
<p>Kedua partisipan menyatakan mengerti perbedaan tiap paket, informasi paket dan durasi cukup jelas, dan mudah memutuskan paket serta durasi yang diambil. Hal yang disukai antara lain bagian domain yang eye catching dan tampilan yang minimalis namun seluruh informasi tersampaikan dengan jelas. Kesimpulannya, desain yang dibuat sudah cukup memudahkan user untuk memilih paket yang ditawarkan.</p>

<h2>UI Kit</h2>
<p>Sebelum membuat UI Design, dibuat UI Kit sebagai panduan agar desain konsisten. UI Kit adalah versi sederhana dari Design System yang dapat digunakan pada desain skala kecil. Color palette yang digunakan adalah color palette yang memang sudah digunakan oleh Niagahoster, agar desain memiliki warna dan vibe yang konsisten.</p>
<div class="cs-swatches">
<div class="cs-sw"><i style="background:#007AFF"></i><span><b>Primary Blue</b>#007AFF</span></div>
<div class="cs-sw"><i style="background:#F0F8FF"></i><span><b>Background Blue</b>#F0F8FF</span></div>
<div class="cs-sw"><i style="background:#29384E"></i><span><b>Text</b>#29384E</span></div>
<div class="cs-sw"><i style="background:#FF9800"></i><span><b>Accent Orange</b>#FF9800</span></div>
<div class="cs-sw"><i style="background:#00BFA6"></i><span><b>Success Green</b>#00BFA6</span></div>
<div class="cs-sw"><i style="background:#F43636"></i><span><b>Danger Red</b>#F43636</span></div>
</div>
<p>Tipografi menggunakan font Inter: Heading Inter Medium 32, Title Inter Medium 24, Button Inter Bold 20, Body Inter Regular 16, dan Caption Inter Regular 14. Komponen pada UI Kit meliputi logo Niagahoster, kartu paket, kartu durasi, serta tombol "Lanjutkan" varian primer dan outline. UI Design akhir kemudian dibuat menggunakan komponen-komponen dari UI Kit ini.</p>
<p class="cs-src">Case study oleh Kinanti Ayudya Putri Rahardiani</p>
</article>
"""
build('niagahoster.html', 'Redesign Niagahoster Checkout — Kinanti', body)

# ---------------------------------------------------------------- Warunk Upnormal
body = hero(
    '#f8bbdc', '#363636', 'Case Study · Research &amp; Strategy',
    'Warunk Upnormal',
    'Reclaiming market interest in Warunk Upnormal, a youth hangout cafe whose outlets were closing, and making customers keep coming back.',
    [('Role', 'UI/UX Designer'), ('Methods', 'Design Thinking · Desk research · In-depth interviews'),
     ('Participants', '4 interviewees, aged 20–24'), ('Focus', 'Customer return &amp; brand experience')],
    'project-warunk-upnormal.webp', 'Warunk Upnormal cover')
body += """
<h2>About</h2>
<p>Warunk Upnormal is a cafe founded in 2014, themed as a place for young people to hang out, with a menu of various Indomie modifications, toast, milk, and coffee. In 2019, there were 85 Warunk Upnormal outlets spread across various regions.</p>
<h2>Context &amp; objective</h2>
<p>Many Warunk Upnormal outlets have closed, and market interest in Upnormal is decreasing. The objective of this case study: <strong>reclaiming market interest in Upnormal, and making customers keep coming back.</strong></p>

<h2>Desk research</h2>
<ul>
<li>Upnormal targets the youth market segment aged 15–25 years (beritasatu, 2023).</li>
<li>During the Covid-19 pandemic, Warunk Upnormal's sales decreased by up to <strong>40%</strong> (bisnis.com, 2023), and many outlets were closed.</li>
<li>To adapt to post-covid consumer habits, Upnormal implemented the Pay at Table feature in the Upnormal App, and provided promos for delivery purchases via GrabFood &amp; GoFood.</li>
<li>Some outlets were renamed Upnormal Coffee &amp; Roaster with the same menu, and a self-service Indomie cooking concept is planned.</li>
</ul>

<h2>Interviews</h2>
<p>In-depth online interviews were conducted with 4 participants, men and women aged 20–24 who had been to an Upnormal outlet. They were asked whether they ever came back and why, what they like about Upnormal, what would attract them again, where they look for restaurant information, and in their opinion why Upnormal went quiet and what would make it crowded again.</p>
<div class="cs-stats">
<div class="cs-stat"><b>3 of 4</b><span>Participants never came back after trying Upnormal once</span></div>
<div class="cs-stat"><b>−40%</b><span>Sales decrease during the Covid-19 pandemic</span></div>
<div class="cs-stat"><b>85</b><span>Outlets across various regions in 2019</span></div>
</div>
<h3>Why they did not return</h3>
<ul>
<li>2 participants said the food is very ordinary, nothing special.</li>
<li>The food is overpriced, just Indomie, and quite expensive for what it is.</li>
</ul>
<h3>What could bring them back</h3>
<ul>
<li>2 participants said an event by their favorite artist.</li>
<li>Promos, and new menu items.</li>
</ul>
<h3>What they like, and how they search</h3>
<ul>
<li>3 participants said the place is nice, and there is a playzone (UNO, UNO Stacko).</li>
<li>Restaurant information is mostly looked up on Instagram, Google, and Google Maps; 3 of 4 rarely open a restaurant's website.</li>
<li>Everyone looks for the menu &amp; price list; some also look for reservation contacts, outlet galleries, and locations.</li>
</ul>
<h3>Why Upnormal went quiet, in their words</h3>
<ul>
<li>2 participants said Upnormal is outdated and does not keep up with trends, only hype at the beginning.</li>
<li>Menus are overpriced, inferior to other restaurants in a lower price range.</li>
<li>It could be crowded again if the food tastes better, the name changes, and there are more games and more menu variety, especially sharing menus.</li>
</ul>

<h2>Research summary</h2>
<p>The main problems: <strong>the food tastes very ordinary; Upnormal is outdated, not keeping up with trends, with nothing special about it; and the menus are overpriced, not worth it.</strong> The opportunity: Upnormal will make self-service Indomie cooking.</p>
<h3>Persona</h3>
<p><strong>Upi</strong>, 21–23 years old, a college student and employee. Upi wants a place with good food and a good atmosphere at a reasonable price, a trendy and fun hangout. Upi thinks Upnormal's menu is not worth the price and tastes average, with nothing special about it. Upi likes promos, wants to try attractive new menus, and wants to attend events with their favorite artist.</p>
<h3>How Might We</h3>
<ul>
<li>How might we make customers think the price is worth it?</li>
<li>How might we make the food tasty?</li>
<li>How might we make Upnormal special?</li>
</ul>
<p>The prioritized How Might We is the first one: most participants do not come back because they think the price is not worth it, and most stated there is nothing special about Upnormal. Competitor analysis was benchmarked mainly against Mie Gacoan, the competitor participants compared Upnormal with that shares the same spread, form, menu, and price; competitors offer a cheaper price range and websites with more of the information customers usually search for.</p>

<h2>The solutions</h2>
<div class="cs-cards">
<div class="cs-card"><h3>1 · Reward for Feedback</h3><p>A feedback survey customers can access with their Receipt ID, so only customers who really experienced Upnormal can fill it in. The survey has 3 parts: scalable questions, options, and free text. After completing it, the customer reaches a reward page, and the voucher is sent to the email filled in on the first page.</p></div>
<div class="cs-card"><h3>2 · General suggestions</h3><p><strong>Seasonal menu</strong>, so Upnormal always has something new that attracts customers to try again. <strong>Events</strong> in collaboration with famous artists, such as live music performances or meet &amp; greet, with a minimum purchase to enter.</p></div>
<div class="cs-card"><h3>3 · Self-service components</h3><p>Making the self-service Indomie experience uniquely Upnormal: its own special sauce recipe, various free and paid toppings, complete Indomie variants including rare and premium ones, an automatic ramen machine, and tips &amp; tricks cooking videos playing on TV while customers queue.</p></div>
</div>

<h2>Conclusion</h2>
<p>Most participants do not want to go back to Upnormal after trying it once. To make them keep coming back, the solutions are built on what attracts them: something special about Upnormal, and a service that feels worth it. Reward for Feedback keeps customers coming back and spending to redeem the reward; new menus and events keep them attracted to something new; and the uniqueness of self-service gives them a reason to return. The next steps are usability testing, to check whether the suggested solutions actually attract customers, and iteration.</p>
<div class="cs-callout"><p><strong>Key learnings.</strong> It doesn't have to be a UI screen. And breaking down interview results more carefully reveals opportunities that a surface reading misses. There is still a lot lacking in this case study, especially in research and problem defining, and that is exactly what I want to learn deeper.</p></div>
<p class="cs-src">Case study by Kinanti Ayudya Putri Rahardiani</p>
</article>
"""
build('warunk-upnormal.html', 'Warunk Upnormal — Kinanti', body)
print('DONE')
