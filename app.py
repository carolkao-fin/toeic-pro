"""
TOEIC Pro 850+ — Streamlit 版
根據多益學習平台開發紀錄重建 + 每日打卡 + 小遊戲
"""
import random
import time
import json
import calendar as cal_mod
from datetime import date, timedelta
from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="TOEIC Pro 850+",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─────────────────────────────────────────────────────────────────────────────
# CSS
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
:root {
  --pr:#2563eb;--gr:#10b981;--yl:#f59e0b;
  --rd:#ef4444;--bg:#f1f5f9;--tx:#1e293b;--mu:#64748b;
  --purple:#7c3aed;
}
#MainMenu,footer,header{visibility:hidden}
.stTabs [data-baseweb="tab-list"]{gap:4px;flex-wrap:wrap}
.stTabs [data-baseweb="tab"]{border-radius:8px 8px 0 0;padding:8px 16px;font-weight:600}
.tcard{background:white;border-radius:14px;padding:1.4rem 1.6rem;margin-bottom:1rem;
  box-shadow:0 1px 3px rgba(0,0,0,.08);border:1px solid #e2e8f0}
.stat-grid{display:flex;gap:12px;flex-wrap:wrap;margin-bottom:1rem}
.stat-box{background:white;border-radius:12px;padding:1rem 1.4rem;
  border:1px solid #e2e8f0;flex:1;min-width:120px;text-align:center;
  box-shadow:0 1px 3px rgba(0,0,0,.06)}
.stat-num{font-size:2rem;font-weight:800;color:var(--pr);line-height:1}
.stat-lbl{font-size:.75rem;color:var(--mu);margin-top:4px}
.flashcard{background:linear-gradient(135deg,#2563eb,#1d4ed8);color:white;border-radius:18px;
  padding:2.5rem 2rem;text-align:center;min-height:180px;display:flex;flex-direction:column;
  align-items:center;justify-content:center;cursor:pointer;margin-bottom:1rem;
  box-shadow:0 8px 24px rgba(37,99,235,.25)}
.fc-word{font-size:2.2rem;font-weight:800;letter-spacing:.04em}
.fc-pos{font-size:.85rem;opacity:.75;margin-top:.3rem}
.fc-zh{font-size:1.5rem;font-weight:700;margin-bottom:.5rem}
.fc-ex{font-size:.85rem;opacity:.85;line-height:1.5}
.pb-wrap{background:#e2e8f0;border-radius:99px;height:8px;overflow:hidden;margin:.5rem 0}
.pb{height:100%;border-radius:99px;background:linear-gradient(90deg,#2563eb,#7c3aed);transition:width .4s}
.fb-ok{background:#ecfdf5;border:1px solid #10b981;border-radius:10px;padding:.8rem 1rem;color:#065f46;margin-top:.5rem}
.fb-bad{background:#fef2f2;border:1px solid #ef4444;border-radius:10px;padding:.8rem 1rem;color:#991b1b;margin-top:.5rem}
.tag{display:inline-block;padding:.15rem .55rem;border-radius:6px;font-size:.72rem;font-weight:700;margin-right:.3rem}
.tag-n{background:#dbeafe;color:#1e40af}
.tag-v{background:#dcfce7;color:#166534}
.tag-adj{background:#fef9c3;color:#854d0e}
.tag-adv{background:#f3e8ff;color:#6b21a8}
.timer-box{text-align:center;font-size:2rem;font-weight:800;color:var(--pr);margin-bottom:.5rem}
.timer-warn{color:var(--yl)!important}
.timer-danger{color:var(--rd)!important}
.hero{background:linear-gradient(135deg,#2563eb,#7c3aed);color:white;border-radius:16px;
  padding:1.8rem 2rem;margin-bottom:1.5rem}
.hero h1{color:white;margin:0;font-size:1.8rem;font-weight:800}
.hero p{color:rgba(255,255,255,.85);margin:.3rem 0 0}
.wl-row{display:flex;align-items:center;gap:.8rem;padding:.6rem .8rem;border-radius:8px;
  border-bottom:1px solid #f1f5f9}
.wl-word{font-weight:700;min-width:130px}
.wl-zh{color:var(--mu);flex:1}
.wl-ex{font-size:.78rem;color:#94a3b8;flex:2}
/* 打卡 */
.streak-banner{background:linear-gradient(135deg,#7c3aed,#2563eb);color:white;
  border-radius:16px;padding:1.6rem 2rem;margin-bottom:1rem;
  display:flex;align-items:center;gap:1.5rem}
.streak-num{font-size:3rem;font-weight:900;line-height:1}
.streak-label{font-size:.9rem;opacity:.85}
.badge-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(110px,1fr));gap:10px}
.badge-item{background:white;border:1px solid #e2e8f0;border-radius:12px;
  padding:14px 10px;text-align:center;transition:all .2s}
.badge-unlocked{border-color:#f59e0b;background:linear-gradient(135deg,#fffbeb,#fef3c7)}
.badge-locked{opacity:.4;filter:grayscale(.8)}
.badge-icon{font-size:1.8rem;margin-bottom:4px}
.badge-name{font-size:.75rem;font-weight:700;color:#1e293b}
.badge-req{font-size:.65rem;color:#64748b;margin-top:2px}
/* 遊戲 */
.game-pick-card{background:white;border:2px solid #e2e8f0;border-radius:16px;
  padding:1.6rem;text-align:center;cursor:pointer;transition:all .2s;
  box-shadow:0 1px 3px rgba(0,0,0,.06)}
.game-pick-card:hover{border-color:var(--purple);transform:translateY(-2px)}
.game-icon{font-size:2.5rem;margin-bottom:.6rem}
.mc-card-matched{background:#ecfdf5;border:2px solid #10b981;border-radius:10px;
  padding:.7rem;text-align:center;color:#065f46;font-weight:700;font-size:.85rem}
.mc-card-selected{background:#ede9fe;border:2px solid #7c3aed;border-radius:10px;
  padding:.7rem;text-align:center;color:#5b21b6;font-weight:700;font-size:.85rem}
.xp-pill{display:inline-block;background:linear-gradient(135deg,#f59e0b,#d97706);
  color:white;border-radius:99px;padding:.3rem 1rem;font-weight:700;font-size:.85rem}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# 資料層
# 詞彙來源：kknono668/toeic-vocab-tw (Hugging Face, CC-BY-SA-4.0)
# https://huggingface.co/datasets/kknono668/toeic-vocab-tw
# ─────────────────────────────────────────────────────────────────────────────
def _load_vocab() -> list:
    vocab_file = Path(__file__).parent / "vocab_data.json"
    if not vocab_file.exists():
        return []
    raw = json.loads(vocab_file.read_text(encoding="utf-8"))
    pos_map = {
        "verb": "v.", "noun": "n.", "adjective": "adj.", "adverb": "adv.",
        "preposition": "prep.", "conjunction": "conj.", "determiner": "n.",
        "pronoun": "n.", "interjection": "n.", "phrase": "n.",
    }
    result, seen = [], set()
    for r in raw:
        word = r.get("word", "").strip()
        zh = r.get("zh", "").strip()
        ex = r.get("ex", "").strip()
        if not word or not zh or not ex:
            continue
        # 過濾含空格的多字片語與過長單字
        if " " in word or len(word) > 25:
            continue
        if word.lower() in seen:
            continue
        seen.add(word.lower())
        pos_raw = r.get("pos", "noun").split(",")[0].strip().lower()
        pos = pos_map.get(pos_raw, "n.")
        result.append({
            "word": word,
            "pos": pos,
            "cat": r.get("cat", "商務辦公"),
            "zh": zh,
            "ex": ex,
            "range": r.get("range", "600-780"),
        })
    return result

VOCAB = _load_vocab()

GRAMMAR_QS = [
    {"q":"The report will be submitted _____ Friday.","opts":["on","at","in","by"],"ans":3,"exp":'"By Friday" 表示截止時間，用 by'},
    {"q":"She is responsible _____ managing the budget.","opts":["of","for","to","with"],"ans":1,"exp":'"Responsible for" 是固定搭配'},
    {"q":"The meeting has been _____ until next Monday.","opts":["postponed","cancelled","started","finished"],"ans":0,"exp":'"Postponed until" = 延後到某時間'},
    {"q":"Please _____ the form completely before submitting.","opts":["fill out","fill in","fill up","fill over"],"ans":0,"exp":'"Fill out a form" 填寫表格，美式常用'},
    {"q":"The new policy will _____ effect from January.","opts":["take","do","make","get"],"ans":0,"exp":'"Take effect" = 生效，固定搭配'},
    {"q":"All employees are required to _____ the training.","opts":["attend","join to","participate","enter"],"ans":0,"exp":'"Attend" 不需介系詞'},
    {"q":"The product is currently _____ of stock.","opts":["out","away","off","short"],"ans":0,"exp":'"Out of stock" = 缺貨'},
    {"q":"The contract was signed _____ both parties.","opts":["by","of","from","with"],"ans":0,"exp":"被動語態行為者用 by"},
    {"q":"We need to _____ a decision by end of day.","opts":["make","do","take","have"],"ans":0,"exp":'"Make a decision" 固定搭配'},
    {"q":"The budget _____ approved last week.","opts":["was","were","be","is"],"ans":0,"exp":"過去式被動：was + p.p."},
    {"q":"Sales have increased _____ 20% compared to last year.","opts":["by","at","in","for"],"ans":0,"exp":"增加了百分比用 by"},
    {"q":"The manager asked the team _____ overtime this week.","opts":["to work","working","work","worked"],"ans":0,"exp":"ask sb. to-v 固定結構"},
    {"q":"_____ the bad weather, the outdoor event was cancelled.","opts":["Due to","Because","Since","Despite"],"ans":0,"exp":'"Due to" 後接名詞片語'},
    {"q":"The office will be _____ for renovation next week.","opts":["closed","closing","close","closes"],"ans":0,"exp":"be + p.p. 被動語態"},
    {"q":"She has worked here _____ five years.","opts":["for","since","during","from"],"ans":0,"exp":'"For" 接時間長度'},
    {"q":"The new employee _____ to the team yesterday.","opts":["was introduced","introduced","is introduced","has introduced"],"ans":0,"exp":"過去被動：was + p.p."},
    {"q":"He will notify you _____ soon as the package arrives.","opts":["as","so","very","that"],"ans":0,"exp":'"As soon as" = 一…就…'},
    {"q":"The figures in this report are not _____.","opts":["accurate","accuracy","accurately","accurateness"],"ans":0,"exp":"be 動詞後接形容詞"},
    {"q":"Please submit your application _____ the deadline.","opts":["before","until","during","while"],"ans":0,"exp":'"Before the deadline" = 在截止日前'},
    {"q":"The company's profits _____ steadily over the past year.","opts":["have grown","grew","are growing","had grown"],"ans":0,"exp":"現在完成式：持續到現在的結果"},
    {"q":"_____ completing the training, employees receive a certificate.","opts":["Upon","For","By","After"],"ans":0,"exp":'"Upon completing" = 完成後立即'},
    {"q":"The document needs to be _____ before distribution.","opts":["proofread","proofreading","to proofread","proofread by"],"ans":0,"exp":"need to be + p.p. 被動不定詞"},
    {"q":"Please let me know if you have _____ questions.","opts":["any","some","many","few"],"ans":0,"exp":"疑問或條件句中用 any"},
    {"q":"The seminar will be held _____ the third floor.","opts":["on","in","at","by"],"ans":0,"exp":"樓層用 on（在幾樓）"},
    {"q":"Sales _____ by 15% if we launch the new product.","opts":["will increase","would increase","increase","are increasing"],"ans":0,"exp":"真實條件句：if + 現在式，主句用 will"},
    {"q":"The CEO will _____ the annual shareholders' meeting.","opts":["address","speech","talk","speak"],"ans":0,"exp":'"Address the meeting" = 在會議上發言'},
    {"q":"The project is behind schedule _____ unexpected delays.","opts":["due to","because","so","however"],"ans":0,"exp":'"Due to" 後接名詞'},
    {"q":"Employees must _____ with the company's dress code.","opts":["comply","agreement","follow with","obey to"],"ans":0,"exp":'"Comply with" = 遵守（固定搭配）'},
    {"q":"The report was _____ prepared by the marketing team.","opts":["thoroughly","thorough","thoroughness","thorough in"],"ans":0,"exp":"修飾動詞用副詞 thoroughly"},
    {"q":"Please _____ your supervisor before making any changes.","opts":["consult","consult with","consulting","consulted"],"ans":0,"exp":'"Consult" 可直接接受詞'},
    # --- ESL Lounge 風格 Part 5 補充題（詞形、被動、連接詞、搭配詞）---
    {"q":"The factory implemented _____ safety measures after the inspection.","opts":["effective","effect","effectively","effectiveness"],"ans":0,"exp":"名詞前需形容詞 effective"},
    {"q":"Flight attendants _____ check passengers' seat belts before takeoff.","opts":["routine","routinely","routines","routined"],"ans":1,"exp":"修飾動詞用副詞 routinely"},
    {"q":"The _____ of the new branch office is planned for next quarter.","opts":["open","opening","opened","openly"],"ans":1,"exp":"the + 動名詞作名詞 opening"},
    {"q":"The head chef _____ inspects each dish before it is served.","opts":["personal","personality","personally","personalize"],"ans":2,"exp":"修飾動詞 inspects 用副詞 personally"},
    {"q":"All invoices must be _____ by the finance director.","opts":["approval","approve","approved","approving"],"ans":2,"exp":"被動語態：must be + p.p."},
    {"q":"The new regulation requires _____ of all financial transactions.","opts":["disclose","disclosing","disclosure","disclosed"],"ans":2,"exp":"requires + 名詞：disclosure（揭露）"},
    {"q":"The project was _____ due to a lack of funding.","opts":["suspend","suspended","suspending","suspension"],"ans":1,"exp":"was + p.p. 被動：was suspended 暫停"},
    {"q":"The marketing team held a _____ to brainstorm new ideas.","opts":["session","sessions","sessional","sessionize"],"ans":0,"exp":"hold a session = 舉辦會議"},
    {"q":"Applicants should _____ three professional references.","opts":["provide","providing","provided","provision"],"ans":0,"exp":"should + 原形動詞 provide"},
    {"q":"The contract will be _____ once both parties sign the agreement.","opts":["finalize","finalizing","finalized","finalization"],"ans":2,"exp":"will be + p.p. 被動：finalized"},
    {"q":"_____ the team worked overtime, the deadline was still missed.","opts":["Although","Due to","Therefore","However"],"ans":0,"exp":"Although 引導讓步副詞子句，後接完整句"},
    {"q":"The new software has greatly _____ our data processing speed.","opts":["improve","improved","improvement","improving"],"ans":1,"exp":"has + p.p. 現在完成式：improved"},
    {"q":"The manager asked for _____ feedback from all department heads.","opts":["write","written","writing","writes"],"ans":1,"exp":"written feedback 書面回饋（形容詞）"},
    {"q":"_____ the merger is completed, staff will be notified of any changes.","opts":["Once","Despite","Unless","Whereas"],"ans":0,"exp":"Once = 一旦…就，表時間條件"},
    {"q":"Customer satisfaction scores have _____ since the new policy was introduced.","opts":["raise","risen","risen up","raised"],"ans":1,"exp":"不及物動詞 rise 的完成式是 risen"},
    {"q":"The proposal was _____ accepted by the board of directors.","opts":["unanimous","unanimously","unanimity","unanimousness"],"ans":1,"exp":"修飾 accepted（動詞）用副詞 unanimously"},
    {"q":"All employees are _____ to attend the mandatory safety training.","opts":["require","required","requiring","requirement"],"ans":1,"exp":"are required to = 被要求，被動語態"},
    {"q":"The new policy is designed to _____ workplace efficiency.","opts":["maximize","maximum","maximally","maximization"],"ans":0,"exp":"to + 原形動詞 maximize 最大化"},
    {"q":"_____ careful planning, the event was a great success.","opts":["Thanks to","Although","However","Unless"],"ans":0,"exp":"Thanks to 後接名詞，表原因"},
    {"q":"She has a proven _____ for meeting tight deadlines.","opts":["capable","capability","capably","capableness"],"ans":1,"exp":"a proven + 名詞 capability 能力"},
    {"q":"The annual sales figures _____ at the board meeting last Friday.","opts":["present","were presented","presenting","has presented"],"ans":1,"exp":"被動語態：were + p.p. presented"},
    {"q":"The new hire completed the training _____ than expected.","opts":["quick","quicker","more quickly","most quickly"],"ans":2,"exp":"修飾動詞 completed 用副詞比較級 more quickly"},
    {"q":"All staff are asked to _____ their access badges at all times.","opts":["carry","carrying","carried","carries"],"ans":0,"exp":"are asked to + 原形動詞 carry"},
    {"q":"The company's _____ policy ensures a safe work environment for everyone.","opts":["safe","safety","safely","safeness"],"ans":1,"exp":"名詞修飾名詞 policy → safety policy 安全政策"},
]

LISTEN_P2 = [
    {"q":"When will the budget report be ready?","opts":["A. It's on the third shelf.","B. By Thursday afternoon.","C. The budget was approved."],"ans":1,"exp":"問何時，答 By Thursday 最符合"},
    {"q":"Who is in charge of the marketing campaign?","opts":["A. Ms. Chen is leading it.","B. The campaign starts in May.","C. We have a new product."],"ans":0,"exp":"問人，答 Ms. Chen 最直接"},
    {"q":"Has the client confirmed the meeting time?","opts":["A. Yes, two o'clock is fine.","B. The client is very satisfied.","C. The meeting room is available."],"ans":0,"exp":"Yes/No 問句，A 最合適"},
    {"q":"Where should I submit the expense report?","opts":["A. It was submitted yesterday.","B. To the accounting department.","C. The report is very detailed."],"ans":1,"exp":"問 where，答地點"},
    {"q":"Why was the project deadline extended?","opts":["A. The deadline is Friday.","B. Because of unexpected technical issues.","C. The project was very successful."],"ans":1,"exp":"問 why，答 Because 最合適"},
    {"q":"Could you send me the revised contract?","opts":["A. Sure, I'll email it right away.","B. The contract was signed.","C. I don't have a contract."],"ans":0,"exp":"請求，A 表示同意最合適"},
    {"q":"When does the new employee orientation begin?","opts":["A. The orientation was very helpful.","B. It begins at nine tomorrow morning.","C. There are five new employees."],"ans":1,"exp":"問何時，答具體時間"},
    {"q":"How many people attended the conference?","opts":["A. The conference was in Tokyo.","B. About 300 participants.","C. It lasted three days."],"ans":1,"exp":"問數量，答約 300 人"},
    {"q":"Is the printer on the second floor working?","opts":["A. I printed ten copies.","B. No, it's being repaired.","C. The printer is expensive."],"ans":1,"exp":"Yes/No 問句，B 最合適"},
    {"q":"Who should I contact about the IT issue?","opts":["A. Call the IT help desk.","B. The IT department is on Floor 3.","C. The issue was resolved."],"ans":0,"exp":"問聯絡對象，A 直接回答"},
]

LISTEN_P3 = [
    {"title":"對話 1：預約會議室","lines":["M: Hi, I need to book the large conference room for Friday afternoon.","W: Let me check the schedule. I'm sorry, it's already reserved from 2 to 5 PM.","M: How about in the morning? Say, from 9 to 11?","W: That's available. Shall I reserve it for you now?","M: Yes, please. It's for the sales team's quarterly review."],
     "qs":[{"q":"What does the man want to do?","opts":["Book a conference room","Cancel a reservation","Check the schedule","Move a meeting"],"ans":0},{"q":"Why is the large room unavailable in the afternoon?","opts":["It is being renovated","It is already reserved","It is too small","It is closed"],"ans":1},{"q":"What time will the meeting be held?","opts":["9 to 11 AM","2 to 5 PM","1 to 3 PM","All day"],"ans":0}]},
    {"title":"對話 2：訂購辦公用品","lines":["W: I noticed we're running low on printer paper and toner cartridges.","M: You're right. I'll put in an order this afternoon.","W: Could you also add some pens and sticky notes to the order?","M: Sure. Do you need anything else?","W: That should be enough. Oh, and please get express shipping — we need them by Wednesday."],
     "qs":[{"q":"What is the main topic?","opts":["A broken printer","Ordering office supplies","Hiring new staff","Planning a meeting"],"ans":1},{"q":"What shipping does the woman request?","opts":["Standard","Express","Overnight","Free"],"ans":1},{"q":"When do they need the supplies?","opts":["Monday","Tuesday","Wednesday","Friday"],"ans":2}]},
]

LISTEN_P4 = [
    {"title":"獨白 1：機場廣播","text":"Attention, passengers on Flight KA 305 to Singapore. Due to a technical issue, boarding will be delayed by approximately 45 minutes. The new boarding time is 3:30 PM at Gate 22. Passengers requiring special assistance should proceed to the gate immediately. We apologize for the inconvenience and thank you for your patience.",
     "qs":[{"q":"Why is the flight delayed?","opts":["Bad weather","A technical issue","Gate change","Staff shortage"],"ans":1},{"q":"What is the new boarding time?","opts":["3:00 PM","3:15 PM","3:30 PM","4:00 PM"],"ans":2},{"q":"Who is asked to go to the gate immediately?","opts":["All passengers","Business class only","Passengers needing special help","Frequent flyers"],"ans":2}]},
    {"title":"獨白 2：公司廣播","text":"Good morning, everyone. This is a reminder that the annual company picnic will be held this Saturday at Riverside Park, starting at 10 AM. All employees and their families are welcome. Please bring your own chairs and sunscreen. Lunch will be provided by the company. If you haven't signed up yet, please contact HR by tomorrow afternoon.",
     "qs":[{"q":"What event is being announced?","opts":["A company meeting","An annual picnic","A training seminar","An award ceremony"],"ans":1},{"q":"What should employees bring?","opts":["Food and drinks","Their own chairs","Company ID","A laptop"],"ans":1},{"q":"By when should employees sign up?","opts":["This morning","Tomorrow afternoon","Saturday morning","End of this week"],"ans":1}]},
]

READINGS = [
    {"title":"Email: Project Status Update","text":"""To: All Project Team Members\nFrom: Sarah Chen, Project Manager\nSubject: Q3 Project Update\n\nDear Team,\n\nI wanted to share a brief update on the status of our Q3 initiative. As of this week, we have completed 75% of the planned deliverables. The development phase is on track, and we expect to finish by the end of next week.\n\nHowever, the testing phase is slightly behind schedule due to some unexpected technical issues. To address this, I have arranged for additional QA support starting Monday. All team members should receive updated timelines by Thursday.\n\nPlease let me know if you have any questions or concerns.\n\nBest regards,\nSarah Chen""",
     "qs":[{"q":"What percentage of deliverables is complete?","opts":["50%","65%","75%","90%"],"ans":2},{"q":"Why is testing behind schedule?","opts":["Lack of staff","Technical issues","Budget cuts","Poor planning"],"ans":1},{"q":"What will team members receive by Thursday?","opts":["New assignments","Updated timelines","Performance reviews","Budget reports"],"ans":1},{"q":"'Initiative' is closest in meaning to:","opts":["Problem","Project","Meeting","Policy"],"ans":1}]},
    {"title":"Notice: Office Renovation","text":"""OFFICE RENOVATION NOTICE\n\nTo all staff:\n\nPlease be advised that the third floor will undergo renovation from June 10 to June 25. During this period, all staff currently located on the third floor will be temporarily relocated to available workstations on floors two and four.\n\nAccess to the third floor will be restricted to authorized personnel only. The elevators will remain operational; however, the stairwell near the east exit will be closed for safety reasons.\n\nIT support will assist with equipment setup in the temporary locations. For questions, please contact facilities management at ext. 305.\n\nManagement""",
     "qs":[{"q":"Which floor is being renovated?","opts":["Second","Third","Fourth","All floors"],"ans":1},{"q":"Where will affected staff be moved?","opts":["To another building","Floors 2 and 4","Work from home","The basement"],"ans":1},{"q":"What will be closed during renovation?","opts":["The elevators","The parking lot","The east stairwell","The main entrance"],"ans":2},{"q":"Who should staff contact for questions?","opts":["HR department","IT support","Facilities management","The CEO"],"ans":2}]},
    {"title":"Advertisement: Job Opening","text":"""HIRING: Senior Marketing Manager\n\nXYZ Corporation is seeking a talented Senior Marketing Manager in Taipei.\n\nResponsibilities:\n• Develop and execute integrated marketing campaigns\n• Manage a team of 5 marketing specialists\n• Analyze market trends and report to senior leadership\n• Oversee social media strategy\n\nRequirements:\n• Bachelor's degree in Marketing or related field\n• Minimum 7 years of marketing experience\n• Strong leadership and communication skills\n• Fluent in English and Mandarin\n\nSalary: Competitive, based on experience\nTo apply, send your resume to careers@xyzgroup.com by July 15.""",
     "qs":[{"q":"How many specialists will the manager oversee?","opts":["3","5","7","10"],"ans":1},{"q":"What language skill is required?","opts":["Japanese","English only","English and Mandarin","Mandarin only"],"ans":2},{"q":"Which is NOT a listed requirement?","opts":["Leadership skills","7 years experience","MBA degree","Marketing background"],"ans":2},{"q":"By when must applications be submitted?","opts":["June 30","July 1","July 15","July 31"],"ans":2}]},
    {"title":"Memo: Remote Work Policy","text":"""MEMORANDUM\n\nTo: All Employees\nFrom: Human Resources\nRe: Updated Remote Work Policy\n\nEffective June 1, the company will implement a hybrid work model. Employees may work remotely up to three days per week, provided they maintain full productivity and attend all scheduled meetings.\n\nRemote workdays must be approved by the direct supervisor at least 48 hours in advance. Employees working remotely must be available during core hours (9 AM – 3 PM) and respond to communications within one hour.\n\nAll remote workers must use the company VPN. Employees who do not comply with this policy may lose remote work privileges.\n\nFor more details, please refer to the full policy document on the company intranet.""",
     "qs":[{"q":"When does the new policy take effect?","opts":["May 1","June 1","July 1","Immediately"],"ans":1},{"q":"How many remote days per week are allowed?","opts":["1","2","3","5"],"ans":2},{"q":"How far in advance must remote days be approved?","opts":["24 hours","48 hours","One week","Same day"],"ans":1},{"q":"What tool must remote workers use?","opts":["A company phone","The company VPN","A time tracker","Video conferencing"],"ans":2}]},
]

BADGES = [
    {"id":"b1","icon":"🌱","name":"初次打卡","req":"累計 1 天","days":1},
    {"id":"b2","icon":"🔥","name":"熱身週","req":"連續 3 天","streak":3},
    {"id":"b3","icon":"💪","name":"習慣養成","req":"連續 7 天","streak":7},
    {"id":"b4","icon":"🌟","name":"雙週達人","req":"連續 14 天","streak":14},
    {"id":"b5","icon":"👑","name":"月度冠軍","req":"連續 30 天","streak":30},
    {"id":"b6","icon":"📚","name":"累積 10 天","req":"累計 10 天","days":10},
    {"id":"b7","icon":"🎯","name":"累積 30 天","req":"累計 30 天","days":30},
    {"id":"b8","icon":"🏆","name":"百日學霸","req":"累計 100 天","days":100},
    {"id":"b9","icon":"⚡","name":"遊戲達人","req":"玩遊戲 10 次","games":10},
    {"id":"b10","icon":"💎","name":"TOEIC 高手","req":"XP 達 1000","xp":1000},
]

# ─────────────────────────────────────────────────────────────────────────────
# 打卡資料持久化（JSON 檔案，Streamlit Cloud 也能用）
# ─────────────────────────────────────────────────────────────────────────────
CHECKIN_FILE = Path(__file__).parent / "checkin_data.json"

def load_checkin():
    if CHECKIN_FILE.exists():
        try:
            return json.loads(CHECKIN_FILE.read_text(encoding="utf-8"))
        except Exception:
            pass
    return {"checkins": [], "streak": 0, "longest_streak": 0, "xp": 0, "badges": [], "game_count": 0}

def save_checkin(data):
    CHECKIN_FILE.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

def calc_streak(checkins: list) -> int:
    if not checkins:
        return 0
    sorted_dates = sorted(date.fromisoformat(d) for d in checkins)
    today = date.today()
    yesterday = today - timedelta(days=1)
    if sorted_dates[-1] not in (today, yesterday):
        return 0
    streak = 1
    for i in range(len(sorted_dates) - 1, 0, -1):
        if (sorted_dates[i] - sorted_dates[i - 1]).days == 1:
            streak += 1
        else:
            break
    return streak

def check_badges(cd):
    new_badges = []
    for b in BADGES:
        if b["id"] in cd["badges"]:
            continue
        unlocked = False
        if "days" in b and len(cd["checkins"]) >= b["days"]:
            unlocked = True
        if "streak" in b and cd["streak"] >= b["streak"]:
            unlocked = True
        if "games" in b and cd["game_count"] >= b["games"]:
            unlocked = True
        if "xp" in b and cd["xp"] >= b["xp"]:
            unlocked = True
        if unlocked:
            cd["badges"].append(b["id"])
            new_badges.append(b)
    return new_badges

# ─────────────────────────────────────────────────────────────────────────────
# Session State
# ─────────────────────────────────────────────────────────────────────────────
def init_state():
    defaults = {
        "learned": set(), "correct": 0, "total": 0, "sessions": 0, "mistakes": [],
        "v_idx": 0, "v_flipped": False, "v_cat": "全部", "v_range": "全部",
        "g_qs": [], "g_idx": 0, "g_done": {}, "g_started": False,
        "lp2_idx": 0, "lp3_idx": 0, "lp3_q": 0, "lp4_idx": 0, "lp4_q": 0,
        "r_idx": 0, "r_done": {},
        "mock_qs": [], "mock_idx": 0, "mock_done": {}, "mock_started": False,
        "mock_end_time": 0.0, "mock_finished": False,
        "rev_idx": 0, "rev_done": {},
        "wl_query": "", "wl_cat": "全部",
        # 遊戲狀態
        "game_active": None,      # 'match' | 'quiz' | 'speed' | None
        "game_end_time": 0.0,
        "game_correct": 0, "game_wrong": 0, "game_xp": 0,
        "match_cards": [], "match_selected": None, "match_matched": set(),
        "gq_qs": [], "gq_idx": 0, "gq_answered": False, "gq_was_correct": False, "gq_chosen": -1,
        "sp_words": [], "sp_idx": 0, "sp_key": 0,
        "game_result": None,      # dict when game ends
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_state()
S = st.session_state

# ─────────────────────────────────────────────────────────────────────────────
# 工具函式
# ─────────────────────────────────────────────────────────────────────────────
def est_toeic():
    if S.total == 0:
        return "—"
    acc = S.correct / S.total
    if acc >= 0.96: return "990 🏆"
    if acc >= 0.92: return "~950"
    if acc >= 0.87: return "~850 ✨"
    if acc >= 0.80: return "~800"
    if acc >= 0.72: return "~730"
    if acc >= 0.62: return "~650"
    return "~550"

def add_mistake(type_, q, correct, chosen):
    S.mistakes.append({"type": type_, "q": q, "correct": correct, "chosen": chosen})
    if len(S.mistakes) > 100:
        S.mistakes.pop(0)

def vocab_filtered():
    result = VOCAB
    if S.v_cat != "全部":
        result = [w for w in result if w["cat"] == S.v_cat]
    if S.v_range != "全部":
        result = [w for w in result if w["range"] == S.v_range]
    return result

def tag_html(pos):
    cls = {"n.": "tag-n", "v.": "tag-v", "adj.": "tag-adj", "adv.": "tag-adv"}.get(pos, "tag-n")
    return f'<span class="tag {cls}">{pos}</span>'

def speak_js(text):
    safe = text.replace("'", "\\'").replace("\n", " ")
    components.html(f"""<script>
    (function(){{
      var u=new SpeechSynthesisUtterance('{safe}');
      u.lang='en-US';u.rate=0.88;u.pitch=1;
      window.speechSynthesis.cancel();
      var vs=window.speechSynthesis.getVoices();
      var en=vs.find(v=>v.lang.startsWith('en'));
      if(en)u.voice=en;
      window.speechSynthesis.speak(u);
    }})();
    </script>""", height=0)

def render_timer(remaining, total):
    pct = max(0, remaining / total * 100)
    mins, secs = int(remaining // 60), int(remaining % 60)
    color = "#10b981" if pct > 50 else "#f59e0b" if pct > 25 else "#ef4444"
    st.markdown(f"""
    <div style="text-align:center;font-size:1.6rem;font-weight:800;color:{color};margin-bottom:4px">
      ⏱ {mins:02d}:{secs:02d}
    </div>
    <div class="pb-wrap"><div class="pb" style="width:{pct:.0f}%;background:{color}"></div></div>
    """, unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# 頁面：首頁儀表板
# ─────────────────────────────────────────────────────────────────────────────
def page_home():
    st.markdown("""<div class="hero"><h1>🎯 TOEIC Pro 850+</h1>
    <p>系統化備考，穩定達成多益 850 分目標</p></div>""", unsafe_allow_html=True)
    acc = f"{S.correct/S.total*100:.0f}%" if S.total > 0 else "—"
    cd = load_checkin()
    st.markdown(f"""
    <div class="stat-grid">
      <div class="stat-box"><div class="stat-num">{len(S.learned)}</div><div class="stat-lbl">📚 已學單字</div></div>
      <div class="stat-box"><div class="stat-num">{acc}</div><div class="stat-lbl">🎯 整體正確率</div></div>
      <div class="stat-box"><div class="stat-num">{S.sessions}</div><div class="stat-lbl">✅ 練習次數</div></div>
      <div class="stat-box"><div class="stat-num">{len(S.mistakes)}</div><div class="stat-lbl">🔴 待複習錯題</div></div>
      <div class="stat-box"><div class="stat-num">{est_toeic()}</div><div class="stat-lbl">📊 預估多益分數</div></div>
      <div class="stat-box"><div class="stat-num">{cd['streak']}🔥</div><div class="stat-lbl">連續打卡天數</div></div>
      <div class="stat-box"><div class="stat-num">{cd['xp']}⭐</div><div class="stat-lbl">累積 XP</div></div>
    </div>
    """, unsafe_allow_html=True)
    if S.total > 0:
        pct = S.correct / S.total
        st.markdown(f"""<div class="tcard"><b>整體進度</b>　{S.correct}/{S.total} 題正確
        <div class="pb-wrap"><div class="pb" style="width:{pct*100:.0f}%"></div></div>
        <small style="color:#64748b">目標：87% 以上 → 預估 850+</small></div>""", unsafe_allow_html=True)
    st.info("💡 **今日建議：** 先完成每日打卡 → 玩一局小遊戲 → 練習 30 張單字卡\n\n🎯 **目標：整體正確率 87% 以上 → 預估多益 850 分**")

# ─────────────────────────────────────────────────────────────────────────────
# 頁面：每日打卡
# ─────────────────────────────────────────────────────────────────────────────
def page_checkin():
    st.markdown("## 📅 每日打卡")
    cd = load_checkin()
    today_str = date.today().isoformat()
    done_today = today_str in cd["checkins"]

    # Streak 橫幅
    streak_icon = "🔥" if cd["streak"] >= 7 else "✨" if cd["streak"] >= 3 else "💫"
    st.markdown(f"""
    <div class="streak-banner">
      <div style="font-size:3rem">{streak_icon}</div>
      <div>
        <div class="streak-num">{cd['streak']}</div>
        <div class="streak-label">連續打卡天數</div>
      </div>
      <div style="margin-left:auto;text-align:right">
        <div style="font-size:1.8rem;font-weight:800">⭐ {cd['xp']} XP</div>
        <div style="opacity:.8;font-size:.85rem">累計打卡 {len(cd['checkins'])} 天　最長 {cd['longest_streak']} 天</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # 打卡按鈕
    col1, col2 = st.columns([1, 3])
    with col1:
        if done_today:
            st.button("✅ 今日已打卡", disabled=True, use_container_width=True)
        else:
            if st.button("📅 今日打卡！", type="primary", use_container_width=True):
                cd["checkins"].append(today_str)
                cd["checkins"] = sorted(set(cd["checkins"]))
                streak = calc_streak(cd["checkins"])
                cd["streak"] = streak
                cd["longest_streak"] = max(cd["longest_streak"], streak)
                xp = 10
                if streak % 30 == 0: xp += 200
                elif streak % 7 == 0: xp += 50
                elif streak % 3 == 0: xp += 20
                cd["xp"] += xp
                new_badges = check_badges(cd)
                save_checkin(cd)
                st.success(f"🎉 打卡成功！+{xp} XP  連續 {streak} 天")
                for b in new_badges:
                    st.balloons()
                    st.info(f"🏅 解鎖成就：{b['icon']} **{b['name']}**！")
                st.rerun()
    with col2:
        if done_today:
            st.success(f"今天已打卡 ✓　連續 {cd['streak']} 天　明天繼續加油！")
        else:
            st.info("今天還沒打卡！每日打卡 +10 XP，連續越多天獎勵越多！")

    st.markdown("---")

    # 月曆
    st.markdown("### 📆 本月打卡記錄")
    _render_calendar_html(cd["checkins"])

    st.markdown("---")

    # XP 說明
    with st.expander("💡 XP 獎勵說明"):
        st.markdown("""
| 條件 | 獎勵 |
|------|------|
| 每日打卡 | +10 XP |
| 連續 3 天 | 額外 +20 XP |
| 連續 7 天 | 額外 +50 XP |
| 連續 30 天 | 額外 +200 XP |
| 遊戲勝利 | +5 ~ 30 XP |
        """)

    st.markdown("---")

    # 徽章
    st.markdown("### 🏅 成就徽章")
    badge_html = '<div class="badge-grid">'
    for b in BADGES:
        unlocked = b["id"] in cd["badges"]
        cls = "badge-item badge-unlocked" if unlocked else "badge-item badge-locked"
        badge_html += f"""
        <div class="{cls}">
          <div class="badge-icon">{b['icon']}</div>
          <div class="badge-name">{b['name']}</div>
          <div class="badge-req">{b['req']}</div>
        </div>"""
    badge_html += '</div>'
    st.markdown(badge_html, unsafe_allow_html=True)

def _render_calendar_html(checkins: list):
    today = date.today()
    year, month = today.year, today.month
    checkin_set = set(checkins)
    first_weekday = (date(year, month, 1).weekday() + 1) % 7  # Sun=0
    days_in_month = cal_mod.monthrange(year, month)[1]

    html = f"""
    <div style="background:white;border-radius:14px;padding:1.2rem;border:1px solid #e2e8f0;margin-bottom:1rem">
      <div style="text-align:center;font-weight:700;margin-bottom:12px;color:#1e293b">{year}年{month}月</div>
      <div style="display:grid;grid-template-columns:repeat(7,1fr);gap:5px">
    """
    for d in ["日","一","二","三","四","五","六"]:
        html += f'<div style="text-align:center;font-size:.7rem;color:#64748b;font-weight:700;padding:4px">{d}</div>'
    for _ in range(first_weekday):
        html += '<div></div>'
    for d in range(1, days_in_month + 1):
        ds = f"{year}-{month:02d}-{d:02d}"
        if ds in checkin_set:
            style = "background:#7c3aed;color:white;border-radius:8px;text-align:center;padding:6px 2px;font-weight:700;font-size:.85rem"
            content = f"✓{d}"
        elif ds == today.isoformat():
            style = "border:2px solid #7c3aed;border-radius:8px;text-align:center;padding:5px 2px;font-weight:700;color:#7c3aed;font-size:.85rem"
            content = str(d)
        else:
            style = "background:#f8fafc;border-radius:8px;text-align:center;padding:6px 2px;color:#94a3b8;font-size:.85rem"
            content = str(d)
        html += f'<div style="{style}">{content}</div>'
    html += "</div></div>"
    st.markdown(html, unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# 頁面：小遊戲
# ─────────────────────────────────────────────────────────────────────────────
def page_games():
    st.markdown("## 🎮 小遊戲")

    # 顯示遊戲結果
    if S.game_result:
        _show_game_result()
        return

    # 遊戲中
    if S.game_active == "match":
        _run_match_game()
        return
    if S.game_active == "quiz":
        _run_quiz_game()
        return
    if S.game_active == "speed":
        _run_speed_game()
        return

    # 選遊戲
    cd = load_checkin()
    st.markdown(f'<div style="margin-bottom:1rem">你的 XP：<span class="xp-pill">⭐ {cd["xp"]} XP</span>　今日遊戲可額外加分！</div>', unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("""<div class="game-pick-card"><div class="game-icon">🔗</div>
        <h3 style="margin:.3rem 0">單字配對</h3>
        <p style="color:#64748b;font-size:.85rem">90秒內配對英文↔中文</p>
        <div style="font-size:.75rem;color:#7c3aed;margin-top:.5rem">答對 +5 XP</div>
        </div>""", unsafe_allow_html=True)
        if st.button("▶️ 開始配對", key="start_match", use_container_width=True):
            _init_match_game()
    with c2:
        st.markdown("""<div class="game-pick-card"><div class="game-icon">⚡</div>
        <h3 style="margin:.3rem 0">快速測驗</h3>
        <p style="color:#64748b;font-size:.85rem">120秒 TOEIC 文法選擇題</p>
        <div style="font-size:.75rem;color:#7c3aed;margin-top:.5rem">答對 +10 XP</div>
        </div>""", unsafe_allow_html=True)
        if st.button("▶️ 開始測驗", key="start_quiz", use_container_width=True):
            _init_quiz_game()
    with c3:
        st.markdown("""<div class="game-pick-card"><div class="game-icon">⌨️</div>
        <h3 style="margin:.3rem 0">拼字挑戰</h3>
        <p style="color:#64748b;font-size:.85rem">60秒看中文打英文單字</p>
        <div style="font-size:.75rem;color:#7c3aed;margin-top:.5rem">答對 +8 XP</div>
        </div>""", unsafe_allow_html=True)
        if st.button("▶️ 開始拼字", key="start_speed", use_container_width=True):
            _init_speed_game()

# ── 遊戲初始化 ────────────────────────────────────────────────────────────────
def _init_match_game():
    pairs = random.sample(VOCAB, 6)
    en_cards = [{"text": p["word"], "type": "en", "pair": i} for i, p in enumerate(pairs)]
    zh_cards = [{"text": p["zh"],  "type": "zh", "pair": i} for i, p in enumerate(pairs)]
    cards = en_cards + zh_cards
    random.shuffle(cards)
    S.game_active = "match"
    S.match_cards = cards
    S.match_selected = None
    S.match_matched = set()
    S.game_correct = 0; S.game_wrong = 0; S.game_xp = 0
    S.game_end_time = time.time() + 90
    S.game_result = None
    st.rerun()

def _init_quiz_game():
    S.game_active = "quiz"
    S.gq_qs = random.sample(GRAMMAR_QS, 10)
    S.gq_idx = 0; S.gq_answered = False; S.gq_was_correct = False; S.gq_chosen = -1
    S.game_correct = 0; S.game_wrong = 0; S.game_xp = 0
    S.game_end_time = time.time() + 120
    S.game_result = None
    st.rerun()

def _init_speed_game():
    S.game_active = "speed"
    S.sp_words = [{"en": w["word"], "zh": w["zh"]} for w in random.sample(VOCAB, 12)]
    S.sp_idx = 0; S.sp_key = 0
    S.game_correct = 0; S.game_wrong = 0; S.game_xp = 0
    S.game_end_time = time.time() + 60
    S.game_result = None
    st.rerun()

# ── 共用遊戲標頭 ──────────────────────────────────────────────────────────────
def _game_header(title, total_time):
    remaining = max(0, S.game_end_time - time.time())
    col1, col2, col3 = st.columns([3, 2, 1])
    with col1:
        st.markdown(f"### {title}")
    with col2:
        render_timer(remaining, total_time)
    with col3:
        if st.button("✕ 結束", use_container_width=True):
            _end_game(forced=True)
    st.markdown(f"✅ 正確 **{S.game_correct}**　❌ 錯誤 **{S.game_wrong}**　⭐ **{S.game_xp} XP**")
    st.markdown("---")
    return remaining

def _end_game(forced=False):
    total = S.game_correct + S.game_wrong
    acc = int(S.game_correct / total * 100) if total > 0 else 0
    xp_earned = S.game_xp
    # 儲存到打卡資料
    cd = load_checkin()
    cd["xp"] += xp_earned
    cd["game_count"] += 1
    new_badges = check_badges(cd)
    save_checkin(cd)
    S.game_result = {
        "game": S.game_active, "correct": S.game_correct,
        "total": total, "acc": acc, "xp": xp_earned,
        "forced": forced, "new_badges": new_badges
    }
    S.game_active = None
    S.sessions += 1
    st.rerun()

# ── 配對遊戲 ──────────────────────────────────────────────────────────────────
def _run_match_game():
    remaining = _game_header("🔗 單字配對", 90)
    if remaining <= 0:
        _end_game()
        return

    st.caption("點選英文單字，再點選對應的中文意思")
    cards = S.match_cards
    matched = S.match_matched
    cols = st.columns(4)

    for i, card in enumerate(cards):
        with cols[i % 4]:
            if card["pair"] in matched:
                st.markdown(f'<div class="mc-card-matched">✓ {card["text"]}</div>', unsafe_allow_html=True)
            elif S.match_selected == i:
                st.markdown(f'<div class="mc-card-selected">▶ {card["text"]}</div>', unsafe_allow_html=True)
                if st.button("取消", key=f"mc_cancel_{i}", use_container_width=True):
                    S.match_selected = None
                    st.rerun()
            else:
                if st.button(card["text"], key=f"mc_{i}", use_container_width=True):
                    if S.match_selected is None:
                        S.match_selected = i
                    else:
                        prev = cards[S.match_selected]
                        cur = card
                        if prev["pair"] == cur["pair"] and prev["type"] != cur["type"]:
                            matched.add(cur["pair"])
                            S.game_correct += 1
                            S.game_xp += 5
                            S.match_selected = None
                            if len(matched) == 6:
                                S.game_xp += 10  # 全對bonus
                                _end_game()
                                return
                        else:
                            S.game_wrong += 1
                            S.match_selected = None
                    st.rerun()

    pct = len(matched) / 6 * 100
    st.markdown(f'<div class="pb-wrap"><div class="pb" style="width:{pct:.0f}%"></div></div><small>已配對 {len(matched)}/6 組</small>', unsafe_allow_html=True)

# ── 快速測驗 ──────────────────────────────────────────────────────────────────
def _run_quiz_game():
    remaining = _game_header("⚡ 快速測驗", 120)
    if remaining <= 0:
        _end_game()
        return

    qs = S.gq_qs
    idx = S.gq_idx

    if idx >= len(qs):
        _end_game()
        return

    q = qs[idx]
    pct = idx / len(qs) * 100
    st.markdown(f'<div class="pb-wrap"><div class="pb" style="width:{pct:.0f}%"></div></div><small>第 {idx+1}/{len(qs)} 題</small>', unsafe_allow_html=True)
    st.markdown(f"<div class='tcard'><b>Q{idx+1}.</b> {q['q']}</div>", unsafe_allow_html=True)

    if not S.gq_answered:
        for i, opt in enumerate(q["opts"]):
            if st.button(f"{chr(65+i)}. {opt}", key=f"gq_{idx}_{i}", use_container_width=True):
                ok = (i == q["ans"])
                S.gq_answered = True
                S.gq_was_correct = ok
                S.gq_chosen = i
                if ok:
                    S.game_correct += 1; S.game_xp += 10
                else:
                    S.game_wrong += 1
                    add_mistake("game_quiz", q["q"], q["opts"][q["ans"]], q["opts"][i])
                st.rerun()
    else:
        for i, opt in enumerate(q["opts"]):
            label = f"{chr(65+i)}. {opt}"
            if i == q["ans"]:
                st.markdown(f'<div style="background:#ecfdf5;border:2px solid #10b981;border-radius:10px;padding:.6rem 1rem;margin:.25rem 0">✅ {label}</div>', unsafe_allow_html=True)
            elif i == S.gq_chosen and not S.gq_was_correct:
                st.markdown(f'<div style="background:#fef2f2;border:2px solid #ef4444;border-radius:10px;padding:.6rem 1rem;margin:.25rem 0">❌ {label}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div style="background:#f8fafc;border:1px solid #e2e8f0;border-radius:10px;padding:.6rem 1rem;margin:.25rem 0;color:#94a3b8">{label}</div>', unsafe_allow_html=True)
        if S.gq_was_correct:
            st.markdown('<div class="fb-ok">✅ 答對！' + q["exp"] + '</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="fb-bad">❌ 答錯。正確：<b>' + q["opts"][q["ans"]] + '</b><br>💡 ' + q["exp"] + '</div>', unsafe_allow_html=True)
        if st.button("下一題 →", type="primary"):
            S.gq_idx += 1; S.gq_answered = False; S.gq_was_correct = False
            st.rerun()

# ── 拼字挑戰 ──────────────────────────────────────────────────────────────────
def _run_speed_game():
    remaining = _game_header("⌨️ 拼字挑戰", 60)
    if remaining <= 0:
        _end_game()
        return

    words = S.sp_words
    idx = S.sp_idx

    if idx >= len(words):
        _end_game()
        return

    w = words[idx]
    hint = w["en"][0] + "_" * (len(w["en"]) - 1)
    pct_done = idx / len(words)
    dots = "".join(["🟣" if i < idx else "⬜" for i in range(len(words))])

    st.markdown(f"""
    <div style="text-align:center;margin-bottom:1rem">
      <div style="font-size:2rem;font-weight:800;color:#7c3aed">{w['zh']}</div>
      <div style="color:#64748b;font-size:.9rem;margin-top:.3rem">提示：{hint}（共 {len(w['en'])} 個字母）</div>
      <div style="font-size:.7rem;letter-spacing:4px;margin-top:.6rem">{dots}</div>
    </div>
    """, unsafe_allow_html=True)

    with st.form(key=f"sp_form_{idx}_{S.sp_key}", clear_on_submit=True):
        answer = st.text_input("輸入英文單字", placeholder="按 Enter 提交", label_visibility="collapsed")
        c1, c2 = st.columns(2)
        submitted = c1.form_submit_button("✅ 確認", use_container_width=True)
        skipped = c2.form_submit_button("⏭ 跳過", use_container_width=True)

    if submitted and answer:
        if answer.strip().lower() == w["en"].lower():
            st.success(f"✅ 正確！{w['en']} = {w['zh']}")
            S.game_correct += 1; S.game_xp += 8
        else:
            st.error(f"❌ 答案是：**{w['en']}**")
            S.game_wrong += 1
            add_mistake("game_speed", w["zh"], w["en"], answer.strip())
        S.sp_idx += 1; S.sp_key += 1
        time.sleep(0.6)
        st.rerun()
    elif skipped:
        st.warning(f"跳過　正確答案：**{w['en']}**")
        S.game_wrong += 1
        S.sp_idx += 1; S.sp_key += 1
        time.sleep(0.5)
        st.rerun()

# ── 遊戲結果 ──────────────────────────────────────────────────────────────────
def _show_game_result():
    r = S.game_result
    game_names = {"match": "🔗 單字配對", "quiz": "⚡ 快速測驗", "speed": "⌨️ 拼字挑戰"}
    gname = game_names.get(r["game"], "遊戲")
    emoji = "🤩" if r["acc"] >= 80 else "😊" if r["acc"] >= 60 else "💪"

    st.markdown(f"""
    <div style="background:linear-gradient(135deg,#7c3aed,#2563eb);color:white;border-radius:20px;
      padding:2.5rem;text-align:center;margin-bottom:1.5rem">
      <div style="font-size:4rem">{emoji}</div>
      <div style="font-size:2.5rem;font-weight:900;margin:.5rem 0">{r['acc']}%</div>
      <div style="font-size:1.1rem">{gname}　正確 {r['correct']}/{r['total']} 題</div>
      <div style="margin-top:1rem;font-size:1.4rem;font-weight:700">+{r['xp']} XP 🎉</div>
    </div>
    """, unsafe_allow_html=True)

    for b in r.get("new_badges", []):
        st.success(f"🏅 解鎖成就：{b['icon']} **{b['name']}**！")

    c1, c2 = st.columns(2)
    with c1:
        if st.button("🔄 再玩一次", type="primary", use_container_width=True):
            game_type = r["game"]
            S.game_result = None
            if game_type == "match": _init_match_game()
            elif game_type == "quiz": _init_quiz_game()
            elif game_type == "speed": _init_speed_game()
    with c2:
        if st.button("← 回選擇", use_container_width=True):
            S.game_result = None
            st.rerun()

# ─────────────────────────────────────────────────────────────────────────────
# 頁面：單字卡
# ─────────────────────────────────────────────────────────────────────────────
def page_vocab():
    st.markdown("## 📚 單字卡練習")
    c1, c2 = st.columns(2)
    with c1:
        cats = ["全部"] + sorted(set(w["cat"] for w in VOCAB))
        S.v_cat = st.selectbox("分類篩選", cats, index=cats.index(S.v_cat))
    with c2:
        ranges = ["全部", "600-780", "780-900", "900+"]
        S.v_range = st.selectbox("分數區間", ranges, index=ranges.index(S.v_range))
    words = vocab_filtered()
    if S.v_idx >= len(words): S.v_idx = 0
    total_w = len(words)
    done_w = len([w for w in words if w["word"] in S.learned])
    st.markdown(f'<div class="pb-wrap"><div class="pb" style="width:{done_w/total_w*100:.0f}%"></div></div><small>已學 {done_w}/{total_w}　第 {S.v_idx+1}/{total_w} 張</small>', unsafe_allow_html=True)
    w = words[S.v_idx]
    if not S.v_flipped:
        st.markdown(f'<div class="flashcard"><div class="fc-word">{w["word"]}</div><div class="fc-pos">{w["pos"]} ‧ {w["cat"]}</div><div style="margin-top:1rem;font-size:.85rem;opacity:.7">點擊「翻牌」查看意思</div></div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="flashcard" style="background:linear-gradient(135deg,#059669,#047857)"><div class="fc-zh">{w["zh"]}</div><div class="fc-ex">"{w["ex"]}"</div></div>', unsafe_allow_html=True)
    c1,c2,c3,c4 = st.columns(4)
    with c1:
        if st.button("🔊 發音", use_container_width=True): speak_js(w["word"]+". "+w["ex"])
    with c2:
        if st.button("翻牌 🔄" if not S.v_flipped else "收起 🔄", use_container_width=True):
            S.v_flipped = not S.v_flipped; st.rerun()
    with c3:
        if st.button("✅ 已學會", use_container_width=True):
            S.learned.add(w["word"]); S.v_idx=(S.v_idx+1)%len(words); S.v_flipped=False; st.rerun()
    with c4:
        if st.button("➡️ 下一張", use_container_width=True):
            S.v_idx=(S.v_idx+1)%len(words); S.v_flipped=False; st.rerun()
    with st.expander("🔀 隨機跳至"):
        if st.button("隨機一張"):
            S.v_idx=random.randint(0,len(words)-1); S.v_flipped=False; st.rerun()

# ─────────────────────────────────────────────────────────────────────────────
# 頁面：文法測驗
# ─────────────────────────────────────────────────────────────────────────────
def page_grammar():
    st.markdown("## 📝 文法測驗（Part 5）")
    if not S.g_started:
        st.info(f"共 {len(GRAMMAR_QS)} 題，涵蓋時態、介系詞、詞性辨別、固定片語等考點。")
        if st.button("▶️ 開始測驗", type="primary"):
            S.g_qs=random.sample(GRAMMAR_QS,len(GRAMMAR_QS)); S.g_idx=0; S.g_done={}; S.g_started=True; S.sessions+=1; st.rerun()
        return
    qs=S.g_qs; idx=S.g_idx; done=S.g_done
    if idx >= len(qs):
        correct=sum(1 for v in done.values() if v["ok"])
        acc=correct/len(qs)*100
        st.success(f"### 測驗完成！正確率 {acc:.0f}%  ({correct}/{len(qs)})")
        S.correct+=correct; S.total+=len(qs)
        if st.button("🔄 再來一次"): S.g_started=False; st.rerun()
        st.markdown("#### 錯題回顧")
        for k,v in done.items():
            if not v["ok"]:
                q=qs[int(k)]
                with st.expander(f"❌ Q{int(k)+1}: {q['q']}"):
                    st.error(f"你選了：{q['opts'][v['chosen']]}"); st.success(f"正確答案：{q['opts'][q['ans']]}"); st.info(f"💡 {q['exp']}")
        return
    q=qs[idx]; answered=str(idx) in done
    pct=idx/len(qs)
    st.markdown(f'<div class="pb-wrap"><div class="pb" style="width:{pct*100:.0f}%"></div></div><small>第 {idx+1}/{len(qs)} 題</small>', unsafe_allow_html=True)
    st.markdown(f"<div class='tcard'><b>Q{idx+1}.</b> {q['q']}</div>", unsafe_allow_html=True)
    for i,opt in enumerate(q["opts"]):
        label=f"{chr(65+i)}. {opt}"
        if answered:
            v=done[str(idx)]
            if i==q["ans"]: st.markdown(f'<div style="background:#ecfdf5;border:2px solid #10b981;border-radius:10px;padding:.6rem 1rem;margin:.3rem 0">✅ {label}</div>', unsafe_allow_html=True)
            elif i==v["chosen"]: st.markdown(f'<div style="background:#fef2f2;border:2px solid #ef4444;border-radius:10px;padding:.6rem 1rem;margin:.3rem 0">❌ {label}</div>', unsafe_allow_html=True)
            else: st.markdown(f'<div style="background:#f8fafc;border:1px solid #e2e8f0;border-radius:10px;padding:.6rem 1rem;margin:.3rem 0;color:#64748b">{label}</div>', unsafe_allow_html=True)
        else:
            if st.button(label, key=f"g_{idx}_{i}", use_container_width=True):
                ok=(i==q["ans"]); done[str(idx)]={"chosen":i,"ok":ok}
                if not ok: add_mistake("grammar",q["q"],q["opts"][q["ans"]],q["opts"][i])
                st.rerun()
    if answered:
        v=done[str(idx)]
        if v["ok"]: st.markdown(f'<div class="fb-ok">✅ {q["exp"]}</div>', unsafe_allow_html=True)
        else: st.markdown(f'<div class="fb-bad">❌ 答錯。正確：<b>{q["opts"][q["ans"]]}</b><br>💡 {q["exp"]}</div>', unsafe_allow_html=True)
        if st.button("下一題 →", type="primary"): S.g_idx+=1; st.rerun()

# ─────────────────────────────────────────────────────────────────────────────
# 頁面：聽力
# ─────────────────────────────────────────────────────────────────────────────
def page_listening():
    st.markdown("## 🎧 聽力練習")
    st.info("請確認瀏覽器已允許音訊，點擊「播放」後系統將朗讀題目。", icon="🔊")
    tab1,tab2,tab3 = st.tabs(["Part 2 應答題","Part 3 對話題","Part 4 獨白題"])
    with tab1:
        st.markdown(f"**Part 2：聽一個問句，選出最佳回應**（共 {len(LISTEN_P2)} 題）")
        idx=S.lp2_idx
        if idx>=len(LISTEN_P2): st.success("Part 2 全部完成！")
        else:
            item=LISTEN_P2[idx]
            st.markdown(f'<div class="pb-wrap"><div class="pb" style="width:{idx/len(LISTEN_P2)*100:.0f}%"></div></div><small>第 {idx+1}/{len(LISTEN_P2)} 題</small>', unsafe_allow_html=True)
            st.markdown(f"<div class='tcard'>🎧 **題目：** {item['q']}</div>", unsafe_allow_html=True)
            if st.button("▶️ 播放題目", key=f"p2s{idx}"): speak_js(item["q"])
            for i,opt in enumerate(item["opts"]):
                if st.button(opt, key=f"p2_{idx}_{i}", use_container_width=True):
                    ok=(i==item["ans"]); S.correct+=(1 if ok else 0); S.total+=1
                    if not ok: add_mistake("listen_p2",item["q"],item["opts"][item["ans"]],opt)
                    S.sessions+=1
                    if ok: st.success(f"✅ 正確！{item['exp']}")
                    else: st.error(f"❌ 答錯。正確：{item['opts'][item['ans']]}  解析：{item['exp']}")
            if st.button("下一題 →", key=f"p2n{idx}"): S.lp2_idx+=1; st.rerun()
    with tab2:
        idx3=S.lp3_idx
        if idx3>=len(LISTEN_P3): st.success("Part 3 全部完成！")
        else:
            conv=LISTEN_P3[idx3]
            st.markdown(f"#### {conv['title']}")
            with st.expander("📄 對話內容"):
                for line in conv["lines"]: st.write(line)
            if st.button("▶️ 播放對話", key=f"p3s{idx3}"): speak_js(" ... ".join(conv["lines"]))
            q_idx=S.lp3_q
            if q_idx<len(conv["qs"]):
                q=conv["qs"][q_idx]; st.markdown(f"**Q{q_idx+1}. {q['q']}**")
                for i,opt in enumerate(q["opts"]):
                    if st.button(f"{chr(65+i)}. {opt}", key=f"p3_{idx3}_{q_idx}_{i}", use_container_width=True):
                        ok=(i==q["ans"]); S.correct+=(1 if ok else 0); S.total+=1
                        if not ok: add_mistake("listen_p3",q["q"],q["opts"][q["ans"]],opt)
                        if ok: st.success("✅ 正確！")
                        else: st.error(f"❌ 正確：{q['opts'][q['ans']]}")
                        if q_idx+1>=len(conv["qs"]): S.lp3_idx+=1; S.lp3_q=0
                        else: S.lp3_q+=1
    with tab3:
        idx4=S.lp4_idx
        if idx4>=len(LISTEN_P4): st.success("Part 4 全部完成！")
        else:
            passage=LISTEN_P4[idx4]
            st.markdown(f"#### {passage['title']}")
            with st.expander("📄 獨白內容"): st.write(passage["text"])
            if st.button("▶️ 播放獨白", key=f"p4s{idx4}"): speak_js(passage["text"])
            q_idx=S.lp4_q
            if q_idx<len(passage["qs"]):
                q=passage["qs"][q_idx]; st.markdown(f"**Q{q_idx+1}. {q['q']}**")
                for i,opt in enumerate(q["opts"]):
                    if st.button(f"{chr(65+i)}. {opt}", key=f"p4_{idx4}_{q_idx}_{i}", use_container_width=True):
                        ok=(i==q["ans"]); S.correct+=(1 if ok else 0); S.total+=1
                        if not ok: add_mistake("listen_p4",q["q"],q["opts"][q["ans"]],opt)
                        if ok: st.success("✅ 正確！")
                        else: st.error(f"❌ 正確：{q['opts'][q['ans']]}")
                        if q_idx+1>=len(passage["qs"]): S.lp4_idx+=1; S.lp4_q=0
                        else: S.lp4_q+=1

# ─────────────────────────────────────────────────────────────────────────────
# 頁面：閱讀測驗
# ─────────────────────────────────────────────────────────────────────────────
def page_reading():
    st.markdown("## 📖 閱讀測驗（Part 7）")
    arts=READINGS; idx=S.r_idx; done=S.r_done
    art_names=[f"{'✅' if str(i) in done and len(done[str(i)])==len(arts[i]['qs']) else '📄'} {arts[i]['title']}" for i in range(len(arts))]
    selected=st.selectbox("選擇文章",art_names,index=idx)
    new_idx=art_names.index(selected)
    if new_idx!=S.r_idx: S.r_idx=new_idx; st.rerun()
    art=arts[idx]
    st.markdown(f"#### {art['title']}")
    with st.expander("📄 閱讀文章",expanded=True): st.text(art["text"])
    st.markdown("---")
    art_done=done.get(str(idx),{})
    for qi,q in enumerate(art["qs"]):
        st.markdown(f"**Q{qi+1}. {q['q']}**")
        answered=str(qi) in art_done
        for i,opt in enumerate(q["opts"]):
            label=f"{chr(65+i)}. {opt}"
            if answered:
                if i==q["ans"]: st.markdown(f'<div style="background:#ecfdf5;border:2px solid #10b981;border-radius:8px;padding:.5rem 1rem;margin:.25rem 0">✅ {label}</div>', unsafe_allow_html=True)
                elif i==art_done[str(qi)]: st.markdown(f'<div style="background:#fef2f2;border:2px solid #ef4444;border-radius:8px;padding:.5rem 1rem;margin:.25rem 0">❌ {label}</div>', unsafe_allow_html=True)
                else: st.markdown(f'<div style="background:#f8fafc;border:1px solid #e2e8f0;border-radius:8px;padding:.5rem 1rem;margin:.25rem 0;color:#94a3b8">{label}</div>', unsafe_allow_html=True)
            else:
                if st.button(label, key=f"r_{idx}_{qi}_{i}", use_container_width=True):
                    if str(idx) not in done: done[str(idx)]={}
                    done[str(idx)][str(qi)]=i; ok=(i==q["ans"])
                    S.correct+=(1 if ok else 0); S.total+=1
                    if not ok: add_mistake("reading",q["q"],q["opts"][q["ans"]],opt)
                    st.rerun()
        st.markdown("")
    answered_count=len(art_done)
    if answered_count==len(art["qs"]):
        correct_count=sum(1 for qi2,i2 in art_done.items() if i2==art["qs"][int(qi2)]["ans"])
        st.success(f"✅ 本篇完成！正確率 {correct_count}/{len(art['qs'])}")
        if idx+1<len(arts):
            if st.button("▶️ 下一篇"): S.r_idx+=1; st.rerun()

# ─────────────────────────────────────────────────────────────────────────────
# 頁面：計時模擬考
# ─────────────────────────────────────────────────────────────────────────────
def page_mock():
    st.markdown("## ⏱ 計時模擬考")
    MOCK_TIME=30*60

    def build_mock():
        qs=[]
        for q in random.sample(GRAMMAR_QS,min(20,len(GRAMMAR_QS))): qs.append({**q,"source":"grammar"})
        r_qs=[]
        for art in READINGS:
            for qi,q in enumerate(art["qs"]): r_qs.append({**q,"source":"reading","article":art["title"]})
        for q in random.sample(r_qs,min(20,len(r_qs))): qs.append(q)
        for w in random.sample(VOCAB,min(10,len(VOCAB))):
            same=[x for x in VOCAB if x["pos"]==w["pos"] and x["word"]!=w["word"]]
            wrongs=random.sample(same,min(3,len(same)))
            opts=[w["word"]]+[x["word"] for x in wrongs]; random.shuffle(opts)
            qs.append({"q":f"選出正確單字：{w['zh']} ({w['pos']})","opts":opts,"ans":opts.index(w["word"]),"source":"vocab"})
        random.shuffle(qs); return qs

    if not S.mock_started:
        st.info("📋 共 50 題（文法 20、閱讀 20、單字 10）　限時 **30 分鐘**")
        if st.button("▶️ 開始模擬考", type="primary"):
            S.mock_qs=build_mock(); S.mock_idx=0; S.mock_done={}
            S.mock_started=True; S.mock_end_time=time.time()+MOCK_TIME
            S.mock_finished=False; S.sessions+=1; st.rerun()
        return

    if S.mock_finished or S.mock_idx>=len(S.mock_qs): _show_mock_result(); return

    remaining=S.mock_end_time-time.time()
    if remaining<=0: S.mock_finished=True; st.rerun()

    render_timer(remaining, MOCK_TIME)
    pct=len(S.mock_done)/len(S.mock_qs)
    st.markdown(f'<div class="pb-wrap"><div class="pb" style="width:{pct*100:.0f}%"></div></div><small>已作答 {len(S.mock_done)}/{len(S.mock_qs)}</small>', unsafe_allow_html=True)

    idx=S.mock_idx
    while idx<len(S.mock_qs) and str(idx) in S.mock_done: idx+=1
    if idx>=len(S.mock_qs): S.mock_finished=True; st.rerun()
    S.mock_idx=idx; q=S.mock_qs[idx]
    src={"grammar":"📝 文法","reading":"📖 閱讀","vocab":"📚 單字"}.get(q.get("source",""),"")
    st.markdown(f"<div class='tcard'><small style='color:#64748b'>{src} ‧ Q{idx+1}/{len(S.mock_qs)}</small><br><b>{q['q']}</b></div>", unsafe_allow_html=True)
    if q.get("article"):
        with st.expander("📄 查看相關文章"):
            for art in READINGS:
                if art["title"]==q["article"]: st.text(art["text"])
    for i,opt in enumerate(q["opts"]):
        if st.button(f"{chr(65+i)}. {opt}", key=f"mock_{idx}_{i}", use_container_width=True):
            S.mock_done[str(idx)]=i; S.mock_idx=idx+1; st.rerun()
    if st.button("⏹ 交卷"): S.mock_finished=True; st.rerun()
    time.sleep(1); st.rerun()

def _show_mock_result():
    qs=S.mock_qs; done=S.mock_done
    correct=sum(1 for k,v in done.items() if v==qs[int(k)]["ans"])
    acc=correct/len(qs)*100
    S.correct+=correct; S.total+=len(qs); S.mock_started=False
    est="990 🏆" if acc>=96 else "~950" if acc>=92 else "~850 ✨" if acc>=87 else "~800" if acc>=80 else "~730" if acc>=72 else "~650" if acc>=62 else "~550"
    st.markdown(f"""<div style="background:linear-gradient(135deg,#2563eb,#7c3aed);color:white;border-radius:16px;padding:2rem;text-align:center;margin-bottom:1rem">
    <div style="font-size:3rem;font-weight:900">{acc:.0f}%</div>
    <div style="font-size:1.3rem;margin:.5rem 0">預估多益分數：{est}</div>
    <div style="opacity:.85">正確 {correct}/{len(qs)} 題</div>
    </div>""", unsafe_allow_html=True)
    by={"grammar":[0,0],"reading":[0,0],"vocab":[0,0]}
    for k,v in done.items():
        q=qs[int(k)]; s=q.get("source","grammar"); by[s][1]+=1
        if v==q["ans"]: by[s][0]+=1
    c1,c2,c3=st.columns(3)
    for col,(s,l) in zip([c1,c2,c3],[("grammar","📝 文法"),("reading","📖 閱讀"),("vocab","📚 單字")]):
        co,to=by[s]; a=f"{co/to*100:.0f}%" if to else "—"
        with col: st.metric(l,a,f"{co}/{to}")
    if st.button("🔄 重新考一次",type="primary"): S.mock_started=False; S.mock_finished=False; st.rerun()

# ─────────────────────────────────────────────────────────────────────────────
# 頁面：錯題複習
# ─────────────────────────────────────────────────────────────────────────────
def page_review():
    st.markdown("## 🔴 錯題複習")
    mistakes=S.mistakes
    if not mistakes: st.success("🎉 目前沒有錯題！繼續保持！"); return
    st.info(f"共 {len(mistakes)} 道待複習錯題")
    idx=S.rev_idx; done=S.rev_done
    if idx>=len(mistakes):
        correct=sum(1 for v in done.values() if v); st.success(f"✅ 複習完成！重新答對 {correct}/{len(mistakes)}")
        if st.button("🔄 再複習"): S.rev_idx=0; S.rev_done={}; st.rerun()
        if st.button("🗑️ 清除所有錯題"): S.mistakes=[]; S.rev_idx=0; S.rev_done={}; st.rerun()
        return
    pct=idx/len(mistakes)
    st.markdown(f'<div class="pb-wrap"><div class="pb" style="width:{pct*100:.0f}%"></div></div><small>第 {idx+1}/{len(mistakes)}</small>', unsafe_allow_html=True)
    m=mistakes[idx]; answered=str(idx) in done
    tl={"grammar":"📝 文法","reading":"📖 閱讀","listen_p2":"🎧 Part2","listen_p3":"🎧 Part3","listen_p4":"🎧 Part4","vocab":"📚 單字","game_quiz":"⚡ 遊戲","game_speed":"⌨️ 遊戲"}.get(m["type"],"題目")
    st.markdown(f"<div class='tcard'><small style='color:#ef4444'>{tl} 錯題</small><br><b>{m['q']}</b></div>", unsafe_allow_html=True)
    if not answered:
        pool=list({m["correct"],m["chosen"]}|set(random.sample([w["word"] for w in VOCAB if w["word"] not in {m["correct"],m["chosen"]}],min(2,len(VOCAB)))))
        random.shuffle(pool)
        for opt in pool:
            if st.button(opt, key=f"rev_{idx}_{opt}", use_container_width=True):
                ok=(opt==m["correct"]); done[str(idx)]=ok
                if ok: st.success("✅ 這次答對了！")
                else: st.error(f"❌ 正確：{m['correct']}")
                st.rerun()
    else:
        ok=done[str(idx)]
        if ok: st.markdown(f'<div class="fb-ok">✅ 正確答案：{m["correct"]}</div>', unsafe_allow_html=True)
        else: st.markdown(f'<div class="fb-bad">❌ 正確：{m["correct"]}　你選：{m["chosen"]}</div>', unsafe_allow_html=True)
        if st.button("下一題 →", type="primary"): S.rev_idx+=1; st.rerun()

# ─────────────────────────────────────────────────────────────────────────────
# 頁面：單字庫
# ─────────────────────────────────────────────────────────────────────────────
def page_wordlist():
    st.markdown("## 📋 單字庫")
    c1, c2, c3 = st.columns([3, 2, 2])
    with c1: query = st.text_input("🔍 搜尋單字或中文", value=S.wl_query, placeholder="allocate / 分配...")
    with c2: cat = st.selectbox("分類", ["全部"] + sorted(set(w["cat"] for w in VOCAB)))
    with c3: wl_range = st.selectbox("分數區間", ["全部", "600-780", "780-900", "900+"])
    S.wl_query = query; S.wl_cat = cat
    filtered = VOCAB
    if query:
        q = query.lower()
        filtered = [w for w in filtered if q in w["word"].lower() or q in w["zh"]]
    if cat != "全部": filtered = [w for w in filtered if w["cat"] == cat]
    if wl_range != "全部": filtered = [w for w in filtered if w["range"] == wl_range]
    range_colors = {"780-900": "#dbeafe", "900+": "#f3e8ff", "600-780": "#f0fdf4"}
    st.markdown(f"<small style='color:#64748b'>顯示 {len(filtered)}/{len(VOCAB)} 筆</small>", unsafe_allow_html=True)
    st.markdown("---")
    for w in filtered:
        mark = "✅ " if w["word"] in S.learned else ""
        rng = w.get("range", "")
        rng_bg = range_colors.get(rng, "#f8fafc")
        rng_tag = f'<span style="background:{rng_bg};border-radius:4px;padding:.1rem .4rem;font-size:.68rem;font-weight:700;white-space:nowrap">{rng}</span>'
        st.markdown(f'<div class="wl-row"><div class="wl-word">{mark}{w["word"]}</div>{tag_html(w["pos"])}{rng_tag}<div class="wl-zh">{w["zh"]}</div><div class="wl-ex">{w["ex"]}</div></div>', unsafe_allow_html=True)
    st.markdown("<br><small style='color:#94a3b8'>詞彙資料來源：<a href='https://huggingface.co/datasets/kknono668/toeic-vocab-tw' target='_blank'>kknono668/toeic-vocab-tw</a>（CC-BY-SA-4.0）</small>", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# 頁面：AI 出題
# ─────────────────────────────────────────────────────────────────────────────
def page_ai():
    st.markdown("## 🤖 AI 自動出題")
    st.info(f"從 {len(VOCAB):,} 個單字庫中隨機抽取，自動生成填空選擇題。")
    if st.button("🎲 生成 5 題",type="primary"):
        sample=random.sample(VOCAB,5)
        TEMPLATES=[
            lambda w:f"The company decided to _____ the new policy. （{w['zh']}）",
            lambda w:f"She was praised for being highly _____ in her work. （{w['zh']}）",
            lambda w:f"We need to _____ our resources more effectively. （{w['zh']}）",
            lambda w:f"Please _____ the document before the meeting. （{w['zh']}）",
            lambda w:f"The manager asked the team to _____ the project. （{w['zh']}）",
        ]
        qs=[]
        for i,w in enumerate(sample):
            same=[x for x in VOCAB if x["pos"]==w["pos"] and x["word"]!=w["word"]]
            wrongs=random.sample(same,min(3,len(same)))
            opts=[w["word"]]+[x["word"] for x in wrongs]; random.shuffle(opts)
            qs.append({"q":TEMPLATES[i%len(TEMPLATES)](w),"opts":opts,"ans":opts.index(w["word"]),"exp":f"{w['word']}（{w['zh']}）— {w['ex']}"})
        st.session_state["ai_qs"]=qs; st.session_state["ai_done"]={}
    for qi,q in enumerate(st.session_state.get("ai_qs",[])):
        st.markdown(f"**Q{qi+1}. {q['q']}**")
        answered=str(qi) in st.session_state.get("ai_done",{})
        for i,opt in enumerate(q["opts"]):
            label=f"{chr(65+i)}. {opt}"
            if answered:
                if i==q["ans"]: st.markdown(f'<div style="background:#ecfdf5;border:2px solid #10b981;border-radius:8px;padding:.5rem 1rem;margin:.2rem 0">✅ {label}</div>', unsafe_allow_html=True)
                elif i==st.session_state["ai_done"][str(qi)]: st.markdown(f'<div style="background:#fef2f2;border:2px solid #ef4444;border-radius:8px;padding:.5rem 1rem;margin:.2rem 0">❌ {label}</div>', unsafe_allow_html=True)
                else: st.markdown(f'<div style="background:#f8fafc;border:1px solid #e2e8f0;border-radius:8px;padding:.5rem 1rem;margin:.2rem 0;color:#94a3b8">{label}</div>', unsafe_allow_html=True)
            else:
                if st.button(label, key=f"ai_{qi}_{i}", use_container_width=True):
                    st.session_state["ai_done"][str(qi)]=i; ok=(i==q["ans"])
                    S.correct+=(1 if ok else 0); S.total+=1
                    if not ok: add_mistake("vocab",q["q"],q["opts"][q["ans"]],opt)
                    st.rerun()
        if answered: st.markdown(f'<div class="fb-ok">💡 {q["exp"]}</div>', unsafe_allow_html=True)
        st.markdown("")

# ─────────────────────────────────────────────────────────────────────────────
# 主程式
# ─────────────────────────────────────────────────────────────────────────────
TABS = ["🏠 首頁","📅 打卡","🎮 遊戲","📚 單字卡","📝 文法","🎧 聽力","📖 閱讀","⏱ 模擬考","🔴 錯題","📋 單字庫","🤖 AI 出題"]
tabs = st.tabs(TABS)

with tabs[0]:  page_home()
with tabs[1]:  page_checkin()
with tabs[2]:  page_games()
with tabs[3]:  page_vocab()
with tabs[4]:  page_grammar()
with tabs[5]:  page_listening()
with tabs[6]:  page_reading()
with tabs[7]:  page_mock()
with tabs[8]:  page_review()
with tabs[9]:  page_wordlist()
with tabs[10]: page_ai()
